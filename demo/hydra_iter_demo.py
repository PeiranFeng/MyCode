import yaml
from typing import List, Tuple, Dict, Any, Union
from itertools import product
from pathlib import Path
from functools import singledispatchmethod

class LinearSweep:
    def __init__(self, node_name: str, values: List[str]):
        self.node_name = node_name
        self.values = values
    def __iter__(self):
        for v in self.values:
            # s = yaml.dump(v).rstrip('\n...\n')
            yield {self.node_name:v}

class Iter:
    def __init__(self, items: List[Dict[str, Any]]):
        self.items = items if items else []
    
    def __iter__(self):
        yield from self.items

    @singledispatchmethod    
    def __add__(self, anothor):
        raise NotImplementedError
    
    def __repr__(self):
        return list(self.items).__repr__()

@Iter.__add__.register
def _(self, anothor: Iter):
    self.items.extend(anothor.items)
    return self


class IterGenerator:
    @classmethod
    def _product_(cls, *sweeps):
        for sweep in sweeps:
            assert isinstance(sweep, LinearSweep)
        for _ in product(*sweeps):
            yield _

    @classmethod
    def _obj_cat_(cls, *objs):
        res = {}
        for obj in objs:
            assert isinstance(obj, dict)
            res |= obj
        return res

    @classmethod
    def iter_linear(cls, *args):
        iter = Iter([])
        for arg in args:
            assert isinstance(arg, Iter)
            iter += arg
        return iter

    @classmethod
    def iter_product(cls, *args):
        return Iter([cls._obj_cat_(*_) for _ in product(*args)])
    
    @classmethod
    def linear(cls, node_name: str, values: List[Any]):
        assert isinstance(node_name, str)
        assert isinstance(values, list)
        return Iter(LinearSweep(node_name, values))

    @classmethod
    def product(cls, *args):
        overrides = {}
        for arg in args:
            assert isinstance(arg, dict)
            overrides |= arg
        sweeps = [LinearSweep(k,v) for k, v in overrides.items()]
        return Iter([cls._obj_cat_(*_) for _ in cls._product_(*sweeps)])

    @classmethod
    def concatenate(cls, *args):
        """
        Use case:
         IterGenerator._concatenate_(
            {"data.schema_file_path": "../schema/feature-2.yaml"},
            {"models.base.encoder.embedding": 8},
            {"constants.rebalance_period": 10}
         )

        Will return:
         Iter([{
            "data.schema_file_path": "../schema/feature-2.yaml",
            "models.base.encoder.embedding": 8,s
            "constants.rebalance_period": 10
         }])
        """
        overrides = {}
        for arg in args:
            assert isinstance(arg, dict), "Parameters of concatenate method must be dict."
            overrides |= arg
        sweeps = [LinearSweep(k,[v]) for k, v in overrides.items()]
        return Iter([cls._obj_cat_(*_) for _ in cls._product_(*sweeps)])

def iter():
    """
        A Node to be overridden should not be an interpolation node, otherwise, its original structure will be lost. 
    """
    # yield from IterGenerator.iter_linear(
    #     IterGenerator.concatenate({"constants.cor_s_condition_dim": "null"}, {"constants.cor_t_condition_dim": "null"}),
    #     IterGenerator.concatenate({"constants.cor_s_condition_dim": 2},{"constants.cor_t_condition_dim": 0})
    # )
    # yield from IterGenerator.linear('a', [1,2,3])
    # yield from IterGenerator.product(
    #     {'a': [1,2,3]},
    #     {'b': [10, 100]}
    # )
    # yield from IterGenerator.iter_linear(
    #     IterGenerator.product({'a':[4,5]},{'b':[1000]}),
    #     IterGenerator.product({'a':[1,2,3]},{'b':[10,100]})
    # )

    # yield from IterGenerator.iter_product(
    #     IterGenerator.concatenate({'a':10}, {'b':20}),
    #     IterGenerator.linear('c',[5,15,20])
    # )

    yield from IterGenerator.iter_product(
        IterGenerator.iter_linear(
            IterGenerator.concatenate({'a1':100},{'a2':200}),
            IterGenerator.linear('c', [5,10])
        ),
        IterGenerator.linear('d', [[4, -1], [3, -1], [2, -1]])
    )

if __name__ == '__main__':
    print(list(iter()))