import curses

_colors = False
offset = 0.0

def init():
    global _colors
    if curses.has_colors():
        curses.start_color()
        curses.use_default_colors()
        try:
            curses.init_pair(1, curses.COLOR_CYAN, -1)
            curses.init_pair(2, curses.COLOR_YELLOW, -1)
            curses.init_pair(3, curses.COLOR_WHITE, -1)
            _colors = True
        except:
            pass

def draw(stdscr, artist, title, lines, current, speed):
    global offset

    stdscr.erase()
    h, w = stdscr.getmaxyx()

    header = f"{artist or ''} - {title or ''}"
    x = max(0, (w//2 - len(header)//2))

    stdscr.addnstr(0, x, header, w-1, curses.A_BOLD | (curses.color_pair(1) if _colors else 0))

    target = max(0, current - h//2)
    offset += (target - offset) * float(speed)
    off = int(offset)

    for i, line in enumerate(lines[off:off+h-2]):
        idx = i + off
        attr = curses.color_pair(3) if _colors else curses.A_NORMAL

        if idx == current:
            attr = (curses.color_pair(2) if _colors else curses.A_REVERSE) | curses.A_BOLD

        stdscr.addnstr(i+2, 0, line, w-1, attr)

    stdscr.refresh()
