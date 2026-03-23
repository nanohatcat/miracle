import curses

colors = False


def init():
    global colors
    if curses.has_colors():
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_CYAN, -1)
        curses.init_pair(2, curses.COLOR_YELLOW, -1)
        curses.init_pair(3, curses.COLOR_WHITE, -1)
        curses.init_pair(4, curses.COLOR_RED, -1)
        colors = True


def progress_bar(w, pos, duration):
    if duration <= 0:
        return ""

    ratio = max(0.0, min(1.0, pos / duration))
    fill = int(ratio * (w - 2))

    return "[" + ("#" * fill).ljust(w - 2) + "]"


def draw(stdscr, artist, title, lines, current, cfg, pos, duration, has_lrc):
    stdscr.erase()
    h, w = stdscr.getmaxyx()

    header = f"{artist or ''} - {title or ''}"
    stdscr.addnstr(
        0,
        max(0, (w // 2 - len(header) // 2)),
        header,
        w - 1,
        curses.A_BOLD | (curses.color_pair(1) if colors else 0),
    )

    bar = progress_bar(w, pos, duration)
    stdscr.addnstr(1, 0, bar, w - 1)

    if not lines:
        stdscr.refresh()
        return

    window_height = h - 3

    # when no lrc: no highlight, just plain lyrics
    if not has_lrc:
        start = 0
    else:
        half = window_height // 2
        start = max(0, current - half)

    view = lines[start:start + window_height]

    for i, line in enumerate(view):
        idx = start + i
        y = i + 2
        x = max(0, (w // 2 - len(line) // 2))

        if has_lrc:
            if colors:
                if idx == current:
                    attr = curses.color_pair(2) | curses.A_BOLD
                else:
                    attr = curses.color_pair(3)
            else:
                attr = curses.A_REVERSE if idx == current else curses.A_NORMAL
        else:
            # plain rendering (dimmed slightly if colors exist)
            attr = curses.color_pair(3) if colors else curses.A_NORMAL

        stdscr.addnstr(y, x, line, w - 1, attr)

    # overlay error message when no lrc
    if not has_lrc:
        msg = "no synced lyrics (lrc) found"
        y = h // 2
        x = max(0, (w // 2 - len(msg) // 2))

        attr = curses.color_pair(4) | curses.A_BOLD if colors else curses.A_BOLD
        stdscr.addnstr(y, x, msg, w - 1, attr)

    stdscr.refresh()
