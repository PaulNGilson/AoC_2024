import sys, traceback

TESTDATA = None
if len(sys.argv) > 1:
    TESTDATA = sys.argv[1]

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

def check(actual, expected, variant="test"):
    if (TESTDATA and variant == "test") or (not TESTDATA and variant != "test"):
        if actual != expected:
            print("CHECK FAILED:")
            print("  actual:", actual)
            print("expected:", expected)
            print("\n".join(traceback.format_stack(limit=2)))
            exit()

data = open_input()

left_list = []
right_list = []
for line in data:
    left_s, right_s = line.split()
    left_list.append(int(left_s))
    right_list.append(int(right_s))
left_list.sort()
right_list.sort()

check(left_list, [1, 2, 3, 3, 3, 4])
check(right_list, [3, 3, 3, 4, 5, 9])

total_differences = 0
for i in range(0, len(left_list)):
    total_differences += abs(left_list[i] - right_list[i])

check(total_differences, 11)

print("part 1:", total_differences)

total_similarity = 0
for left_i in left_list:
    total_similarity += left_i * right_list.count(left_i)

check(total_similarity, 31)

print("part 2:", total_similarity)
