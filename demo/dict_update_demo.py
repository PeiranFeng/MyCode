a = dict()
for _ in ['one', [2,3,4]]:
    a.update({_:_} if isinstance(_, str) else _)
for k, v in a.items():
    print(k, v)