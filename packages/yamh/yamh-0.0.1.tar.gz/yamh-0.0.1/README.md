# yamh
Yet Another Murmur3 Hash library

## Overview
Provides an interface to the murumurv3 hash library, but allows for streaming of
data with a similar interface to the python hashlib library, ie:
```python
m = yamh.murmur3_32()
m.update(b"Nobody inspects")
m.update(b" the spammish repetition")
m.digest()
```
