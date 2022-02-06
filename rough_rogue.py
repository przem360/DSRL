import curses
import random

from numpy import empty, empty_like

def pick_random_room(room_list):
    r = random.randint(0,len(room_list)-1)
    room = room_list[r]
    return room

def random_spawn(dungeon, floor_tile):
    rx = random.randint(0,len(dungeon[0])-1)
    ry = random.randint(0,len(dungeon)-1)
    while dungeon[ry][rx] != floor_tile:
        print('picked tile: '+str(dungeon[ry][rx]))
        rx = random.randint(0,len(dungeon[0])-1)
        ry = random.randint(0,len(dungeon)-1)
    return [rx,ry]

class dungeon():
    def __init__(self,width=64,height=64,min_room_size=5,ch_bck=' ',ch_floor='.',ch_wall='#', blocks=3,horisontal_corridors=3):
        self.width = width
        self.height = height
        self.min_room_size = min_room_size
        self.dungeon = []
        self.h_corridors = horisontal_corridors
        self.rooms_list = []
        self.corridor_list = []
        self.ch_bck = ch_bck
        self.ch_floor = ch_floor
        self.ch_wall = ch_wall
        self.height_available = height
        self.blocks = blocks
        self.max_x_room = 0
        self.max_x_corr = 0
    def gen_room(self,min_size,max_width,max_height,y_pos,max_x):
        the_room = {'type':'room','x':0,'y':0,'middle':[],'width':0,'height':0}
        x, y, w, h = 0, 0, 0, 0
        w = random.randint(self.min_room_size, max_width)
        h = random.randint(self.min_room_size, max_height)
        x = max_width - w # this s not enough to be sure that new room will connect with previous corridor MAX_X should ensure this
        prev_x = x
        if x > self.max_x_room-1:
            x = self.max_x_room-1
            if x < 0: x = 2
        y = y_pos
        the_room['x'] = x
        the_room['y'] = y
        the_room['width'] = w
        the_room['height'] = h
        the_room['middle'] = [(x+(w//2)),(y+(h//2))]
        self.height_available = self.height_available - h
        self.max_x_corr = x + w
        return the_room
    def gen_v_corridor(self,y_pos,min_height,max_height,prev_room_x,prev_room_width):
        if prev_room_width == 0:
            prev_room_width = self.width // self.blocks
        the_corridor = {'type':'vcorr','x':0,'y':0,'height':0}
        min_x = prev_room_x
        max_x = prev_room_x + prev_room_width -1
        x = random.randint(min_x,max_x)
        y = y_pos
        h = random.randint(min_height, max_height)
        the_corridor['x'] = x
        the_corridor['y'] = y
        the_corridor['height'] = h
        self.height_available = self.height_available - h
        self.max_x_room = x
        return the_corridor
    def gen_h_corridor(self,starting_points):
        the_corridor = {'type':'hcorr','x':0,'y':0,'lenght':0}
        h_corridors = []
        for point in starting_points:
            lenght = (self.width-point[0]-1)
            the_corridor = {'type':'hcorr','x':point[0],'y':point[1],'lenght':lenght}
            h_corridors.append(the_corridor)
        return h_corridors

    def gen_vertical_part(self,width,height,max_elem_h):
        height_left = height
        total_h = 0
        start_y=2
        vert = []
        tcrh = 2 # total corridors (and) rooms height
        maximum_room_x = width // 2
        while (height_left>max_elem_h):
            room = self.gen_room(min_size=5,max_width=width,max_height=max_elem_h,y_pos=tcrh,max_x=maximum_room_x)
            self.rooms_list.append(room)
            vert.append(room)
            tcrh = tcrh + room['height']
            height_left = height - tcrh
            corridor = self.gen_v_corridor(y_pos=tcrh,min_height=5,max_height=max_elem_h,prev_room_x=room['x'],prev_room_width=room['width'])
            maximum_room_x = corridor['x']
            vert.append(corridor)
            tcrh = tcrh + corridor['height']
            height_left = height - tcrh
        # removing empty rooms and corridors
        filtered = []
        for elem in vert:
            if (elem['height']>0):
                filtered.append(elem)
        return filtered


    def draw_on_map(self,elements,map=[]):
        for element in elements:
            #
            # REMEMBER!
            # proper element positioning in dungeon is self.dungeon[Y,X]
            #
            if element['type'] == 'room':
                for w in range(element['width']):
                    for h in range(element['height']+1):
                        self.dungeon[element['y'] + h][element['x'] + w] = self.ch_floor
            elif element['type'] == 'vcorr':
                for h in range(element['height']):
                    if (element['y']+h)>=len(self.dungeon):
                        self.dungeon[len(self.dungeon)-1][element['x']] = self.ch_floor
                    else:
                        self.dungeon[element['y']+h][element['x']] = self.ch_floor
            elif element['type'] == 'hcorr':
                for l in range(element['lenght']+1):
                    self.dungeon[element['y']][element['x']+l] = self.ch_floor

    def print_map(self):
        str_dungeon = ''
        tmp_line = ''
        for line in self.dungeon:
            tmp_line = ''.join(line)
            tmp_line = tmp_line + '\n'
            str_dungeon = str_dungeon + tmp_line
        return str_dungeon

    def add_walls(self):
        for row in range(1, self.height - 1):
            for col in range(1, self.width - 1):
                if self.dungeon[row][col] == self.ch_floor:
                    if self.dungeon[row - 1][col - 1] == self.ch_bck:
                        self.dungeon[row - 1][col - 1] = self.ch_wall
                    if self.dungeon[row - 1][col] == self.ch_bck:
                        self.dungeon[row - 1][col] = self.ch_wall
                    if self.dungeon[row - 1][col + 1] == self.ch_bck:
                        self.dungeon[row - 1][col + 1] = self.ch_wall
                    if self.dungeon[row][col - 1] == self.ch_bck:
                        self.dungeon[row][col - 1] = self.ch_wall
                    if self.dungeon[row][col + 1] == self.ch_bck:
                        self.dungeon[row][col + 1] = self.ch_wall
                    if self.dungeon[row + 1][col - 1] == self.ch_bck:
                        self.dungeon[row + 1][col - 1] = self.ch_wall
                    if self.dungeon[row + 1][col] == self.ch_bck:
                        self.dungeon[row + 1][col] = self.ch_wall
                    if self.dungeon[row + 1][col + 1] == self.ch_bck:
                        self.dungeon[row + 1][col + 1] = self.ch_wall
        for row in self.dungeon:
            if row[0] == self.ch_floor: row[0] = self.ch_wall
            if row[-1] == self.ch_floor: row[-1] = self.ch_wall
        for tile in range(len(self.dungeon[-1])):
            if self.dungeon[-1][tile] == self.ch_floor: self.dungeon[-1][tile] = self.ch_wall

    def new (self):
        for h in range(self.height):
            tmp_line = []
            for w in range(self.width):
                tmp_line.append(self.ch_bck)
            self.dungeon.append(tmp_line)
        start_y = 2
        block_width = self.width // self.blocks
        all_blocks = []
        i = 0
        for blk in range(self.blocks):
            all_blocks.append([])
            vert_block = self.gen_vertical_part(width=block_width,height=self.height,max_elem_h=8)
            all_blocks[i] = vert_block
            vert_block = []
            i = i+1
        
        width_to_add = block_width
        middles_in_first_column = []
        i = 0
        for b in all_blocks:
            for elem in b:
                elem['x'] = elem['x']+block_width*i
                if (i == 0)and(elem['type'] == 'room'):
                    middles_in_first_column.append(elem['middle'])
            i = i+1
        all_blocks.append(self.gen_h_corridor(middles_in_first_column))
        i = 1
        for b in all_blocks:
            self.draw_on_map(b)
        self.add_walls()


class screen():
    def __init__(self,width,height,ground,hero=None,bck='',hx=7,hy=7):
        self.test = True
        self.width = width
        self.height = height
        self.hero = hero
        self.bck = bck
        self.ground = ground
        self.hx = hx
        self.hy = hy
        self.l_w=[]
        self.area=[]
        self.viewport = [None]*self.height
        self.sc = curses.initscr()
        self.h, self.w = self.sc.getmaxyx()
        self.win = curses.newwin(self.h, self.w, 0, 0)
        self.win.keypad(1)
        curses.curs_set(0)

        
    def draw_old(self):
        # clear()
        self.win.clear()
        self.my_screen = []
        area_string = ''
        self.matrix_debug = []
        self.area=[]
        ts = ''
        for h in range(self.height):
            for w in range(self.width):
                self.l_w.append(self.bck)
            self.area.append(self.l_w)
            self.l_w = []
        self.matrix_debug = self.area
        if (self.hero.x < len(self.area[0])) and (self.hero.y < len(self.area)):
            self.area[self.hero.y][self.hero.x] = self.hero.chr
        for line in self.area:
            area_string = area_string + ts.join(line) + '\n'
        self.test = area_string
        self.win.addstr(area_string)
        self.win.refresh()

    def expand_dungeon(self,dungeon,top_margin,bottom_margin,side_margin,expand_character='.'):
        vertical_line = []
        additional_spaces = []
        vertical_line = [expand_character]*(len(dungeon[0])+side_margin+side_margin)
        additional_spaces = [expand_character]*(side_margin)
        empty_line = []
        ext_dungeon = []
        for line in dungeon:
            for ads in additional_spaces:
                empty_line.append(ads)
            for li in line:
                empty_line.append(li)
            for ads in additional_spaces:
                empty_line.append(ads)
            ext_dungeon.append(empty_line)
            empty_line = []
        tmp_dungeon = []
        for w in range(top_margin):
            tmp_dungeon.append(vertical_line)
        for line in ext_dungeon:
            tmp_dungeon.append(line)
        for w in range(bottom_margin):
            tmp_dungeon.append(vertical_line)
        return tmp_dungeon

    def test_draw(self,rms,dungeon):
        self.area = [None]*self.height  
        tmp_dungeon = self.expand_dungeon(dungeon=dungeon,top_margin=self.height,bottom_margin=self.height,side_margin=self.width,expand_character=' ')
        area_string = ''
        self.win.clear()
        where_am_i = pick_random_room(rms)
        i = 0
        while i<(len(self.area)):
            y_coord = self.hero.dy+i+self.hy+1
            x_coord_start = self.hero.dx+(self.width-self.hy)
            x_coord_stop = self.hero.dx+self.width+(self.width-self.hy)
            self.area[i] = tmp_dungeon[y_coord][x_coord_start:x_coord_stop]
            i = i+1
        # self.win.addstr('MD: '+self.hero.move_direction+' LT: '+self.area[self.hy][self.hx-1]+' | '+self.ground)
        self.area[self.hy][self.hx] = self.hero.chr # y,x
        for line in self.area:
            area_string = area_string + ''.join(line) + '\n'
        # self.area = []
        self.win.addstr(area_string)
    def static_draw(self,rms,dungeon):
        pass
class creature():
    def __init__(self, chr, x_pos, y_pos, move_direction='',hp=100) -> None:
        self.x = x_pos
        self.y = y_pos
        # mx and my positions for placing creatures in dungeon
        self.dx = 0
        self.dy = 0
        self.move_direction = move_direction
        self.chr = chr
    def move (self,direction):
        if direction == 'left':
            self.x = self.x - 1
            self.dx = self.dx - 1
            self.move_direction = 'left'
        if direction == 'right':
            self.x = self.x + 1
            self.dx = self.dx + 1
            self.move_direction = 'right'
        if direction == 'up':
            self.y = self.y - 1
            self.dy = self.dy - 1
            self.move_direction = 'up'
        if direction == 'down':
            self.y = self.y + 1
            self.dy = self.dy + 1
            self.move_direction = 'down'