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
/// @param tgt_time reference time
/// @param src_indices output of source indices
/// @param tgt_t_indices output of target time indices
/// @param offsets output of offsets from index t to s
/// @param latency 
/// @param lookback
/// @param padding
template <typename Ttime>
void causal_filling_1d(
    torch::Tensor src_time,
    torch::Tensor tgt_time,
    torch::Tensor src_indices,
    torch::Tensor tgt_t_indices,
    torch::Tensor offsets,
    Ttime lookback,
    Ttime latency,
    int32_t padding
);

/// Grouped by gid.
/// For each t in tgt_time, find latest s in src_time.
/// s ∈ [t-lookback, t-latency].
///
/// @param src_time a slice of reference time
/// @param src_key a slice of reference keys
/// @param tgt_time reference time
/// @param tgt_key  reference key(factor/stock)
/// @param src_indices output of source indices
/// @param tgt_t_indices output of target time indices
/// @param tgt_k_indices output of target key indices
/// @param offsets output of offsets from index t to s
/// @param latency 
/// @param lookback
/// @param padding
template <typename Ttime, typename Tkey>
void causal_filling_2d(
    torch::Tensor src_time,
    torch::Tensor src_key,
    torch::Tensor tgt_time,
    torch::Tensor tgt_key,
    torch::Tensor src_indices,
    torch::Tensor tgt_t_indices,
    torch::Tensor tgt_k_indices,
    torch::Tensor offsets,
    Ttime lookback,
    Ttime latency,
    int32_t padding
);

/// Grouped by gid.
/// For each t in tgt_time, find latest s in src_time.
/// s ∈ [t-lookback, t-latency].
///
/// @param src_time a slice of reference time
/// @param src_key0 a slice of reference keys
/// @param src_key1 a slice of reference keys
/// @param tgt_time reference time
/// @param tgt_key0  reference key(factor/stock)
/// @param tgt_key1  reference key(factor/stock)
/// @param src_indices output of source indices
/// @param tgt_t_indices output of target time indices
/// @param tgt_k0_indices output of target key indices
/// @param tgt_k1_indices output of target key indices
/// @param offsets output of offsets from index t to s
/// @param latency 
/// @param lookback
/// @param padding
template <typename Ttime, typename Tkey0, typename Tkey1>
void causal_filling_3d(
    torch::Tensor src_time,
    torch::Tensor src_key0,
    torch::Tensor src_key1,
    torch::Tensor tgt_time,
    torch::Tensor tgt_key0,
    torch::Tensor tgt_key1,
    torch::Tensor src_indices,
    torch::Tensor tgt_t_indices,
    torch::Tensor tgt_k0_indices,
    torch::Tensor tgt_k1_indices,
    torch::Tensor offsets,
    Ttime lookback,
    Ttime latency,
    int32_t padding
);

extern template void causal_filling_1d<int64_t, int64_t>(
    torch::Tensor, torch::Tensor,
    torch::Tensor, torch::Tensor, torch::Tensor,
    int64_t, int64_t, int32_t
);

extern template void causal_filling_2d<int64_t, int64_t>(
    torch::Tensor, torch::Tensor, torch::Tensor, torch::Tensor,
    torch::Tensor, torch::Tensor, torch::Tensor, torch::Tensor, 
    int64_t, int64_t, int32_t
);

extern template void causal_filling_3d<int64_t, int64_t>(
    torch::Tensor, torch::Tensor, torch::Tensor, 
    torch::Tensor, torch::Tensor, torch::Tensor,
    torch::Tensor, torch::Tensor, torch::Tensor, torch::Tensor, 
    int64_t, int64_t, int32_t
);