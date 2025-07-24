import hashlib

hasher = hashlib.sha3_224()
hasher.update('123'.encode('utf-8'))
print(hasher.hexdigest())