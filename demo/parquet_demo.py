import pandas as pd
from pathlib import Path

p = Path(__file__).parent / "test_seed-00.parquet"
# 读取 Parquet 文件
df = pd.read_parquet(p.absolute())

# 显示前 5 行
print(df.head())

# 打印基本信息
print(df.info())