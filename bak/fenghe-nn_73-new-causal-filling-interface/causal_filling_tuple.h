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
/// @param src_keys slices of reference keys
/// @param tgt_time reference time
/// @param tgt_keys  reference keys(factor/stock)
/// @param src_indices output of source indices
/// @param tgt_t_indices output of target time indices
/// @param tgt_k_indices output of target key indices
/// @param offsets output of offsets from index t to s
/// @param latency 
/// @param lookback
/// @return src_indices, tgt_t_indices, tgt_k_indices, offsets
template <typename Ttime, typename Tkey>
void causal_filling(
    torch::Tensor src_time,
    std::vector<torch::Tensor> src_keys,
    torch::Tensor tgt_time,
    std::vector<torch::Tensor> tgt_keys,
    torch::Tensor src_indices,
    torch::Tensor tgt_t_indices,
    std::vector<torch::Tensor> tgt_k_indices,
    torch::Tensor offsets,
    Ttime lookback,
    Ttime latency,
    int32_t padding
);

extern template void causal_filling<int64_t, int64_t>(
    torch::Tensor, std::vector<torch::Tensor>, 
    torch::Tensor, std::vector<torch::Tensor>,
    torch::Tensor, torch::Tensor, std::vector<torch::Tensor>, torch::Tensor, 
    int64_t, int64_t, int32_t
);