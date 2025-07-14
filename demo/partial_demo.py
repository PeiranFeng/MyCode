from functools import partial

def func(arg: int, multiplier: int) -> int:
    """A simple function that multiplies an integer by a multiplier."""
    return arg * multiplier

func_3 = partial(func, multiplier=3)
func_4 = partial(func, multiplier=4)

if __name__ == '__main__':
    print(func(5, 2))
    print(func_3(5))  # Output: 15
    print(func_4(5))  # Output: 20