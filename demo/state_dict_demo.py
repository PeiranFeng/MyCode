import torch
import torch.nn as nn

class DummyModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.param = nn.Parameter(torch.tensor(1.0))
    
    def state_dict(self):
        return {'param': self.param}