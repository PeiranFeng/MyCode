def f():
    for t in [(1,2), (3,4)]:
        yield t

if __name__ == '__main__':
    for i, (a, b) in enumerate(f()):
        print(i,a,b)