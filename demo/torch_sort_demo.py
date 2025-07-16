import torch
from datetime import date

class MyTensor(torch.Tensor):
    origin = date.fromisoformat("1970-01-01")

    @staticmethod
    def __new__(cls, data: date, modify=True, *args, **kwargs):
        data = (data - MyTensor.origin).days
        obj = super().__new__(cls, [data], *args, **kwargs)
        if modify:
            obj = obj.int()
        return obj
    
    def sort(self, dim=-1, descending=False):
        ret = super().sort(dim, descending)
        return (ret[0], ret[1]._base_())
    
    @classmethod
    def __torch_function__(cls, func, types, args=(), kwargs=None):
        if kwargs is None:
            kwargs = {}

        ret = super().__torch_function__(func, types, args, kwargs)
        if func.__name__ == 'sort':
            # ret = (ret[0], ret[1]._base_())  # Ensure second return value is a standard tensor
            print(f"Calling {func.__name__} with types {types} and args {args}")
        return ret
    
    def _base_(self):
        return torch.Tensor(self)

if __name__ == '__main__':
    x = MyTensor(date.today(), modify=True)
    print('x',x)
    print('x.sort()',x.sort())
    print('torch.sort(x)',torch.sort(x))