// causal_filling
#pragma once

#include <vector>
#include <cstdint>
#include <torch/extension.h>

/// Grouped by gid.
/// For each t in tgt_time, find latest s in src_time.
/// s ∈ [t-lookback, t-latency].
///
/// @param src_time a slice of reference time
/// @param src_gids  group ids 
/// @param tgt_time reference time
/// @param tgt_gids  group ids packed by the reference keys(factor/stock)
/// @param src_indices output of source indices
/// @param tgt_t_indices output of target time indices
/// @param tgt_g_indices output of target group indices
/// @param offsets output of offsets from index t to s
/// @param latency 
/// @param lookback
/// @return src_indices, tgt_t_indices, tgt_k_indices, offsets
template <typename Ttime, typename Tkey>
std::vector<torch.Tensor> causal_filling(
    torch::Tensor src_time,
    torch::Tensor src_gids,
    torch::Tensor tgt_time,
    torch::Tensor tgt_gids,
    torch::Tensor src_indices,
    torch::Tensor tgt_t_indices,
    torch::Tensor tgt_g_indices,
    torch::Tensor offsets,
    int32_t lookback,
    int32_t latency 
);

extern template std::vector<torch::Tensor> causal_filling<int64_t, uint64_t>(
    torch::Tensor, torch::Tensor, torch::Tensor, torch::Tensor,
    torch::Tensor, torch::Tensor, torch::Tensor, torch::Tensor, 
    int32_t, int32_t
);

extern template std::vector<torch::Tensor> causal_filling<int64_t, uint32_t>(
    torch::Tensor, torch::Tensor, torch::Tensor, torch::Tensor,
    torch::Tensor, torch::Tensor, torch::Tensor, torch::Tensor, 
    int32_t, int32_t
);