#!/usr/bin/env python3

import curses
import time
import argparse
import json

from src.player import get_track
from src.lyrics import fetch_lyrics
from src.lrc import get_lrc
from src.config import load_config
from src.ui import draw, init
from src.ipc import send_state


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

                timestamps = get_lrc(artist, title, cfg.getboolean("lrc"))

                start = time.time()
                last = key

        now = time.time() - start

        current = -1
        display_lines = lines

        if timestamps:
            for i, (t, txt) in enumerate(timestamps):
                if now >= t:
                    current = i
            display_lines = [t[1] for t in timestamps]

        state = {
            "artist": artist,
            "title": title,
            "line": current
        }

        if args.json:
            print(json.dumps(state))
        else:
            draw(stdscr, artist, title, display_lines, current, cfg)

        if cfg.getboolean("ipc"):
            send_state(state)

        time.sleep(0.05)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    cfg = load_config()
    curses.wrapper(run, args, cfg)
