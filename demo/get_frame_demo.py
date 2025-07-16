import sys

def f():
    g = 1
    l = 2
    frame = sys._getframe()
    for name in frame.__dict__():
        print(name, frame[name])

f()