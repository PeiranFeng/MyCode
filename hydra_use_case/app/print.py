import hydra
import os
from omegaconf import DictConfig, OmegaConf, ListConfig
from pathlib import Path, WindowsPath
from typing import List, Tuple, Dict, Any, Optional
from itertools import product
from pathlib import Path
from hydra.core.hydra_config import HydraConfig
from functools import singledispatch
# from myConfPath import MyConfPath

JOD_ID = 0
CONF_DIR = '../conf'
PARENT_PATH = Path(__file__).parent
CONFIG_ENV_VAR = "CONFIGURE_PATH"
DEFAULT_CONFIG_DIR = "conf"

def print_linear(*args):
    return [*args]

def file(file_path):
    return PARENT_PATH/"conf"/file_path

def tuple_resolver(*args):
    return tuple(args)

def path_resolver(file_name, config_name):
    config_base_path = os.getenv(CONFIG_ENV_VAR, DEFAULT_CONFIG_DIR)
    config_name = Path.cwd() / config_base_path / config_name
    file_name = Path(file_name)
    if not Path.is_absolute(file_name):
        file_name = config_name / '../' / file_name
    return file_name.resolve()

def get_path(config_name, file_name):
    config_name = Path(__file__).resolve() / Path('../'+CONF_DIR) / config_name
    file_name = Path(file_name)
    if not Path.is_absolute(file_name):
        file_name = config_name / '../' / file_name
    return file_name.resolve()

OmegaConf.register_new_resolver('linear', print_linear)
OmegaConf.register_new_resolver('file', file)
OmegaConf.register_new_resolver('tuple', tuple_resolver)
OmegaConf.register_new_resolver('path', path_resolver)

@singledispatch
def instantiat_configuration(cfg):
    return cfg

from hydra.utils import instantiate
@instantiat_configuration.register
def _(cfg: DictConfig):
    if '_target_' in cfg.keys():
        return instantiate(cfg)
    else:
        return {k:instantiat_configuration(v) for k,v in cfg.items_ex()}

@instantiat_configuration.register
def _(cfg_list: Optional[list|ListConfig]):
    return [instantiat_configuration(_) for _ in cfg_list]


def main():
    conf_cfg_name = "conf"
    with hydra.initialize(config_path=CONF_DIR):
        config_name = 'config'
        cfg = hydra.compose(config_name, overrides=["++file_relative_path=../schema/override.yaml"])
        print(OmegaConf.to_object(cfg))
        OmegaConf.save(cfg, Path.cwd()/'hydra_use_case'/'conf'/'overrides.yaml')



if __name__ == '__main__':
    main()
    # a()