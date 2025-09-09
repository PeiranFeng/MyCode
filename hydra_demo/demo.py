from omegaconf import OmegaConf 
import hydra
from pathlib import Path
from hydra.core.global_hydra import GlobalHydra

experiments = ['brownian_motion', 'mean_reversion']

def dynamic_cfg_model():
    with hydra.initialize(config_path="conf", version_base=None):
        for exp in experiments:
            cfg = hydra.compose(overrides=[f"+experiments={exp}"])
            print(OmegaConf.to_yaml(cfg))
    
def save():
    with hydra.initialize(config_path="conf", version_base=None):
        cfg = hydra.compose(config_name="experiments\\brownian_motion", overrides=["++learn_rate=0.01"], return_hydra_config=True)
        print(OmegaConf.to_yaml(cfg))
        print(type(cfg))
        # OmegaConf.save(cfg, "C:\\brownian_motion_0.01.yaml")

from _loader_ import load

def inject_loader():
    with hydra.initialize(config_path="conf", version_base=None):
        cfg = hydra.compose(config_name="experiments/brownian_motion", overrides=[
            "+hydra.job.config.loader=my_loader", 
            "++learn_rate=0.01"
        ])
        print(OmegaConf.to_yaml(cfg))
        # OmegaConf.save(cfg, "C:\\brownian_motion_0.01.yaml")


if __name__ == '__main__':
    # dynamic_cfg_model()
    # save()
    inject_loader()