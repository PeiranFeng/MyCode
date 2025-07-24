__all__ = ['generator']

import torch
from random import random
import math

def generator(num_samples: int, p: float):
    assert p>0 and p<1, 'p should be in (0, 1) range'

    for _ in range(num_samples):
        yield 1 if random() < p else 0

if __name__ == '__main__':
    data = generator(10000, 0.6)
    win = 0
    loss = 0
    for turn in data:
        if turn:
            win += 1
        else:
            loss += 1
    print('pred p',win/(win+loss))