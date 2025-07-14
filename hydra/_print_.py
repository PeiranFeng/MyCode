import hydra
from omegaconf import DictConfig, OmegaConf

def train(
  model: str,
  n_epoches: int,
  lr: float,
  batch_size: int      
):
    print("Start training...")
    print(f"Model: {model}, \nEpochs: {n_epoches}, \nLearning Rate: {lr}, \nBatch Size: {batch_size}")

@hydra.main(version_base=None, config_path="conf", config_name="conf")
def my_app(cfg: DictConfig) -> None:
    """
    Read parameters from the configuration by hydra
    Parameters can be accessed by omegaconf.DictConfig
    """
    # print(OmegaConf.to_yaml(cfg))

    model_name = cfg.train_setting.model
    n_epoches = cfg.train_setting.n_epoches

    lr: float = cfg['train_setting']['lr']
    batch_size: int = cfg["train_setting"]['batch_size']

    train(
        model=model_name,
        n_epoches=n_epoches,
        lr=lr,
        batch_size=batch_size
    )

if __name__ == "__main__":
    my_app()