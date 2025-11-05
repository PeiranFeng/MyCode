import torch

class CascadeWeighter:
    def __init__(self, components):
        super().__init__()
        self.components = components
    def __call__(self, weight):
        w = Identity()
        if len(self.components):
            for component in self.components:
                w = w * component(weight)
            return w
        else:
            return w(weight)


class Identity:
    def __init__(self):
        pass
    def __mul__(self, another):
        return another
    def __rmul__(self, another):
        return another
    def __call__(self, weight):
        return torch.ones(weight.size(),dtype=bool)
    