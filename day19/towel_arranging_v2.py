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
# sort the towels so we deal with the smaller matches, first (for performance)
all_towels.sort(key=len)

total_stripes = 0
can_be_striped = 0
for striping in data[2:]:
    try_to_match = {striping: 1}
    found_one = False
    while try_to_match:
        # take the largest amount left to match, first
        match_me = (k := next(iter(try_to_match)), try_to_match.pop(k))
        matches = [towel for towel in all_towels if match_me[0].startswith(towel)]
        for matcher in matches:
            remaining_stripes = match_me[0].removeprefix(matcher)
            if remaining_stripes == "":
                total_stripes += match_me[1]
                found_one = True
            elif remaining_stripes in try_to_match.keys():
                try_to_match[remaining_stripes] += match_me[1]
            else:
                try_to_match[remaining_stripes] = match_me[1]
    if found_one:
        can_be_striped += 1

print("part 1:", can_be_striped)
print("part 2:", total_stripes)

assert can_be_striped == 6 if TESTDATA else 272
assert total_stripes == 16 if TESTDATA else 1041529704688380
