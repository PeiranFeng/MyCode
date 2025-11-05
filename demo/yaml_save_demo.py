import yaml
from pathlib import Path

with open(Path(__file__).parent/'yaml_save_demo.yaml', '+w') as f:
    yaml.dump([1,2,3], f)