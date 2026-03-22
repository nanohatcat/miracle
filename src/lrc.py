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
                        open(path, "w").write(lrc)
        except:
            return []

    return parse(path)


def parse(path):
    out = []
    for line in open(path):
        m = re.match(r"\[(\d+):(\d+\.\d+)\](.*)", line)
        if m:
            m_, s_, txt = m.groups()
            t = int(m_) * 60 + float(s_)
            out.append((t, txt.strip()))
    return sorted(out)
