def f(a, b, *, c=1):
    print(a,b,c)

# f(1,2,3) TypeError: f() takes 2 positional arguments but 3 were given
f(1,2,c=3)