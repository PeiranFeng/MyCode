import torch
import pandas as pd

from typing import Tuple
from pathlib import Path

from fenghe.utility.load_ext import ExtLoader

def _get_ext_loader(ext_name: str):
    base = Path(__file__).parent
    sources = [
        str(base / 'src' / 'causal_filling.cu'),
        str(base / 'src' / 'causal_filling_binding.cpp')
    ]
    extra_include_paths = [
        str(base / 'include')
    ]
    loader = ExtLoader(ext_name=ext_name, sources=sources, extra_include_paths=extra_include_paths)
    return loader

def _query_id(query: torch.Tensor, idx: pd.Index):
    return torch.tensor(idx.get_indexer(query), dtype=torch.uint32)

def _query_key(query: torch.Tensor, idx: pd.Index, dtype: torch.dtype):
    key = idx[query.cpu().numpy()]
    return torch.tensor(key, dtype=dtype)

def _compress_to_uint32(vals: torch.Tensor):
    assert vals.dim() == 1
    assert vals.numel() <= torch.iinfo(torch.uint32).max

    idx = pd.Index(vals.cpu().numpy())
    return idx

def _pack(k0_ids: torch.Tensor, k1_ids: torch.Tensor):
    packed = (k0_ids.to(torch.uint64) << 32) | k1_ids.to(torch.uint64)
    return packed

def _unpack(packed: torch.Tensor):
    k1_id = packed >> 32
    k2_id = packed & 0xFFFFFFFF
    return k1_id, k2_id

def causal_filling(
    src_time: torch.Tensor,
    tgt_time: torch.Tensor,
    *,
    src_key: None|torch.Tensor|Tuple[torch.Tensor, torch.Tensor] = None,
    tgt_key: None|torch.Tensor|Tuple[torch.Tensor, torch.Tensor] = None,
    latency: int = 0,
    lookback: int = 0,
    unfound: int = -1
):
    """
    For each t in tgt_time, find latest s in src_time.
    s ∈ [t - lookback, t - latency]

    Args:
        src_time: A slice of the reference time.
        tgt_time: The reference time.
        src_key:  Slices of the reference keys(factor/stock).
        tgt_key:  The reference keys(factor/stock).
        latency:  Defines the minimum offset from the current time t for backward lookup.
        lookback: Defines the maximum lool-back dutation on the timeline.

    Returns:
        src_indices: 1D tensor
        tgt_t_indices: 1D tensor
        tgt_k_indices: None|torch.Tensor|Tuple[torch.Tensor, torch.Tensor]
        offsets: torch.Tensor

    Notes:
        The src_key and tgt_key must in the same data structure.
        If given multi keys, the length of tuple must be equal to 2.
        All tensor must be contiguous.
    """
    #TODO Finish assert
    assert tgt_time.dim() == 1

    # Build group ids
    if src_key is None:
        src_gids = torch.zeros([1,], dtype=torch.uint32)
        tgt_gids = torch.zeros([1,], dtype=torch.uint32)
    elif isinstance(src_key, torch.Tensor):
        src_gids = src_key
        tgt_gids = tgt_key
    elif isinstance(src_key, Tuple):
        assert len(src_key) == 2, f"The length of src_key must be equal to 2, given {len(src_key)}"
        assert len(src_key, tgt_key), f"The length of tgt_key must be equal to 2, given {len(tgt_key)}"
        # Build key <-> id map
        k0_idx = _compress_to_uint32(tgt_key[0])
        k1_idx = _compress_to_uint32(tgt_key[1])
        
        src_k0_ids = _query_id(src_key[0], k0_idx)
        src_k1_ids = _query_id(src_key[1], k1_idx)
        src_gids = _pack(k0_ids=src_k0_ids, k1_ids=src_k1_ids)

        tgt_k0_ids = _query_id(tgt_key[0], k0_idx)
        tgt_k1_ids = _query_id(tgt_key[1], k1_idx)
        tgt_gids = _pack(k0_ids=tgt_k0_ids, k1_ids=tgt_k1_ids)
    else:
        raise RuntimeError(f"param type error: src_key must be None|torch.Tensor|Tuple, given {type(src_key)}")
    
    # Build the output Tensors.
    src_indices = torch.empty_like(tgt_time).to(torch.int64)
    tgt_t_indices = torch.empty_like(tgt_time).to(torch.int64)
    tgt_g_indices = torch.empty_like(tgt_time).to(torch.int64)
    offsets = torch.zeros_like(tgt_time).to(torch.int64)

    # Load cpp ext
    ext = _get_ext_loader('causal_filling_ext').load()
    ext.causal_filling(
        src_time=src_time, 
        src_gids=src_gids,
        tgt_time=tgt_time, 
        tgt_gids=tgt_gids,
        src_indices=src_indices, 
        tgt_t_indices=tgt_t_indices, 
        tgt_g_indices=tgt_g_indices,
        offsets=offsets,
        latency=latency, 
        lookback=lookback
    )

    if src_key is None:
        return src_indices, tgt_t_indices, None, offsets
    elif isinstance(src_key, torch.Tensor):
        return src_indices, tgt_t_indices, tgt_g_indices, offsets
    else:
        # unpack
        group_ids = torch.gather(tgt_gids, dim=0, index=tgt_g_indices)
        tgt_k0_indices, tgt_k1_indices = _unpack(group_ids)
        return src_indices, tgt_t_indices, (tgt_k0_indices, tgt_k1_indices), offsets

    

    
