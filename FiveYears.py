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
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    curses.start_color()

    colors = [] # stores the curses color pairs used to print each word
    for i, color_constant in enumerate(COLOR_CONSTANTS):
        curses.init_pair(i+1, color_constant, curses.COLOR_BLACK)
        colors.append(curses.color_pair(i+1))

    # the default color pair for printing, white on black
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)
    stdscr.bkgd(' ', curses.color_pair(6))

    curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK)
    heart_color = curses.color_pair(7)

    prompt_to_resize(stdscr)

    stdscr.clear()
    for i, s in enumerate(STRS):
        animate_message_str(stdscr, s, STARTS[i], END_COLS[i], colors[i])
    time.sleep(0.5)

    points = []
    while points := randomized_heart_points(5, points):
        for p in points:
            stdscr.addstr(p[0], p[1], "♥", heart_color)
        stdscr.refresh()
        time.sleep(0.5)
        for p in points:
                stdscr.addstr(p[0], p[1], " ")
        stdscr.refresh()


# prompts user (my partner) to resize the terminal until it is the target size
def prompt_to_resize(stdscr):
    while (maxyx := stdscr.getmaxyx()) != (TARGET_HEIGHT, TARGET_WIDTH):
        height, width = maxyx
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

            # pressing any key here will break out of the parent loop and start the animation unless the "keypress"
            # is actually a window resize whereby it will re-enter the window resize prompt flow
            while True:
                ch = stdscr.getch()
                if ch == curses.KEY_RESIZE:
                    break
                else:
                    break


def animate_message_str(stdscr, s, start, end_col, color):
    start_row, start_col = start 
    print_points = list(zip(
        range(start_row, MESSAGE_ROW+1) if start_row < MESSAGE_ROW else range(start_row, MESSAGE_ROW-1, -1),
        range(start_col, end_col+1)))
    
    for row, col in print_points:
        stdscr.addstr(row, col, s, color)
        stdscr.refresh()
        time.sleep(0.05)

    for row, col in print_points[:-1]: # keep the last point as that forms the final message
        stdscr.addstr(row, col, ' ' * len(s))
        stdscr.refresh()
        time.sleep(0.05)


def randomized_heart_points(num_hearts, prev_points):
    point_space = [
        (r, c) for r in range(TARGET_HEIGHT-1) for c in range(TARGET_WIDTH-1)
        if (r, c) not in prev_points and not (r == MESSAGE_ROW and MESSAGE_COL <= c < MESSAGE_COL + NUM_CHARS)
    ]
    return random.sample(point_space, num_hearts)

curses.wrapper(main)
 
