import yaml
from typing import List, Tuple, Dict, Any, Union
from itertools import product
from pathlib import Path

class LinearSweep:
    def __init__(self, node_name: str, values: List[str]):
        self.node_name = node_name
        self.values = values
    def __iter__(self):
        for v in self.values:
            s = yaml.dump(v).rstrip('\n...\n')
            yield {self.node_name:s}

def iter():
    sweeps = [
        LinearSweep("models.forecast.rebalance_period", [10, 15, 20, 25, 30]),
        LinearSweep("training.generator.input.macro_news_scoring.ratio", [0.9, 0.8, 0.7]),
        # LinearSweep("data_default.schema_file_path", ["../schema/feature-2.yaml"]),
        # LinearSweep("model.encoder.embedding", [16])
    ]

    if not sweeps:
        raise Exception("Sweeps are not configured")
    
    print(list(sweeps[0]), list(sweeps[1]))
    # product use case
    for _ in product(sweeps[0], sweeps[1]):
        # yield _
        print(_)
        exit()

    for _ in sweeps[0]:
        yield _

# def cast(overrides: Union[str, Tuple]):
#     if isinstance(overrides, Tuple):
#         overrides = list(overrides)
#     else:
#         overrides = [overrides]
#     return overrides

def cast(overrides: Union[Dict[str, Any], Tuple[Dict[str, Any]]]):
    if isinstance(overrides, Tuple):
        concatenate = {}
        for override in overrides:
            concatenate |= override
        overrides = concatenate
    return overrides

if __name__ == '__main__':
    for idx, _ in enumerate(iter()):
        print(idx, cast(_))