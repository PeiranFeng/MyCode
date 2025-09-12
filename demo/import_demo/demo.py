import module

module.a()
module.b()
print(hasattr(module, 'a'))
getattr(module, 'a')()