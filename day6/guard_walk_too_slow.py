import sys
import copy

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

class Guard:
    def __init__(self, x, y, direction):
        self.x = x
        self.start_x = x
        self.y = y
        self.start_y = y
        self.direction = direction
    def move(self, current_coords):
        if self.direction == "N":
            if self.y == 0:
                return False
            elif current_coords[self.x][self.y-1] == "#":
                if current_coords[self.x+1][self.y] == "#":
                    self.y += 1
                    self.direction = "S"
                else:
                    self.x += 1
                    self.direction = "E"
            else:
                self.y -= 1
        elif self.direction == "E":
            if self.x == len(data[0])-1:
                return False
            elif current_coords[self.x+1][self.y] == "#":
                if current_coords[self.x][self.y+1] == "#":
                    self.x -= 1
                    self.direction = "W"
                else:
                    self.y += 1
                    self.direction = "S"
            else:
                self.x += 1
        elif self.direction == "S":
            if self.y == len(data)-1:
                return False
            elif current_coords[self.x][self.y+1] == "#":
                if current_coords[self.x-1][self.y] == "#":
                    self.y -= 1
                    self.direction = "N"
                else:
                    self.x -= 1
                    self.direction = "W"
            else:
                self.y += 1
        elif self.direction == "W":
            if self.x == 0:
                return False
            elif current_coords[self.x-1][self.y] == "#":
                if current_coords[self.x][self.y-1] == "#":
                    self.x += 1
                    self.direction = "E"
                else:
                    self.y -= 1
                    self.direction = "N"
            else:
                self.x -= 1
        return True

def debug_print_grid(coords):
    for y in range(0, len(data)):
        output_line = ""
        for x in range(0, len(data[0])):
            output_line += coords[x][y]
        print(output_line)
    print("")

def count_guard_visits(coords):
    visited = 0
    for x in range(0, len(data[0])):
        for y in range(0, len(data)):
            if coords[x][y] == "X":
                visited += 1
    return visited

# build the initial grid
coords = {}
for x in range(0, len(data[0])):
    coords[x] = {}
    for y in range(0, len(data)):
        if data[y][x] == "^":
            guard = Guard(x, y, "N")
            coords[x][y] = "."
        else:
            coords[x][y] = data[y][x]

# part 2 needs this
potential_obstructions = []

while True:
    coords[guard.x][guard.y] = "X"
    potential_obstructions.append((guard.x, guard.y))
    # debug_print_grid(coords)
    if not guard.move(coords):
        break

print("part 1:", count_guard_visits(coords))
assert count_guard_visits(coords) == 41 if TESTDATA else True

# part 2 begins
potential_obstructions = list(set(potential_obstructions))
potential_obstructions.remove((guard.start_x, guard.start_y))

loop_count = 0

for potential_obstruction in potential_obstructions:
    obstructed_coords = copy.deepcopy(coords)
    obstructed_coords[potential_obstruction[0]][potential_obstruction[1]] = "#"
    # debug_print_grid(obstructed_coords)
    guard.x = guard.start_x
    guard.y = guard.start_y
    guard.direction = "N"
    history = []

    while True:
        if (guard.x, guard.y, guard.direction) in history:
            loop_count += 1
            break
        else:
            history.append((guard.x, guard.y, guard.direction))
        if not guard.move(obstructed_coords):
            break
    # debug_print_grid(obstructed_coords)

print("part 2:", loop_count)
