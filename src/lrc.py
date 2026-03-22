import urllib.request
import urllib.parse
import json
import re
import os

BASE = os.path.expanduser("~/.cache/miracle/lrc")
os.makedirs(BASE, exist_ok=True)

def get_lrc(artist, title, enabled):
    if not enabled:
        return []

    fname = f"{artist}-{title}.lrc"
    path = os.path.join(BASE, fname)

    if not os.path.exists(path):
        try:
            q = urllib.parse.quote(f"{artist} {title}")
            url = f"https://lrclib.net/api/search?q={q}"

            with urllib.request.urlopen(url, timeout=5) as r:
                data = json.loads(r.read().decode())

                if data:
                    lrc = data[0].get("syncedLyrics")
                    if lrc:
                        with open(path, "w") as f:
                            f.write(lrc)
        except:
            return []

    return parse(path)

def parse(path):
    out = []

    with open(path, "r", errors="ignore") as f:
        for line in f:
            matches = re.findall(r"\[(\d+):(\d+\.\d+)\](.*)", line)

            for m, s, txt in matches:
                t = int(m) * 60 + float(s)
                txt = txt.strip()

                if txt:
                    out.append((t, txt))

    return sorted(out, key=lambda x: x[0])
