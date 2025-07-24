import torch

nrows = 2
value = torch.tensor([1,2,3])
size = value.size()
assert size == (3,)
value = torch.unsqueeze(value, dim=0)
assert value.size() == (1,3)
value = value.expand(2, *size)
assert value.size() == (2, 3)