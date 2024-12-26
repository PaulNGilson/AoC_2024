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

file = open("numpad.txt", "r")
numpad_raw = file.readlines()
file.close()
numpad_transitions = {"A": {}, "9": {}, "8": {}, "7": {}, "6": {}, "5": {}, "4": {}, "3": {}, "2": {}, "1": {}, "0": {}}

for line in numpad_raw:
    nums_from_to, routes_str = line.strip().split(" ", 1)
    num_from, num_to = nums_from_to.split("-")
    routes = routes_str.split(" ")
    numpad_transitions[num_from][num_to] = routes

file = open("dirpad.txt", "r")
dirpad_raw = file.readlines()
file.close()
dirpad_transitions = {"A": {}, "^": {}, "v": {}, "<": {}, ">": {}}

for line in dirpad_raw:
    dirs_from_to, routes_str = line.strip().split(" ", 1)
    dir_from, dir_to = dirs_from_to.split("-")
    routes = routes_str.split(" ")
    dirpad_transitions[dir_from][dir_to] = routes

# for all robots not at the numberpad or immediately next in the sequence, use
# this mapping
# 
# <vA proven more efficient than v<A
# ^>A proven more efficient than >^A
# v>A proven more efficient than >vA
segment_mapping = {
    "A": ["A"],
    "<A": ["v<<A", ">>^A"],
    "vA": ["<vA", "^>A"],
    ">A": ["vA", "^A"],
    "^A": ["<A", ">A"],
    "<<A": ["v<<A", "A", ">>^A"],
    ">>A": ["vA", "A", "^A"],
    "<^A": ["v<<A", ">^A", ">A"],
    ">^A": ["vA", "<^A", ">A"],
    "v<A": ["<vA", "<A", ">>^A"],
    "v>A": ["<vA", ">A", "^A"],
    "v<<A": ["<vA", "<A", "A", ">>^A"],
    ">>^A": ["vA", "A", "<^A", ">A"],
    "^<A": ["<A", "v<A", ">>^A"],
    "^>A": ["<A", "v>A", "^A"],
    "<vA": ["v<<A", ">A", "^>A"],
    ">vA": ["vA", "<A", "^>A"]
}

def calculate_complexity(dirpad_robots):
    total_complexity = 0

    for example_code in data:
        example_code_seq = ["A"] + list(example_code)
        presses_last_directional = [""]
        for i in range(0, len(example_code_seq)-1):
            press_options = numpad_transitions[example_code_seq[i]][example_code_seq[i+1]]
            presses_last_directional_new = []
            for p in presses_last_directional:
                for po in press_options:
                    presses_last_directional_new.append(p + po + "A")
            presses_last_directional = presses_last_directional_new

        presses_mid_directional = []
        for last_directional_code in presses_last_directional:
            last_directional_code_seq = ["A"] + list(last_directional_code)
            presses_mid_directional_interim = [""]
            for i in range(0, len(last_directional_code_seq)-1):
                if last_directional_code_seq[i] == last_directional_code_seq[i+1]:
                    press_options = [""]
                else:
                    press_options = dirpad_transitions[last_directional_code_seq[i]][last_directional_code_seq[i+1]]
                presses_mid_directional_new = []
                for p in presses_mid_directional_interim:
                    for po in press_options:
                        presses_mid_directional_new.append(p + po + "A")
                presses_mid_directional_interim = presses_mid_directional_new
            presses_mid_directional += presses_mid_directional_interim

        # convert the list of strings to a list of dicts
        presses_mid_directional_dicts = []
        for s in presses_mid_directional:
            segments = [seg+"A" for seg in s.split("A")][:-1]
            d = defaultdict(int)
            for segment in segments:
                d[segment] += 1
            presses_mid_directional_dicts.append(d)

        loop_amount = dirpad_robots - 1
        for _ in range(0, loop_amount):
            presses_new_directional_dicts = []
            for next_bot_dict in presses_mid_directional_dicts:
                presses_new_directional = defaultdict(int)
                for segment in next_bot_dict.keys():
                    for new_segment in segment_mapping[segment]:
                        presses_new_directional[new_segment] += next_bot_dict[segment]
                presses_new_directional_dicts.append(presses_new_directional)
            presses_mid_directional_dicts = presses_new_directional_dicts

        complexities = []
        for pmdd in presses_mid_directional_dicts:
            complexities.append(sum([len(k)*v for k, v in pmdd.items()]))
        total_complexity += min(complexities) * int(example_code[:-1])

    return total_complexity

print("part 1:", calculate_complexity(2))
assert calculate_complexity(2) == 128962 if not TESTDATA else True

print("part 2:", calculate_complexity(25))
assert calculate_complexity(25) == 159684145150108 if not TESTDATA else True
