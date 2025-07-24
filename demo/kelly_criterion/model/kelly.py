import torch
from torch import nn
from einops import einsum

class Kelly(nn.Module):
    def __init__(self, num_layers, input_dim, hidden_dim, output_dim):
        super().__init__()
        self.layers = nn.ModuleList([
            nn.Linear() for _ in range(num_layers)
        ])