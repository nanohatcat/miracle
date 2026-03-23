import urllib.request
import urllib.parse
import json
import re
from .cache import get, set_cache
from .fuzzy import normalize


def fetch_lyrics(artist, title, use_cache=True):
    cache_artist = normalize(artist or "")
    cache_title = normalize(title or "")

    if use_cache:
        c = get(cache_artist, cache_title)
        if c:
            return c

    def request(a, t):
        url = f"https://api.lyrics.ovh/v1/{a}/{t}"
        with urllib.request.urlopen(url, timeout=5) as r:
            data = json.loads(r.read().decode())
            return data.get("lyrics")

    def try_fetch(a_raw, t_raw):
        try:
            a = urllib.parse.quote(a_raw, safe="")
            t = urllib.parse.quote(t_raw, safe="")
            return request(a, t)
        except Exception:
            return None

    # build candidate titles
    candidates = []

    # original
    candidates.append(title)

    # split on "/"
    if "/" in title:
        parts = [p.strip() for p in title.split("/") if p.strip()]
        candidates.extend(parts)

    # split on "-"
    if "-" in title:
        parts = [p.strip() for p in title.split("-") if p.strip()]
        candidates.extend(parts)

    # remove parentheses
    cleaned = re.sub(r"\(.*?\)|\[.*?\]", "", title).strip()
    if cleaned and cleaned != title:
        candidates.append(cleaned)

    # normalized fallback
    candidates.append(cache_title)

    # remove duplicates while preserving order
    seen = set()
    unique_candidates = []
    for c in candidates:
        if c and c not in seen:
            seen.add(c)
            unique_candidates.append(c)

    # try all candidates
    for t in unique_candidates:
        lyrics = try_fetch(artist, t)
        if lyrics:
            if use_cache:
                set_cache(cache_artist, cache_title, lyrics)
            return lyrics

    return "no lyrics found"
