import sys

def open_input():
    filename = "input.txt"
    if TESTDATA:
        filename = "input_" + TESTDATA + ".txt"
    file = open(filename, "r")
    data_raw = file.readlines()
    file.close()
    data = []
    for line in data_raw:
        data.append(line.strip())
    return data

TESTDATA = None
if len(sys.argv) > 1:
    TESTDATA = sys.argv[1]

data = open_input()

coords = {}
for y in range(0, len(data)-2):
    for x in range(0, len(data[0])):
        if data[y][x] == "@": # robot start
            robot = (x, y)
            coords[(x, y)] = "."
        else:
            coords[(x, y)] = data[y][x]

directions = list(data[-1])

def lies_ahead(robot, direction):
    current_x = robot[0]
    current_y = robot[1]
    ahead = []
    wall_or_gap_not_found = True
    while wall_or_gap_not_found:
        if direction == ">":
            current_x += 1
        elif direction == "<":
            current_x -= 1
        elif direction == "v":
            current_y += 1
        elif direction == "^":
            current_y -= 1
        next_space = coords[(current_x, current_y)]
        ahead.append(next_space)
        if next_space == "#" or next_space == ".":
            wall_or_gap_not_found = False
    return ahead

assert lies_ahead(robot, ">") == ['.'] if TESTDATA else True
assert lies_ahead((1, 7), ">") == ['O', 'O', '.'] if TESTDATA else True
assert lies_ahead((6, 7), ">") == ['O', 'O', '#'] if TESTDATA else True
assert lies_ahead(robot, "<") == ['O', '.'] if TESTDATA else True
assert lies_ahead(robot, "v") == ['.'] if TESTDATA else True
assert lies_ahead((5, 6), "v") == ['O', 'O', '#'] if TESTDATA else True
assert lies_ahead(robot, "^") == ['.'] if TESTDATA else True

def print_grid():
    for y in range(0, len(data)-2):
        output_line = ""
        for x in range(0, len(data[0])):
            if (x, y) == robot:
                output_line += "@"
            else:
                output_line += coords[(x, y)]
        print(output_line)

while directions:
    direction = directions.pop(0)
    ahead = lies_ahead(robot, direction)
    if ahead[-1] == "#":
        pass # we can't move, so this direction is essentially discarded
    else: # ahead[-1] == "."
        if direction == ">":
            robot = (robot[0]+1, robot[1])
            if "O" in ahead:
                coords[(robot[0]+len(ahead)-1, robot[1])] = "O"
        elif direction == "<":
            robot = (robot[0]-1, robot[1])
            if "O" in ahead:
                coords[(robot[0]-(len(ahead)-1), robot[1])] = "O"
        elif direction == "v":
            robot = (robot[0], robot[1]+1)
            if "O" in ahead:
                coords[(robot[0], robot[1]+len(ahead)-1)] = "O"
        elif direction == "^":
            robot = (robot[0], robot[1]-1)
            if "O" in ahead:
                coords[(robot[0]), robot[1]-(len(ahead)-1)] = "O"
        coords[(robot[0], robot[1])] = "." # may have already been true

#print_grid()

gps_coords_sum = 0
for y in range(0, len(data)-2):
    for x in range(0, len(data[0])):
        if coords[(x, y)] == "O":
            gps_coords_sum += (x + 100*y)

print("part 1:", gps_coords_sum)

# part 2 begins

class Wall:
    def __init__(self, x, y):
        self.left_side = (x, y)
        self.right_side = (x+1, y)

class Box:
    def __init__(self, x, y):
        self.left_side = (x, y)
        self.right_side = (x+1, y)
    def move(self, x_d, y_d):
        self.left_side = (self.left_side[0]+x_d, self.left_side[1]+y_d)
        self.right_side = (self.right_side[0]+x_d, self.right_side[1]+y_d)

class Grid:
    def __init__(self):
        self.rows = {} # containing boxes and walls occurring on each row
        for y in range(0, len(data)-2):
            self.rows[y] = []

grid = Grid()

for y in range(0, len(data)-2):
    for x_half in range(0, len(data[0])):
        if data[y][x_half] == "#":
            grid.rows[y].append(Wall(x_half*2, y))
        elif data[y][x_half] == "O":
            grid.rows[y].append(Box(x_half*2, y))
        elif data[y][x_half] == "@":
            robot = (x_half*2, y)

def inhabits(x, y):
    items = grid.rows[y]
    for item in items:
        if item.left_side == (x, y) and type(item) == Box:
            return "["
        elif item.right_side == (x, y) and type(item) == Box:
            return "]"
        elif item.left_side == (x, y) or item.right_side == (x, y):
            return "#"
    return "."

def print_grid_part_2():
    for y in range(0, len(data)-2):
        output_line = ""
        for x in range(0, len(data[0])*2):
            if (x, y) == robot:
                output_line += "@"
            else:
                output_line += inhabits(x, y)
        print(output_line)

def encounters(robot, direction):
    # different for v/^ compared with </>
    no_walls = True
    if direction == "v":
        x_d = 0
        y_d = 1
    elif direction == "^":
        x_d = 0
        y_d = -1
    elif direction == ">":
        x_d = 1
        y_d = 0
    elif direction == "<":
        x_d = -1
        y_d = 0
    things_to_check = [(robot[0]+x_d, robot[1]+y_d)]
    checked_things = [] # a list of boxes, walls, maybe empty i.e. nothing directly ahead of robot
    while things_to_check and no_walls:
        check = things_to_check.pop()
        items = grid.rows[check[1]]
        for item in items:
            if item.left_side == check or item.right_side == check:
                if type(item) == Wall:
                    no_walls = False
                else:
                    checked_things.append(item)
                    if direction == "v" or direction == "^":
                        things_to_check.append((item.left_side[0]+x_d, item.left_side[1]+y_d))
                        things_to_check.append((item.right_side[0]+x_d, item.right_side[1]+y_d))
                    elif direction == ">":
                        things_to_check.append((item.right_side[0]+x_d, item.right_side[1]+y_d))
                    elif direction == "<":
                        things_to_check.append((item.left_side[0]+x_d, item.left_side[1]+y_d))
    if no_walls:
        return list(set(checked_things))
    else:
        return "#"

#print_grid_part_2()

directions = list(data[-1])
while directions:
    direction = directions.pop(0)
    encountered = encounters(robot, direction)
    if encountered == "#": # immediately or because of boxes up against a wall
        pass # we can't move, so this direction is essentially discarded
    else:
        if direction == "v":
            x_d = 0
            y_d = 1
        elif direction == "^":
            x_d = 0
            y_d = -1
        elif direction == ">":
            x_d = 1
            y_d = 0
        elif direction == "<":
            x_d = -1
            y_d = 0
        robot = (robot[0]+x_d, robot[1]+y_d)
        for box in encountered:
            if direction == "v" or direction == "^":
                grid.rows[box.left_side[1]].remove(box)
                grid.rows[box.left_side[1]+y_d].append(box)
            box.move(x_d, y_d)

gps_coords_sum_part_2 = 0
for y in grid.rows.keys():
    for item in grid.rows[y]:
        if type(item) == Box:
            gps_coords_sum_part_2 += (item.left_side[0] + 100*item.left_side[1])

print("part 2:", gps_coords_sum_part_2)
