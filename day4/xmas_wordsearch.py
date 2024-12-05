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
for x in range(0, len(data[0])):
    coords[x] = {}
    for y in range(0, len(data)):
        coords[x][y] = data[y][x]

def valid(x, y):
    return x >= 0 and x < len(data[0]) and y >= 0 and y < len(data)

def discover_xmas(starting_coords, change):
    xmas_in_direction = 0
    for x, y in starting_coords:
        xmas = 0
        while valid(x, y):
            if coords[x][y] == "X":
                xmas = 1
            elif xmas == 1 and coords[x][y] == "M":
                xmas = 2
            elif xmas == 2 and coords[x][y] == "A":
                xmas = 3
            elif xmas == 3 and coords[x][y] == "S":
                xmas = 0
                xmas_in_direction += 1
            else:
                xmas = 0
            x += change["xd"]
            y += change["yd"]
    return xmas_in_direction

directions = {
    "east": {
        "starting_coords": [(0, y) for y in range(0, len(data))],
        "change": {"xd": 1, "yd": 0}
    },
    "west": {
        "starting_coords": [(len(data[0])-1, y) for y in range(0, len(data))],
        "change": {"xd": -1, "yd": 0}
    },
    "south": {
        "starting_coords": [(x, 0) for x in range(0, len(data[0]))],
        "change": {"xd": 0, "yd": 1}
    },
    "north": {
        "starting_coords": [(x, len(data)-1) for x in range(0, len(data[0]))],
        "change": {"xd": 0, "yd": -1}
    },
    "south-east": {
        "starting_coords": [(x, 0) for x in range(0, len(data[0]))] + [(0, y) for y in range(1, len(data))],
        "change": {"xd": 1, "yd": 1}
    },
    "south-west": {
        "starting_coords": [(x, 0) for x in range(0, len(data[0]))] + [(len(data[0])-1, y) for y in range(1, len(data))],
        "change": {"xd": -1, "yd": 1}
    },
    "north-east": {
        "starting_coords": [(x, len(data)-1) for x in range(0, len(data[0]))] + [(0, y) for y in range(0, len(data)-1)],
        "change": {"xd": 1, "yd": -1}
    },
    "north-west": {
        "starting_coords": [(x, len(data)-1) for x in range(0, len(data[0]))] + [(len(data[0])-1, y) for y in range(0, len(data)-1)],
        "change": {"xd": -1, "yd": -1}
    }
}

assert discover_xmas(directions["east"]["starting_coords"], directions["east"]["change"]) == 3 if TESTDATA else True
assert discover_xmas(directions["west"]["starting_coords"], directions["west"]["change"]) == 2 if TESTDATA else True
assert discover_xmas(directions["south"]["starting_coords"], directions["south"]["change"]) == 1 if TESTDATA else True
assert discover_xmas(directions["north"]["starting_coords"], directions["north"]["change"]) == 2 if TESTDATA else True
assert discover_xmas(directions["south-east"]["starting_coords"], directions["south-east"]["change"]) == 1 if TESTDATA else True
assert discover_xmas(directions["south-west"]["starting_coords"], directions["south-west"]["change"]) == 1 if TESTDATA else True
assert discover_xmas(directions["north-east"]["starting_coords"], directions["north-east"]["change"]) == 4 if TESTDATA else True
assert discover_xmas(directions["north-west"]["starting_coords"], directions["north-west"]["change"]) == 4 if TESTDATA else True

xmas_total = 0
for direction in directions:
    xmas_total += discover_xmas(directions[direction]["starting_coords"], directions[direction]["change"])

print("part 1:", xmas_total)

def discover_mas_crossed(target_coords):
    cross_letters = [
        coords[target_coords[0]-1][target_coords[1]-1],
        coords[target_coords[0]+1][target_coords[1]-1],
        coords[target_coords[0]+1][target_coords[1]+1],
        coords[target_coords[0]-1][target_coords[1]+1]
    ]
    return cross_letters in [
        ["M", "M", "S", "S"],
        ["S", "M", "M", "S"],
        ["S", "S", "M", "M"],
        ["M", "S", "S", "M"]
    ]

mas_crossed_total = 0
for x in range(1, len(data[0])-1):
    for y in range(1, len(data)-1):
        if coords[x][y] == "A" and discover_mas_crossed((x, y)):
            mas_crossed_total += 1

print("part 2:", mas_crossed_total)
