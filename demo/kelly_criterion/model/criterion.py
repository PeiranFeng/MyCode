import torch
from torch import nn

class ProfitLoss(nn.Module):
    def __init__(self, p: float, r: float):
        assert p>0 and p<1, 'p should be in (0, 1).'
        assert r > 0, 'r should be nonnegative.'
        super().__init__()
        self.target = 
        