import sys
import re

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

all_towels = data[0].split(", ")
possible_stripes = 0
for striping in data[2:]:
    try_to_match = set([striping])
    found_one = False
    while try_to_match and not found_one:
        match_me = try_to_match.pop()
        matches = [towel for towel in all_towels if match_me.startswith(towel)]
        for matcher in matches:
            remaining_stripes = match_me.removeprefix(matcher)
            if remaining_stripes == "":
                found_one = True
            else:
                try_to_match.add(remaining_stripes)
    if found_one:
        possible_stripes += 1

print("part 1:", possible_stripes)

# part 2 begins

total_stripes = 0
for striping in data[2:]:
    try_to_match = {striping: 1}
    while try_to_match:
        match_me = (k := next(iter(try_to_match)), try_to_match.pop(k))
        matches = [towel for towel in all_towels if match_me[0].startswith(towel)]
        for matcher in matches:
            remaining_stripes = match_me[0].removeprefix(matcher)
            if remaining_stripes == "":
                total_stripes += match_me[1]
            elif remaining_stripes in try_to_match.keys():
                try_to_match[remaining_stripes] += match_me[1]
            else:
                try_to_match[remaining_stripes] = match_me[1]

print("part 2:", total_stripes)

assert possible_stripes == 6 if TESTDATA else True
assert total_stripes == 16 if TESTDATA else True
