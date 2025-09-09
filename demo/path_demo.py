from pathlib import Path

this = Path(__file__).absolute()
print(this)
demo = Path(__file__).parent.absolute()
print(demo)
print(this.relative_to(demo))
print(this.resolve())
print(type(this))
print(str(this.relative_to(demo)))