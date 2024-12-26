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

locks = []
keys = []
current = None
thing = []

for line in data:
    if line == "":
        if current == "lock":
            locks.append(thing)
        else:
            keys.append(thing)
        current = None
    elif current == None and line == "#####":
        current = "lock"
        thing = ["#####"]
    elif current == None and line == ".....":
        current = "key"
        thing = ["....."]
    else:
        thing.append(line)
if current == "lock":
    locks.append(thing)
else:
    keys.append(thing)

digital_locks = []
digital_keys = []

for lock in locks:
    transposed = list(map(list, zip(*lock)))
    d_lock = []
    for t in transposed:
        d_lock.append(t.count("#"))
    digital_locks.append(d_lock)
for key in keys:
    transposed = list(map(list, zip(*key)))
    d_key = []
    for t in transposed:
        d_key.append(t.count("#"))
    digital_keys.append(d_key)

fits = 0

for d_lock in digital_locks:
    for d_key in digital_keys:
        combined = []
        for i in range(0, 5):
            combined.append(d_lock[i] + d_key[i])
        if max(combined) <= 7:
            fits += 1

assert fits == 3 if TESTDATA else True

print("part 1:", fits)
