#!/usr/bin/env python3
from tracemalloc import start
import rough_rogue
import curses
from curses import KEY_DOWN, KEY_UP, KEY_LEFT, KEY_RIGHT
HEIGHT = 20
WIDTH = 160
# window = curses.initscr()


sc = curses.initscr()
h, w = sc.getmaxyx()

my_dungeon = rough_rogue.dungeon(width=64,height=32) # initialise empty dungeon
steve = rough_rogue.creature(chr='@',x_pos=10,y_pos=5)
# my_screen = rough_rogue.screen(30,15,'.',steve,bck='.',hx=7,hy=7)
my_screen = rough_rogue.screen(80,80,'.',steve,bck='.',hx=7,hy=7)

my_dungeon.new() # fill with rooms and corridors (separated from __init__ because the idea is to prepare different set of functions for different dungeon generation algorithms)

# spawn player at random position
start_pos = rough_rogue.random_spawn(dungeon=my_dungeon.dungeon, floor_tile='.')
steve.dx = start_pos[0]
steve.dy = start_pos[1]


my_dungeon.dungeon[steve.dy][steve.dx] = 'X'

while True:
    # my_screen.test_draw(rms=my_dungeon.rooms_list, dungeon=my_dungeon.dungeon)
    my_screen.static_draw(rms=my_dungeon.rooms_list, dungeon=my_dungeon.dungeon)
    my_screen.win.refresh()
    cmd = my_screen.win.getch()
    if cmd == ord('q'): break
    elif cmd == curses.KEY_LEFT:
        if my_screen.area[steve.dy][steve.dx-1]=='.':
            steve.move('left')
    elif cmd == curses.KEY_RIGHT:
        if my_screen.area[steve.dy][steve.dx+1]=='.':
            steve.move('right')
    elif cmd == curses.KEY_UP:
        if my_screen.area[steve.dy-1][steve.dx]=='.':
            steve.move('up')
    elif cmd == curses.KEY_DOWN:
        if my_screen.area[steve.dy+1][steve.dx]=='.':
            steve.move('down')
curses.endwin()
print('BYE!')
