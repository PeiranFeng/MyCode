import torch
from torch.distributions import LowRankMultivariateNormal

m = LowRankMultivariateNormal(torch.zeros(2), torch.tensor([[1.], [0.]]), torch.ones(2))
s = m.sample(torch.Size((10, 5)))
print(s.shape)