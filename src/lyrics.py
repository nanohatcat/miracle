import urllib.request
import urllib.parse
import json
from .cache import get, set_cache
from .fuzzy import normalize


def fetch_lyrics(artist, title, use_cache=True):
    if use_cache:
        c = get(artist, title)
        if c:
            return c

    try:
        a = urllib.parse.quote(artist)
        t = urllib.parse.quote(normalize(title))

        url = f"https://api.lyrics.ovh/v1/{a}/{t}"

        with urllib.request.urlopen(url, timeout=5) as r:
            data = json.loads(r.read().decode())
            lyrics = data.get("lyrics")

            if lyrics:
                if use_cache:
                    set_cache(artist, title, lyrics)
                return lyrics
    except:
        pass

    return "no lyrics found"
