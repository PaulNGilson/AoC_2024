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

coords = {}

for y in range(0, len(data)):
    for x in range(0, len(data[0])):
        if data[y][x] == "S":
            start = (x, y)
            coords[(x, y)] = {"cell": ".", "steps": 0}
        elif data[y][x] == "E":
            end = (x, y)
            coords[(x, y)] = {"cell": "."}
        elif data[y][x] == "#":
            coords[(x, y)] = {"cell": "#"}
        else:
            coords[(x, y)] = {"cell": "."}

# def print_grid():
#     for y in range(0, len(data)):
#         outline = ""
#         for x in range(0, len(data[0])):
#             outline += coords[(x, y)]["cell"]
#         print(outline)
#print_grid()

current = start
steps = 0

def get_direction(cell, previous_direction):
    if coords[(cell[0], cell[1]-1)]["cell"] == "." and previous_direction != "S":
        return "N"
    elif coords[(cell[0], cell[1]+1)]["cell"] == "." and previous_direction != "N":
        return "S"
    elif coords[(cell[0]-1, cell[1])]["cell"] == "."  and previous_direction != "E":
        return "W"
    elif coords[(cell[0]+1, cell[1])]["cell"] == "."  and previous_direction != "W":
        return "E"

direction = None
while True:
    direction = get_direction(current, direction)
    if direction == "N":
        coords[(current[0], current[1]-1)]["steps"] = steps+1
        coords[(current[0], current[1]-2)]["steps"] = steps+2
        current = (current[0], current[1]-2)
    elif direction == "S":
        coords[(current[0], current[1]+1)]["steps"] = steps+1
        coords[(current[0], current[1]+2)]["steps"] = steps+2
        current = (current[0], current[1]+2)
    elif direction == "W":
        coords[(current[0]-1, current[1])]["steps"] = steps+1
        coords[(current[0]-2, current[1])]["steps"] = steps+2
        current = (current[0]-2, current[1])
    elif direction == "E":
        coords[(current[0]+1, current[1])]["steps"] = steps+1
        coords[(current[0]+2, current[1])]["steps"] = steps+2
        current = (current[0]+2, current[1])
    steps += 2
    if current == end:
        break

# part 1 begins

def get_on_path_over_wall(x, y):
    reachables = []
    if x-2 >= 0 and coords[(x-2, y)]["cell"] == ".":
        reachables.append(coords[(x-2, y)])
    if x+2 <= len(data[0])-1 and coords[(x+2, y)]["cell"] == ".":
        reachables.append(coords[(x+2, y)])
    if y-2 >= 0 and coords[(x, y-2)]["cell"] == ".":
        reachables.append(coords[(x, y-2)])
    if y+2 <= len(data)-1 and coords[(x, y+2)]["cell"] == ".":
        reachables.append(coords[(x, y+2)])
    return reachables

cheats = defaultdict(int)

for y in range(1, len(data)):
    for x in range(1, len(data[0])):
        if coords[(x, y)].get("steps") or (x, y) == start:
            reachables = get_on_path_over_wall(x, y)
            for reachable in reachables:
                if coords[(x, y)]["steps"] < reachable["steps"]: # and reachable.get("steps") --- not necessary?
                    cheat = reachable["steps"]-coords[(x, y)]["steps"]-2
                    if cheat != 0:
                        cheats[cheat] += 1

assert cheats == {4: 14, 12: 3, 2: 14, 10: 2, 8: 4, 6: 2, 64: 1, 40: 1, 38: 1, 20: 1, 36: 1} if TESTDATA else True

print("part 1:", sum([v for k, v in cheats.items() if k >= 100]))

# part 2 begins

def get_reachable_variable_amount(x, y, amount):
    reachables = []
    for yr in range(-amount, amount+1):
        for xr in range(-amount, amount+1):
            distance_away = abs(xr)+abs(yr)
            if distance_away <= amount and (x+xr, y+yr) in coords.keys():
                target = coords[(x+xr, y+yr)]
                if target.get("steps"):
                    reachables.append({"steps": target["steps"], "distance_away": distance_away})
    return reachables

cheats_part2 = defaultdict(int)

for y in range(0, len(data)):
    for x in range(0, len(data[0])):
        if coords[(x, y)].get("steps") or (x, y) == start:
            reachables_with_distance = get_reachable_variable_amount(x, y, 20)
            for reachable_with_distance in reachables_with_distance:
                if coords[(x, y)]["steps"] < reachable_with_distance["steps"]:
                    cheat = reachable_with_distance["steps"]-coords[(x, y)]["steps"]-reachable_with_distance["distance_away"]
                    if cheat != 0:
                        cheats_part2[cheat] += 1

assert cheats_part2[76] == 3 if TESTDATA else True
assert cheats_part2[64] == 19 if TESTDATA else True
assert cheats_part2[50] == 32 if TESTDATA else True

cheats_over_100 = sum([v for k, v in cheats_part2.items() if k >= 100])

assert cheats_over_100 == 1021490 if not TESTDATA else True

print("part 2:", cheats_over_100)
