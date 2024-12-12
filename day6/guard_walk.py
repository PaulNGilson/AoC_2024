import sys
import copy

def open_input():
    filename = "input.txt"
    if len(sys.argv) > 1:
        filename = "input_" + sys.argv[1] + ".txt"
    file = open(filename, "r")
    data_raw = file.readlines()
    file.close()
    data = []
    for line in data_raw:
        data.append(line.strip())
    return data

TESTDATA = None
if len(sys.argv) > 1 and sys.argv[1] == "test":
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

class QuickGuard:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
    def move(self, hori, vert):
        if self.direction == "E":
            self.x = next_visit("normal", hori[self.y], self.x)
            self.direction = "S"
        elif self.direction == "W":
            self.x = next_visit("reverse", hori[self.y], self.x)
            self.direction = "N"
        elif self.direction == "S":
            self.y = next_visit("normal", vert[self.x], self.y)
            self.direction = "W"
        elif self.direction == "N":
            self.y = next_visit("reverse", vert[self.x], self.y)
            self.direction = "E"
        if self.x == None or self.y == None:
            return "left area"
        else:
            return False

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

hori = {}
for y in range(0, len(data)):
    hori[y] = []
    for x in range(0, len(data[0])):
        if coords[x][y] == "#":
            hori[y].append(x)

vert = {}
for x in range(0, len(data[0])):
    vert[x] = []
    for y in range(0, len(data)):
        if coords[x][y] == "#":
            vert[x].append(y)

assert hori == {0: [4], 1: [9], 2: [], 3: [2], 4: [7], 5: [], 6: [1], 7: [8], 8: [0], 9: [6]} if TESTDATA else True
assert vert == {0: [8], 1: [6], 2: [3], 3: [], 4: [0], 5: [], 6: [9], 7: [4], 8: [7], 9: [1]} if TESTDATA else True

def next_visit(orientation, obstacle_indices, current_index):
    """
    orientation is "normal" or "reverse"
    obstacle indicies is one of hori or vert dictionaries
    """
    next_index = None
    if orientation == "normal":
        for obstacle_index in obstacle_indices:
            if obstacle_index > current_index:
                next_index = obstacle_index-1
                break
    else: # orientation == "reverse"
        for obstacle_index in reversed(obstacle_indices):
            if obstacle_index < current_index:
                next_index = obstacle_index+1
                break
    return next_index

assert next_visit("normal", hori[0], 0) == 3 if TESTDATA else True # we move E a few spaces
assert next_visit("normal", hori[0], 3) == 3 if TESTDATA else True # we are already at an obstacle
assert next_visit("normal", hori[0], 5) == None if TESTDATA else True # we leave the area
assert next_visit("normal", hori[7], 2) == 7 if TESTDATA else True # we move E a few spaces

assert next_visit("reverse", hori[0], 9) == 5 if TESTDATA else True # we move W a few spaces
assert next_visit("reverse", hori[0], 5) == 5 if TESTDATA else True # we are already at an obstacle
assert next_visit("reverse", hori[0], 3) == None if TESTDATA else True # we leave the area
assert next_visit("reverse", hori[8], 6) == 1 if TESTDATA else True # we move W a few spaces

assert next_visit("normal", vert[0], 0) == 7 if TESTDATA else True # we move S a few spaces
assert next_visit("normal", vert[0], 7) == 7 if TESTDATA else True
assert next_visit("normal", vert[0], 9) == None if TESTDATA else True
assert next_visit("normal", vert[7], 1) == 3 if TESTDATA else True

assert next_visit("reverse", vert[1], 9) == 7 if TESTDATA else True # we move N a few spaces
assert next_visit("reverse", vert[1], 7) == 7 if TESTDATA else True
assert next_visit("reverse", vert[1], 5) == None if TESTDATA else True
assert next_visit("reverse", vert[4], 5) == 1 if TESTDATA else True

potential_obstructions = []

while True:
    coords[guard.x][guard.y] = "X"
    potential_obstructions.append((guard.x, guard.y))
    if not guard.move(coords):
        break
print("part 1:", len(set(potential_obstructions)))

potential_obstructions = list(set(potential_obstructions))
potential_obstructions.remove((guard.start_x, guard.start_y))

loop_count = 0

for potential_obstruction in potential_obstructions:
    qg = QuickGuard(guard.start_x, guard.start_y, "N")

    hori_new = copy.deepcopy(hori)
    vert_new = copy.deepcopy(vert)
    hori_new[potential_obstruction[1]].append(potential_obstruction[0])
    hori_new[potential_obstruction[1]].sort()
    vert_new[potential_obstruction[0]].append(potential_obstruction[1])
    vert_new[potential_obstruction[0]].sort()

    reason_for_end = False
    history = [qg.__dict__.copy()]
    while not reason_for_end:
        reason_for_end = qg.move(hori_new, vert_new)
        if qg.__dict__ in history:
            reason_for_end = "loop"
        else:
            history.append(qg.__dict__.copy())
    if reason_for_end == "loop":
        loop_count += 1

print("part 2:", loop_count)