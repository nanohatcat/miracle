import os
import hashlib

BASE = os.path.expanduser("~/.cache/miracle")
os.makedirs(BASE, exist_ok=True)

def key(artist, title):
    return hashlib.md5(f"{artist}-{title}".encode()).hexdigest()

def get(artist, title):
    path = os.path.join(BASE, key(artist, title))
    if os.path.exists(path):
        with open(path) as f:
            return f.read()
    return None

def set_cache(artist, title, data):
    path = os.path.join(BASE, key(artist, title))
    with open(path, "w") as f:
        f.write(data)
