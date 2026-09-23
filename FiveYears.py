import curses 
import locale
import random
import time

# a small fixed size looks best
TARGET_WIDTH = 80
TARGET_HEIGHT = 25
# its convenient to have the separated strings and the whole message in their own variables
STRS = ["HAPPY ", "FIVE ", "YEAR ", "ANNIVERSARY ", "!!!"]
MESSAGE = ''.join(STRS)
NUM_CHARS = len(MESSAGE)
# each word has its own color. more configuration is needed when we have our curses screen object
COLOR_CONSTANTS = [curses.COLOR_BLUE, curses.COLOR_CYAN, curses.COLOR_GREEN, curses.COLOR_MAGENTA, curses.COLOR_YELLOW]
# where the final message is printed after each word has been animated
MESSAGE_ROW = TARGET_HEIGHT // 2
MESSAGE_COL = (TARGET_WIDTH - NUM_CHARS) // 2
# the column where each string will end up after its animation
END_COLS = [24, 30, 35, 40, 52] 
# tuples of row column pairs for where each string starts its animation
STARTS = [(0, 12), (24, 18), (0, 23), (24, 28), (0, 40)] 

def main(stdscr):
    locale.setlocale(locale.LC_ALL, '')
    curses.start_color()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    stdscr.clear()

    colors = []
    for i, c in enumerate(COLOR_CONSTANTS):
        curses.init_pair(i+1, c, curses.COLOR_BLACK)
        colors.append(curses.color_pair(i+1))

    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)
    stdscr.bkgd(' ', curses.color_pair(6))

    curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK)
    heart_color = curses.color_pair(7)

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

            if height == TARGET_HEIGHT and width == TARGET_WIDTH:
                stdscr.clear()
                stdscr.addstr(0, 0, "all done! press any key to see your card")
        
                while True:
                    ch = stdscr.getch()
                    if ch == curses.KEY_RESIZE:
                        height, width = stdscr.getmaxyx()
                        break
                    else:
                        break

    stdscr.clear()
    for i, s in enumerate(STRS):
        animate_message_str(stdscr, s, STARTS[i], END_COLS[i], colors[i])
    time.sleep(0.5)

    points = []
    while True:
        points = randomized_heart_points(5, points)
        draw_hearts(stdscr, points, heart_color)
        stdscr.refresh()
        time.sleep(0.5)
        erase_hearts(stdscr, points)
        stdscr.refresh()


def animate_message_str(stdscr, s, start, end_col, color):
    r, c = start 
    points_to_print = []
    
    while c <= end_col:
        points_to_print.append((r, c))
        r += 1 if start[0] < MESSAGE_ROW else -1
        c += 1

        for p in points_to_print:
            stdscr.addstr(p[0], p[1], s, color)
            stdscr.refresh()
        time.sleep(0.05)

    while len(points_to_print) > 1:
        p = points_to_print.pop(0)
        stdscr.addstr(p[0], p[1], ' ' * len(s))
        stdscr.refresh()
        time.sleep(0.05)

def randomized_heart_points(num_hearts, prev_points):
    point_space = []
    for r in range(TARGET_HEIGHT-1):
        for c in range(TARGET_WIDTH-1):
            if (r, c) in prev_points or (r == MESSAGE_ROW and MESSAGE_COL <= c < MESSAGE_COL + NUM_CHARS):
                continue
            point_space.append((r, c))
    return random.sample(point_space, num_hearts)

def draw_hearts(stdscr, points, color):
    for p in points:
        stdscr.addstr(p[0], p[1], "♥", color)


def erase_hearts(stdscr, points):
    for p in points:
        stdscr.addstr(p[0], p[1], " ")

curses.wrapper(main)
 
