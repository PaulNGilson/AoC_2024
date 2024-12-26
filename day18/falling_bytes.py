import sys
from functools import lru_cache

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
grid_size = 0
byte_coords = []

byte_limit = 12 if TESTDATA else 1024

for line in data[:byte_limit]:
    x, y = [int(s) for s in line.split(",")]
    grid_size = max(grid_size, x, y)
    byte_coords.append((x, y))

def get_possible_coords(x, y):
    possible_coords = []
    if x+1 <= grid_size and (x+1, y) not in byte_coords:
        possible_coords.append((x+1, y))
    if y+1 <= grid_size and (x, y+1) not in byte_coords:
        possible_coords.append((x, y+1))
    if x-1 >= 0 and (x-1, y) not in byte_coords:
        possible_coords.append((x-1, y))
    if y-1 >= 0 and (x, y-1) not in byte_coords:
        possible_coords.append((x, y-1))
    return possible_coords

history = {} # (x, y): best_steps
routes = [(0, 0, 0)] # (x, y, steps so far)
while routes:
    current_x, current_y, current_steps = routes.pop(0)
    possible_coords = get_possible_coords(current_x, current_y)
    for possible_coord in possible_coords:
        if possible_coord in history.keys():
            if history[possible_coord] > current_steps + 1:
                history[possible_coord] = current_steps + 1
                routes.append((possible_coord[0], possible_coord[1], current_steps+1))
        else:
            history[possible_coord] = current_steps + 1
            routes.append((possible_coord[0], possible_coord[1], current_steps+1))

assert history[(grid_size, grid_size)] == 22 if TESTDATA else True

print("part 1:", history[(grid_size, grid_size)])

# part 2 begins

@lru_cache(maxsize=None)
def get_connected(x, y):
    possible_coords = []
    if x+1 <= grid_size:
        possible_coords.append((x+1, y))
    if y+1 <= grid_size:
        possible_coords.append((x, y+1))
    if x-1 >= 0:
        possible_coords.append((x-1, y))
    if y-1 >= 0:
        possible_coords.append((x, y-1))
    if x+1 <= grid_size and y+1 <= grid_size:
        possible_coords.append((x+1, y+1))
    if x+1 <= grid_size and y-1 >= 0:
        possible_coords.append((x+1, y-1))
    if x-1 >= 0 and y+1 <= grid_size:
        possible_coords.append((x-1, y+1))
    if x-1 >= 0 and y-1 >= 0:
        possible_coords.append((x-1, y-1))
    return possible_coords

edge_left_bottom = set()
unconnected = []
for line in data:
    x, y = [int(s) for s in line.split(",")]
    if x == 0 or y == grid_size or set(get_connected(x, y)).intersection(edge_left_bottom):
        edge_left_bottom.add((x, y))
        found_more = True
        while found_more:
            found_more = False
            for possible in unconnected:
                if set(get_connected(possible[0], possible[1])).intersection(edge_left_bottom):
                    found_more = True
                    unconnected.remove(possible)
                    edge_left_bottom.add(possible)
    if any(byte[0] == grid_size for byte in edge_left_bottom) or \
        any(byte[1] == 0 for byte in edge_left_bottom):
        print("part 2:", line)
        break
    else:
        unconnected.append((x, y))
