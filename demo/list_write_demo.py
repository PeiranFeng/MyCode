from pathlib import Path

Path.mkdir(Path.cwd()/'demo'/'conf', exist_ok=True)
with open(Path.cwd()/'demo'/'conf'/'empty.yaml', "+w") as f:
    f.write('\n'.join(['1','2','3']))
with open(Path.cwd()/'demo'/'conf'/'empty.yaml', "r") as f:
    print([_.strip() for _ in f.readlines()])