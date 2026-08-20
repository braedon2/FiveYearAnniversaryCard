import curses 
import locale
import random
import time

TARGET_WIDTH = 80
TARGET_HEIGHT = 25

strs = ["HAPPY ", "FIVE ", "YEAR ", "ANNIVERSARY ", "!!!"]
message = ''.join(strs)
num_chars = len(message)
message_row = TARGET_HEIGHT // 2
message_col = (TARGET_WIDTH - num_chars) // 2

end_cols = [] # the column where each string will end up after its animation
for i, s in enumerate(strs):
    if i == 0:
        end_cols.append(message_col)
    else:
        end_cols.append(end_cols[i-1] + len(strs[i-1]))

starts = [] # tuples of row column pairs
for i, c in enumerate(end_cols):
    if i % 2 == 0:
        starts.append(
            (0, c-message_row))
    else:
        d = TARGET_HEIGHT - 1 - message_row 
        starts.append(
            (TARGET_HEIGHT-1, c-d)) 

def main(stdscr):
    locale.setlocale(locale.LC_ALL, '')
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    stdscr.clear()

    height, width = stdscr.getmaxyx()

    if height != TARGET_HEIGHT or width != TARGET_WIDTH:
        while height != TARGET_HEIGHT or width != TARGET_WIDTH:
            stdscr.clear()
            stdscr.addstr(0, 0, "first things first!")
            if height < TARGET_HEIGHT:
                stdscr.addstr(1, 0, f"increase window size vertically until it's {TARGET_HEIGHT} (currently {height})")
            elif height > TARGET_HEIGHT:
                stdscr.addstr(1, 0, f"decrease window size vertically until it's {TARGET_HEIGHT} (currently {height})")

            if width < TARGET_WIDTH:
                stdscr.addstr(2, 0, f"increase window size horizontally until it's {TARGET_WIDTH} (currently {width})")
            elif width > TARGET_WIDTH:
                stdscr.addstr(2, 0, f"decrease window size horizontally until it's {TARGET_WIDTH} (currently {width})")
            stdscr.getch()
            height, width = stdscr.getmaxyx()
        stdscr.clear()
        stdscr.getch()
        stdscr.addstr(0, 0, "all done! press any key to see your card")
        stdscr.getch()

    stdscr.clear()
    for i, s in enumerate(strs):
        animate_message_str(stdscr, s, starts[i], end_cols[i])
    time.sleep(0.5)

    points = []
    while True:
        points = randomized_heart_points(5, points)
        draw_hearts(stdscr, points)
        stdscr.refresh()
        time.sleep(1)
        erase_hearts(stdscr, points)
        stdscr.refresh()
    stdscr.getch()


def animate_message_str(stdscr, s, start, end_col):
    r, c = start 
    points_to_print = []
    
    while c <= end_col:
        points_to_print.append((r, c))
        r += 1 if start[0] < message_row else -1
        c += 1

        for p in points_to_print:
            stdscr.addstr(p[0], p[1], s)
            stdscr.refresh()
        time.sleep(0.05)

    while len(points_to_print) > 1:
        p = points_to_print.pop(0)
        stdscr.addstr(p[0], p[1], ' ' * len(s))
        stdscr.refresh()
        time.sleep(0.05)

def randomized_heart_points(num_hearts, prev_points):
    point_space = []
    for r in range(TARGET_HEIGHT):
        for c in range(TARGET_WIDTH):
            if (r, c) in prev_points or (r == message_row and message_col <= c < message_col + num_chars):
                continue
            point_space.append((r, c))
    return random.sample(point_space, num_hearts)

def draw_hearts(stdscr, points):
    for p in points:
        stdscr.addstr(p[0], p[1], "♥")

def erase_hearts(stdscr, points):
    for p in points:
        stdscr.addstr(p[0], p[1], " ")

curses.wrapper(main)

