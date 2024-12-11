import sys
from collections import defaultdict

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

starting_rocks = data[0].split()

rocks = starting_rocks
max_blinks = 25
for blink in range(0, max_blinks):
    next_rocks = []
    for rock in rocks:
        if rock == "0":
            next_rocks.append("1")
        elif len(rock) % 2 == 0:
            next_rocks.append(rock[:int(len(rock)/2)])
            new_rock = str(int(rock[int(len(rock)/2):]))
            next_rocks.append(new_rock)
        else:
            next_rocks.append(str(int(rock)*2024))
    rocks = next_rocks

assert len(rocks) == 55312 if TESTDATA else True
print("part 1:", len(rocks))

# part 2 begins

rocks_dict = defaultdict(int)
for starting_rock in starting_rocks:
    rocks_dict[starting_rock] += 1

max_blinks = 75
for blink in range(0, max_blinks):
    next_rocks_dict = defaultdict(int)
    for rock in rocks_dict.keys():
        if rock == "0":
            next_rocks_dict["1"] += rocks_dict[rock]
        elif len(rock) % 2 == 0:
            next_rocks_dict[rock[:int(len(rock)/2)]] += rocks_dict[rock]
            new_rock = str(int(rock[int(len(rock)/2):]))
            next_rocks_dict[new_rock] += rocks_dict[rock]
        else:
            next_rocks_dict[str(int(rock)*2024)] += rocks_dict[rock]
    rocks_dict = next_rocks_dict

assert sum(rocks_dict.values()) == 65601038650482 if TESTDATA else True
print("part 2:", sum(rocks_dict.values()))
