import sys
from collections import defaultdict
from itertools import combinations

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
max_x = len(data[0])-1
max_y = len(data)-1

# build the initial grid
antennas = defaultdict(list)
for x in range(0, max_x+1):
    for y in range(0, max_y+1):
        if data[y][x] != ".":
            antennas[data[y][x]].append((x, y))

def valid_antinode(anti):
    return 0 <= anti[0] <= max_x and 0 <= anti[1] <= max_y

def get_antinodes(antenna_pair, run_once=True):
    a1, a2 = antenna_pair
    xd = a2[0] - a1[0]
    yd = a2[1] - a1[1]
    antinodes = []

    i = 1
    potential_antinode1 = (a2[0]+i*xd, a2[1]+i*yd)
    while valid_antinode(potential_antinode1):
        antinodes.append(potential_antinode1)
        if run_once:
            break
        i += 1
        potential_antinode1 = (a2[0]+i*xd, a2[1]+i*yd)

    i = 1
    potential_antinode2 = (a1[0]-i*xd, a1[1]-i*yd)
    while valid_antinode(potential_antinode2):
        antinodes.append(potential_antinode2)
        if run_once:
            break
        i += 1
        potential_antinode2 = (a1[0]-i*xd, a1[1]-i*yd)

    return antinodes

antinodes_part1 = []
antinodes_part2 = []
for antenna_notation in antennas.keys():
    antenna_pairs = list(combinations(antennas[antenna_notation], 2))
    for antenna_pair in antenna_pairs:
        antinodes_part1 += get_antinodes(antenna_pair)
        antinodes_part2 += get_antinodes(antenna_pair, run_once=False)

    # each antenna is also an antinode
    antinodes_part2 += antennas[antenna_notation]

antinodes_part1_count = len(set(antinodes_part1))
antinodes_part2_count = len(set(antinodes_part2))

assert antinodes_part1_count == 14 if TESTDATA else 222
assert antinodes_part2_count == 34 if TESTDATA else 884

print("part 1:", antinodes_part1_count)
print("part 2:", antinodes_part2_count)
