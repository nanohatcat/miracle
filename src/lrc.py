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
    events = []

    time_pattern = re.compile(r"\[(\d+):(\d+\.\d+)\]")

    with open(path, "r", errors="ignore") as f:
        for line in f:
            times = time_pattern.findall(line)
            if not times:
                continue

            # remove timestamps → keep pure lyric text
            text = time_pattern.sub("", line).strip()

            # ignore empty lyric lines
            if not text:
                continue

            # expand multi-timestamp lines
            for m, s in times:
                t = int(m) * 60 + float(s)
                events.append((t, text))

    # sort + deduplicate exact duplicates
    events.sort(key=lambda x: x[0])

    deduped = []
    last = None

    for e in events:
        if e != last:
            deduped.append(e)
            last = e

    return deduped
