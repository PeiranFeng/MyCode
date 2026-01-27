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

def causal_filling(
    src_time: torch.Tensor,
    tgt_time: torch.Tensor,
    *,
    src_key: None|torch.Tensor|Tuple[torch.Tensor, torch.Tensor] = None,
    tgt_key: None|torch.Tensor|Tuple[torch.Tensor, torch.Tensor] = None,
    latency: int = 0,
    lookback: int = 0,
    unfound_padding: int = -1
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
        unfound_padding:  Padding of unfound source indices.

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

    # Build the output Tensors.
    src_indices = torch.empty_like(tgt_time).to(torch.int64)
    tgt_t_indices = torch.empty_like(tgt_time).to(torch.int64)
    tgt_k0_indices = torch.empty_like(tgt_time).to(torch.int64)
    tgt_k1_indices = torch.empty_like(tgt_time).to(torch.int64)
    offsets = torch.zeros_like(tgt_time).to(torch.int64)

    # Load cpp ext
    ext = _get_ext_loader('causal_filling_ext').load()

    if src_key is None:
        return src_indices, tgt_t_indices, None, offsets
    elif isinstance(src_key, torch.Tensor):
        ext.causal_filling_2d(
            src_time=src_time, 
            src_gids=src_key,
            tgt_time=tgt_time, 
            tgt_gids=tgt_key,
            src_indices=src_indices, 
            tgt_t_indices=tgt_t_indices, 
            tgt_k_indices=tgt_k0_indices,
            offsets=offsets,
            latency=latency, 
            lookback=lookback,
            padding=unfound_padding
        )
        assert len(tgt_k0_indices)==1
        return src_indices, tgt_t_indices, tgt_k0_indices, offsets
    elif isinstance(src_key, Tuple):
        assert len(src_key) == 2, f"The length of src_key must be equal to 2, given {len(src_key)}"
        assert len(src_key, tgt_key), f"The length of tgt_key must be equal to 2, given {len(tgt_key)}"
        
        return src_indices, tgt_t_indices, (tgt_k0_indices, tgt_k1_indices), offsets
    else:
        raise RuntimeError(f"param type error: src_key must be None|torch.Tensor|Tuple, given {type(src_key)}")


    

    
