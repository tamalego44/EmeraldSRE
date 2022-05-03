#!/usr/bin/env python

import curses
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)

import curses

def main(stdscr):

    stdscr.clear()
    stdscr.scrollok(True)

    # Display 10 numbered lines:
    for line in range(10):
        stdscr.addstr(line, 0, str(line))

    stdscr.getch()  # Wait for a key press

    # Scrolling:
    stdscr.setscrreg(0, 9)  # Set scrolling region
    for _ in range(5):
        stdscr.scroll()  # Fails!
        stdscr.getch()

curses.wrapper(main)

#Window
# begin_x = 20; begin_y = 7
# height = 5; width = 40
# win = curses.newwin(height, width, begin_y, begin_x)

#Pad
pad = curses.newpad(100, 100)
# These loops fill the pad with letters; addch() is
# explained in the next section
for y in range(0, 99):
    for x in range(0, 99):
        if x % 2 == 1:
            pad.addch(y,x, ord(' '))
        else:
            pad.addch(y,x, ord('a') + (x*x+y*y) % 26)

pad2 = curses.newpad(100, 100)
# These loops fill the pad with letters; addch() is
# explained in the next section
for y in range(0, 99):
    for x in range(0, 99):
        pad2.addch(y,x, ord('0') + (x*x+y*y) % 10)

# Displays a section of the pad in the middle of the screen.
# (0,0) : coordinate of upper-left corner of pad area to display.
# (5,5) : coordinate of upper-left corner of window area to be filled
#         with pad content.
# (20, 75) : coordinate of lower-right corner of window area to be
#          : filled with pad content.
pad.refresh( 0,0, 5,5, 20,20)
pad2.refresh( 0,0, 5,25, 20, 40,)

running = True
x=y=0
while running:
    key = stdscr.getkey()
    
    if key == 'd':
        running = False
    elif key == "KEY_UP":
        y = max(0, y-1)
    elif key == "KEY_LEFT":
        x  = max(0, x-1)
    elif key == "KEY_DOWN":
        y += 1
    elif key == "KEY_RIGHT":
        x += 1
    else:
        stdscr.addstr(0,0,key)
    stdscr.noutrefresh()
    pad.noutrefresh(y,x, 5,5, 20,20)
    pad2.noutrefresh(y,x, 5,25, 20, 40)
    
    curses.doupdate()

stdscr.addstr(0, 0, "testing, testijng", curses.A_BLINK)

curses.start_color()
curses.use_default_colors()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
stdscr.addstr( "Pretty text", curses.color_pair(1) )

print(stdscr.getkey())
print(curses.has_colors())
print("\033[7mReversed\033[m Normal")

curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()

"""
from curses import wrapper

def main(stdscr):
    # Clear screen
    stdscr.clear()

    # This raises ZeroDivisionError when i == 10.
    for i in range(0, 11):
        v = i-10
        stdscr.addstr(i, 0, '10 divided by {} is {}'.format(v, 10/v))

    stdscr.refresh()
    stdscr.getkey()

wrapper(main)
"""