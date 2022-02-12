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
my_screen = rough_rogue.screen(30,15,'.',steve,bck='.',hx=7,hy=7)
# my_screen = rough_rogue.screen(80,80,'.',steve,bck='.',hx=7,hy=7)

my_dungeon.new() # fill with rooms and corridors (separated from __init__ because the idea is to prepare different set of functions for different dungeon generation algorithms)

# spawn player at random position
start_pos = rough_rogue.random_spawn(dungeon=my_dungeon.dungeon, floor_tile='.')
steve.dx = start_pos[0]
steve.dy = start_pos[1]


# my_dungeon.dungeon[steve.dy][steve.dx] = 'X'
my_monsters = rough_rogue.monster(dungeon=my_dungeon.dungeon,floor_tile='.',wall_tile='#')
my_monsters.set_targets()

while True:
    my_screen.viewport_draw(rms=my_dungeon.rooms_list, dungeon=my_dungeon.dungeon,monsters=my_monsters.all_monsters)
    # my_screen.static_draw(rms=my_dungeon.rooms_list, dungeon=my_dungeon.dungeon)
    my_screen.win.refresh()
    cmd = my_screen.win.getch()
    if cmd == ord('q'): break
    elif cmd == curses.KEY_LEFT:
        if my_screen.area[my_screen.hy][my_screen.hx-1]=='.':
            steve.move('left')
    elif cmd == curses.KEY_RIGHT:
        if my_screen.area[my_screen.hy][my_screen.hx+1]=='.':
            steve.move('right')
    elif cmd == curses.KEY_UP:
        if my_screen.area[my_screen.hy-1][my_screen.hx]=='.':
            steve.move('up')
    elif cmd == curses.KEY_DOWN:
        if my_screen.area[my_screen.hy+1][my_screen.hx]=='.':
            steve.move('down')
    # make monsters walking
    for monster in my_monsters.all_monsters:
        if len(monster['path'])>0:
            next_field = monster['path'][0]
            monster['pos_y'] = next_field[0]
            monster['pos_x'] = next_field[1]
            next_field = []
            monster['path'].pop(0)
        else:
            my_monsters.set_target_for_single_monster(monster)
curses.endwin()
print('BYE!')
