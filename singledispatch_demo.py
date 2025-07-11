from functools import singledispatch
import torch

@singledispatch
def func(arg: any):
    print('basic func with an any arg:', arg)

@func.register(int)
def _(arg: int):
    print('func with an int arg:', arg)

@func.register(str)
def _(arg: str):
    print('func with a str arg:', arg)

@singledispatch
def _size_(input):
    matrix = tuple()
    batch = tuple()
    return matrix, batch

@_size_.register
def _(input:torch.Tensor):
    matrix = tuple()
    batch = input.size()
    return matrix, batch

if __name__ == '__main__':
    func(42)  # Calls the int version
    func("Hello")  # Calls the str version  
    func(3.14)

    a = torch.rand((2, 3, 3))
    matrix, batch = _size_(a)
    print('matrix:', matrix)
    print('batch:', batch)