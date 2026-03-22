import urllib.request
import urllib.parse
import json
import re
import os

CACHE = os.path.expanduser("~/.cache/miracle/lrc")
os.makedirs(CACHE, exist_ok=True)

def fetch_lrc(artist, title):
    try:
        q = urllib.parse.quote(f"{artist} {title}")
        url = f"https://lrclib.net/api/search?q={q}"

        with urllib.request.urlopen(url, timeout=5) as r:
            data = json.loads(r.read().decode())

            if data:
                lrc = data[0].get("syncedLyrics")
                if lrc:
                    path = os.path.join(CACHE, f"{artist}-{title}.lrc")
                    with open(path, "w") as f:
                        f.write(lrc)
                    return path
    except:
        pass

    return None

def parse_lrc(path):
    out = []
    with open(path) as f:
        for line in f:
            m = re.match(r"\[(\d+):(\d+\.\d+)\](.*)", line)
            if m:
                m_, s_, txt = m.groups()
                t = int(m_) * 60 + float(s_)
                out.append((t, txt.strip()))
    return sorted(out, key=lambda x: x[0])
