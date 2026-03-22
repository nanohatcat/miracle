import os
import hashlib

BASE = os.path.expanduser("~/.cache/miracle")
os.makedirs(BASE, exist_ok=True)

def _path(key):
    return os.path.join(BASE, key)

def make_key(a, t):
    return hashlib.md5(f"{a}-{t}".encode()).hexdigest()

def get(a, t):
    p = _path(make_key(a, t))
    if os.path.exists(p):
        return open(p).read()
    return None

def set_cache(a, t, data):
    open(_path(make_key(a, t)), "w").write(data)
