import torch
from operator import mul
from functools import reduce

cinsert = torch.ones((110))
normal = torch.randn((110,414))

def merge(x: torch.Tensor, dim0=0, dim1=None):
    if dim1 is None:
        dim1 = x.dim()
    s = tuple(x.size())
    n = reduce(mul, s[dim0:dim1], 1)
    s = s[:dim0] + (n,) + s[dim1:]
    return x.reshape(*s)

cinsert = cinsert.unsqueeze(-1).expand(normal.size())
print(merge(cinsert, 0).size())
print(merge(normal, 0, 2).size())
assert merge(cinsert, 0).size() == merge(normal, 0, 2).size()