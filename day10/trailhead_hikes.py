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

trailhead_coords = []

# build the initial grid
coords = {} # (x, y): height
for x in range(0, len(data[0])):
    for y in range(0, len(data)):
        coords[(x, y)] = int(data[y][x])
        if data[y][x] == "0":
            trailhead_coords.append((x, y))

def get_valid_neighbours(coord):
    neighbours = [] # list of tuples
    if (coord[0]+1, coord[1]) in coords: # E
        neighbours.append((coord[0]+1, coord[1]))
    if (coord[0]-1, coord[1]) in coords: # W
        neighbours.append((coord[0]-1, coord[1]))
    if (coord[0], coord[1]+1) in coords: # S
        neighbours.append((coord[0], coord[1]+1))
    if (coord[0], coord[1]-1) in coords: # N
        neighbours.append((coord[0], coord[1]-1))
    return neighbours

def calculate_trailhead_scores(part):
    sum_trailhead_scores = 0

    for trailhead_coord in trailhead_coords:
        current_height = 0
        current_trails = [trailhead_coord]
        while current_height != 9 and current_trails:
            new_trails = []
            for current_trail in current_trails:
                valid_neighbours = get_valid_neighbours(current_trail)
                for valid_neighbour in valid_neighbours:
                    if coords[valid_neighbour] == current_height + 1:
                        new_trails.append(valid_neighbour)
            if part == 1:
                current_trails = list(set(new_trails))
            else: # part == 2
                current_trails = new_trails
            current_height += 1
        sum_trailhead_scores += len(current_trails)
    return sum_trailhead_scores

assert calculate_trailhead_scores(1) == 36 if TESTDATA else True
assert calculate_trailhead_scores(2) == 81 if TESTDATA else True

print("part 1:", calculate_trailhead_scores(1))
print("part 2:", calculate_trailhead_scores(2))
