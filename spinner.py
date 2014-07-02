"""
<description>
"""

import subprocess
import math
import curses
import time
import cProfile


def get_term_size():
    height = int(subprocess.check_output(["tput", "lines"]))
    width = int(subprocess.check_output(["tput", "cols"]))
    return height, width


def test_screen(bar_width=6, num_bars=3):
    lines, cols = get_term_size()
    bar_str = "=" + "#" * bar_width + "=" + " "* bar_width
    screen = [c*cols for c in bar_str * num_bars]
    return screen


def test(term, duration=4, speed=60):
    decay = speed / duration

    term_h, term_w = get_term_size()
    curses.curs_set(0)
    term.clear()
    term.touchwin()
    term.refresh()
    curses.doupdate()

    screen = test_screen()
    lines = []
    while len(lines) < term_h:
        lines += screen
    num_lines = len(lines)
    lines *= 2
    top = 0
    t_after = time.time()
    while speed > 0:
        t_before = t_after

        i_top = int(top) % num_lines
        i_bot = i_top + term_h - 1
        vis = lines[i_top:i_bot]

        for y, line in enumerate(vis):
            term.addstr(y, 0, line)

        term.addstr(math.floor(term_h/2), term_w-2, "<=", curses.A_BOLD)
        term.refresh()

        t_after = time.time()
        delta_t = t_after - t_before

        top += speed * delta_t
        speed -= decay * delta_t

    time.sleep(1)
    return 1

winner = None
cProfile.run("winner = curses.wrapper(test)")
print(winner)