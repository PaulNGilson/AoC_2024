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
for y in range(0, len(data)):
    for x in range(0, len(data[0])):
        if data[y][x] == "S":
            coords[(x, y)] = "."
            start = (x, y)
        elif data[y][x] == "E":
            coords[(x, y)] = "."
            end = (x, y)
        else:
            coords[(x, y)] = data[y][x]

def print_grid():
    for y in range(0, len(data)):
        output_line = ""
        for x in range(0, len(data[0])):
            output_line += coords[(x, y)]
        print(output_line)

#print_grid()

def can_move(position, direction):
    if direction == "E":
        return coords[(position[0]+1, position[1])] == "."
    elif direction == "W":
        return coords[(position[0]-1, position[1])] == "."
    elif direction == "N":
        return coords[(position[0], position[1]-1)] == "."
    elif direction == "S":
        return coords[(position[0], position[1]+1)] == "."

all_end_routes = []
bests = {}
current_paths = [(start, "E", 0, [start])] # coord, direction, cost
while current_paths:
    path = current_paths.pop(0)
    # move onwards in 3 directions (going backwards can never make sense)
    # if it's a wall, clearly it gets discarded
    # if it reaches an older place, we review
    # else it gets added to the current_paths
    new_paths = []
    if path[1] == "E":
        if can_move(path[0], "E"):
            new_paths.append(((path[0][0]+2, path[0][1]), "E", path[2]+2, path[3] + [(path[0][0]+1, path[0][1]), (path[0][0]+2, path[0][1])]))
        if can_move(path[0], "N"):
            new_paths.append(((path[0][0], path[0][1]-2), "N", path[2]+1002, path[3] + [(path[0][0], path[0][1]-1), (path[0][0], path[0][1]-2)]))
        if can_move(path[0], "S"):
            new_paths.append(((path[0][0], path[0][1]+2), "S", path[2]+1002, path[3] + [(path[0][0], path[0][1]+1), (path[0][0], path[0][1]+2)]))
    elif path[1] == "W":
        if can_move(path[0], "W"):
            new_paths.append(((path[0][0]-2, path[0][1]), "W", path[2]+2, path[3] + [(path[0][0]-1, path[0][1]), (path[0][0]-2, path[0][1])]))
        if can_move(path[0], "N"):
            new_paths.append(((path[0][0], path[0][1]-2), "N", path[2]+1002, path[3] + [(path[0][0], path[0][1]-1), (path[0][0], path[0][1]-2)]))
        if can_move(path[0], "S"):
            new_paths.append(((path[0][0], path[0][1]+2), "S", path[2]+1002, path[3] + [(path[0][0], path[0][1]+1), (path[0][0], path[0][1]+2)]))
    elif path[1] == "N":
        if can_move(path[0], "N"):
            new_paths.append(((path[0][0], path[0][1]-2), "N", path[2]+2, path[3] + [(path[0][0], path[0][1]-1), (path[0][0], path[0][1]-2)]))
        if can_move(path[0], "W"):
            new_paths.append(((path[0][0]-2, path[0][1]), "W", path[2]+1002, path[3] + [(path[0][0]-1, path[0][1]), (path[0][0]-2, path[0][1])]))
        if can_move(path[0], "E"):
            new_paths.append(((path[0][0]+2, path[0][1]), "E", path[2]+1002, path[3] + [(path[0][0]+1, path[0][1]), (path[0][0]+2, path[0][1])]))
    elif path[1] == "S":
        if can_move(path[0], "S"):
            new_paths.append(((path[0][0], path[0][1]+2), "S", path[2]+2, path[3] + [(path[0][0], path[0][1]+1), (path[0][0], path[0][1]+2)]))
        if can_move(path[0], "W"):
            new_paths.append(((path[0][0]-2, path[0][1]), "W", path[2]+1002, path[3] + [(path[0][0]-1, path[0][1]), (path[0][0]-2, path[0][1])]))
        if can_move(path[0], "E"):
            new_paths.append(((path[0][0]+2, path[0][1]), "E", path[2]+1002, path[3] + [(path[0][0]+1, path[0][1]), (path[0][0]+2, path[0][1])]))
    for new_path in new_paths:
        if new_path[0] == end:
            all_end_routes.append(new_path)
        if new_path[0] in bests.keys():
            if new_path[1] in bests[new_path[0]].keys():
                if new_path[2] <= bests[new_path[0]][new_path[1]]: #### sus!
                # for part 1, this was just `<` and sufficient to solve
                    bests[new_path[0]][new_path[1]] = new_path[2]
                    current_paths.append(new_path)
            else: # not been here in this direction yet, so add it
                bests[new_path[0]][new_path[1]] = new_path[2]
                current_paths.append(new_path)
        else: # not been here at all
            bests[new_path[0]] = {}
            bests[new_path[0]][new_path[1]] = new_path[2]
            current_paths.append(new_path)

best_possible = min(bests[end].values())
assert best_possible == 7036 if TESTDATA else True

print("part 1:", best_possible)

all_spaces = []
for route in all_end_routes:
    if route[2] == best_possible:
        all_spaces += route[3]

print("part 2:", len(set(all_spaces)))
