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

data = "".join(data) # input.txt source data is unexpectedly split across >1 line

multiplications_total = 0
matches = re.finditer("mul\([0-9]+,[0-9]+\)", data)
for match in matches:
    numbers = [int(n) for n in re.findall("[0-9]+", match.group(0))]
    multiplications_total += numbers[0] * numbers[1]

assert multiplications_total == 161 if TESTDATA else True

print("part 1:", multiplications_total)

multiplications_total_2 = 0
matches = re.finditer("(mul\([0-9]+,[0-9]+\)|do\(\)|don't\(\))", data)
enabled = True
for match in matches:
    if match.group(0) == "don't()":
        enabled = False
    elif match.group(0) == "do()":
        enabled = True
    elif enabled:
        numbers = [int(n) for n in re.findall("[0-9]+", match.group(0))]
        multiplications_total_2 += numbers[0] * numbers[1]

print("part 2:", multiplications_total_2)
