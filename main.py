#!/usr/bin/env python3

import curses
import time
import argparse
import json

from src.player import get_track
from src.lyrics import fetch_lyrics
from src.lrc import fetch_lrc, parse_lrc
from src.config import load_config
from src.ui import draw, init


def run(stdscr, args, cfg):
    curses.curs_set(0)
    stdscr.nodelay(True)
    init()

    last = ""
    lines = []
    timestamps = []

    start = time.time()

    while True:
        if stdscr.getch() == ord("q"):
            break

        artist, title = get_track()

        if artist and title:
            key = f"{artist}-{title}"

            if key != last:
                raw = fetch_lyrics(artist, title, cfg.getboolean("cache"))
                lines = raw.splitlines()

                if cfg.getboolean("lrc"):
                    path = fetch_lrc(artist, title)
                    if path:
                        timestamps = parse_lrc(path)
                    else:
                        timestamps = []

                start = time.time()
                last = key

        now = time.time() - start

        current = -1
        if timestamps:
            for i, (t, _) in enumerate(timestamps):
                if now >= t:
                    current = i
            lines = [t[1] for t in timestamps]

        if args.json:
            print(json.dumps({
                "artist": artist,
                "title": title,
                "line": current
            }))
        else:
            draw(stdscr, artist, title, lines, current, cfg["scroll_speed"])

        time.sleep(0.05)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    cfg = load_config()

    curses.wrapper(run, args, cfg)
