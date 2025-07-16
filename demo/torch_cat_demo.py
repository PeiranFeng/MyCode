import torch
from torch import nn
import numpy as np

# shape of a is (3, 3) number_dimensions=2 rank of dim is [-2, 1]
a = torch.tensor([[1,2,3], [4,5,6], [7,8,9]], dtype=torch.float32, requires_grad=False)
offset = torch.tensor([10, 10, 10])
b = torch.cat([a, a+offset, a+offset*2], dim=0)
print(b) # shape (9, 3)
b = torch.cat([a, a+offset, a+offset*2], dim=1)
print(b) # shape (3, 9)
b = torch.cat([a, a+offset, a+offset*2], dim=-1)
print(b) # shape (3, 9)

# ndim=3 rank of dim is [-3, 2]
a = torch.rand((2, 3, 3))
b = torch.cat([a, a+offset], dim = 2)
print(b) # shape (2, 3, 6)

# ndim=n rank of dim is [-n, n-1]

