# rfc7748 (Elliptic Curves for Security)

A pure Python implemention of rfc7748.


Usage:

```python
# this code supports both python 2 and 3
from binascii import hexlify
from rfc7748 import x25519

private_key = b'1' * 32
public_key = x25519.scalar_base_mult(private_key)
print(hexlify(public_key))

peer_public_key = b'2' * 32
shared_secret = x25519.scalar_mult(private_key, peer_public_key)
print(hexlify(shared_secret))

'''output:
b'04f5f29162c31a8defa18e6e742224ee806fc1718a278be859ba5620402b8f3a'
b'a6d830c3561f210fc006c77768369af0f5b3e3e502e74bd3e80991d7cb7bfa50'
'''
```
