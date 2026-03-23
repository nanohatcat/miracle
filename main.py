#!/usr/bin/env python3

import curses
import time
import argparse

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

    last_key = None
    last_pos = 0

    lines = []
    timestamps = []
    has_lrc = False

    while True:
        if stdscr.getch() == ord("q"):
            break

        artist, title, pos, duration = get_track()

        key = f"{artist}-{title}-{int(duration)}"

        track_changed = (
            key != last_key or
            (pos < last_pos - 1)
        )

        if artist and title and track_changed:
            raw = fetch_lyrics(artist, title, cfg.getboolean("cache"))
            lines = raw.splitlines()

            timestamps = get_lrc(artist, title, cfg.getboolean("lrc"))
            has_lrc = bool(timestamps)

            last_key = key

        last_pos = pos

        if has_lrc:
            current = 0
            for i, (t, _) in enumerate(timestamps):
                if pos >= t:
                    current = i
                else:
                    break

            display_lines = [txt for _, txt in timestamps]
        else:
            current = -1  # disables highlight
            display_lines = lines if lines else ["no lyrics found"]

        draw(
            stdscr,
            artist,
            title,
            display_lines,
            current,
            cfg,
            pos,
            duration,
            has_lrc
        )

        if cfg.getboolean("ipc"):
            send_state({
                "artist": artist,
                "title": title,
                "line": current
            })

        time.sleep(0.1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    cfg = load_config()
    curses.wrapper(run, args, cfg)
