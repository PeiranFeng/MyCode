import hydra
from omegaconf import DictConfig, OmegaConf
from pathlib import Path
from typing import List, Tuple, Dict, Any
from itertools import product

"""
Use case of Hydra
Basic features:
- Print overrides of configuration by hydra.compose(concatenate and product)
- IoC container by hydra
- Overrides of value quotation
"""

JOD_ID = 0
CONF_DIR = 'conf'
PARENT_PATH = Path(__file__).parent

def concatenate(elements: Dict[str, List]) -> List[Dict[str, Any]]:
    """
        elements like:
            {
                "learning_rate": [0.01, 0.02],
                "max_iter": [1000, 2000, 3000]
            }
        returns:
            [
                {"leaning_rate", 0.01},
                {"leaning_rate", 0.02},
                {"max_iter", 1000},
                {"max_iter", 2000},
                {"max_iter", 3000}
            ]
    """
    # TODO Check unduplicate

    overrides = list()
    for k, values in elements.items():
        overrides.extend([{k:v} for v in values])
    return overrides


# Dose Dict need to be exchanged to OrderedDict?
def ordered_product(elements: Dict[str, List]) -> List[Dict[str, Any]]:
    """
        elements like:
            {
                "learning_rate": [0.01, 0.02],
                "max_iter": [1000, 2000, 3000]
            }
        returns:
            [
                {"leaning_rate", 0.01, "max_iter", 1000},
                {"leaning_rate", 0.01, "max_iter", 2000},
                {"leaning_rate", 0.01, "max_iter", 3000},
                {"leaning_rate", 0.02, "max_iter", 1000},
                {"leaning_rate", 0.02, "max_iter", 2000},
                {"leaning_rate", 0.02, "max_iter", 3000}
            ]
    """
    # TODO check unduplicate

    overrides = list()
    iter_list = list()
    for k, values in elements.items():
        iter_list.append([{k:v} for v in values])
    for pair_dicts in product(*iter_list):
        pair = dict()
        for d in pair_dicts:
            pair |= d
        overrides.append(pair)

    return overrides

def override_load(config_name: str, override: Dict[str, Any]) -> DictConfig:
    cfg = hydra.compose(config_name=config_name, overrides=[
        f"++{k}={v}" for k, v in override.items()
    ])
    return cfg

def main():
    conf_cfg_name = "conf"
    with hydra.initialize(config_path=CONF_DIR):
        conf_cfg = hydra.compose(config_name=conf_cfg_name)
        for experiment, confs in conf_cfg.experiments.items_ex():
            config_name = experiment
            for conf, elements in confs.items_ex():
                if conf == 'concatenate':
                    overrides = concatenate(elements)
                elif conf == 'product':
                    overrides = ordered_product(elements)
                for override in overrides:
                    cfg = override_load(config_name=config_name, override=override)
                    print(config_name, OmegaConf.to_yaml(cfg))
                    exit()

if __name__ == '__main__':
    main()


