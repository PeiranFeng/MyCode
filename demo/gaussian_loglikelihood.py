# gaussian_loglikelihood.py

import triton
import triton.language as tl
import torch
import math
import time

LOG_2PI = math.log(2 * math.pi)

@triton.jit
def gaussian_loglikelihood_kernel(
    x_ptr, mu_ptr, logvar_ptr, ll_ptr,
    M, N,
    stride_m, stride_n,
    LOG_2PI: tl.constexpr,
    BLOCK_SIZE: tl.constexpr
    ):
    pid = tl.program_id(0)
    padding = 0.0
    if pid >= M:
        return

    x_row_ptr = x_ptr + pid * stride_m

    sum_row = 0.0
    for off_start in range(0, N, BLOCK_SIZE):
        offset = off_start + tl.arange(0, BLOCK_SIZE)
        mask = offset < N
        x = tl.load(x_row_ptr + offset * stride_n, mask, other=padding)
        mu = tl.load(mu_ptr + offset, mask, other=padding)
        logvar = tl.load(logvar_ptr + offset, mask, other=padding)

        diff = x - mu
        exp_neg_logvar = tl.exp(-logvar)
        term = diff * diff * exp_neg_logvar + LOG_2PI + logvar
        term = term * mask # !important
        sum_row += tl.sum(term, axis=0)

    tl.store(ll_ptr + pid, -0.5*sum_row)

def gaussian_loglikelihood_triton(
    x: torch.Tensor,
    mu: torch.Tensor,
    logvar: torch.Tensor,
    block_size=256
    ) -> torch.Tensor:
    B, D = x.shape
    ll = torch.empty(B, device=x.device, dtype=torch.float32)
    grid = lambda meta: (B,)
    gaussian_loglikelihood_kernel[grid](
        x, mu, logvar, ll,
        B, D,
        x.stride(0), x.stride(1),
        LOG_2PI,
        BLOCK_SIZE = block_size
    )
    return ll

def gaussian_loglikelihood_pytorch(
    x: torch.Tensor,
    mu: torch.Tensor,
    logvar: torch.Tensor
    ) -> torch.Tensor:
    diff = x - mu
    exp_neg_logvar = torch.exp(-logvar)

    term = diff * diff * exp_neg_logvar + LOG_2PI + logvar

    ll = -0.5 * term.sum(dim=-1)
    return ll

def benchmark(fn, warmup=10, iters=50):
    for _ in range(warmup):
        fn()
    torch.cuda.synchronize()
    start = time.time()
    for _ in range(iters):
        fn()
    torch.cuda.synchronize()
    end = time.time()

    return (end-start) / iters

def test():
    B = 4
    D = 9
    x = torch.randn(B, D, device="cuda")
    mu = torch.randn(D, device="cuda")
    logvar = torch.randn(D, device="cuda")
    ll = torch.empty(B, device="cuda")

    grid = lambda meta: (B,)

    gaussian_loglikelihood_kernel[grid](
        x, mu, logvar, ll,
        B, D,
        x.stride(0), x.stride(1),
        LOG_2PI,
        BLOCK_SIZE = 4
    )

    print(ll.cpu())
    ll_ref = gaussian_loglikelihood_pytorch(x, mu, logvar)
    assert torch.allclose(ll, ll_ref, atol = 1e-6)

if __name__ == '__main__':
    shapes = [
    (4096, 1024),
    (8192, 1024),
    (4096, 2048),
    (8192, 2048),
    (16384, 1024),
    ]

    for B, D in shapes:
        print(f"\n=== Shape B={B}, D={D} ===")

        x = torch.randn(B, D, device="cuda")
        mu = torch.randn(D, device="cuda")
        logvar = torch.randn(D, device="cuda")

        # Time
        t_torch = benchmark(lambda: gaussian_loglikelihood_pytorch(x, mu, logvar))
        t_triton = benchmark(lambda: gaussian_loglikelihood_triton(x, mu, logvar, block_size=256))

        # Memory
        torch.cuda.reset_peak_memory_stats()
        _ = gaussian_loglikelihood_triton(x, mu, logvar, block_size=256)
        mem_triton = torch.cuda.max_memory_allocated()

        torch.cuda.reset_peak_memory_stats()
        _ = gaussian_loglikelihood_pytorch(x, mu, logvar)
        mem_torch = torch.cuda.max_memory_allocated()

        print(f"Torch   Time: {t_torch*1e3:.3f} ms | Mem: {mem_torch/1024/1024:.2f} MB")
        print(f"Triton  Time: {t_triton*1e3:.3f} ms | Mem: {mem_triton/1024/1024:.2f} MB")
        print(f"Speedup: {t_torch/t_triton:.2f}x")