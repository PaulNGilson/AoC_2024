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

def check_safe(levels):
    if sorted(levels, reverse=True) == levels or sorted(levels) == levels:
        changes = [levels[i+1] - levels[i] for i in range(0, len(levels)-1)]
        if all(change in [1,2,3] for change in changes) or all(change in [-1,-2,-3] for change in changes):
            return True
    return False

safe = 0
for report in data:
    levels_str = report.split()
    levels = [int(n) for n in levels_str]
    if check_safe(levels):
        safe += 1

assert safe == 2 if TESTDATA else True
print("part 1:", safe)

safe_with_damping = 0
for report in data:
    levels_str = report.split()
    levels = [int(n) for n in levels_str]
    damped_safety = []
    for i in range(0, len(levels)):
        damped_safety.append(check_safe(levels[:i]+levels[i+1:]))
    if any(damped_safety):
        safe_with_damping += 1

assert safe_with_damping == 4 if TESTDATA else True
print("part 2:", safe_with_damping)
