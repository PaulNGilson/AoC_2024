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

disk_map = data[0]

id_number = 0
next_representation = "file" # flip-flops between this and "space"
output = []
output_part2 = []
file_id_and_length = {} # store file block count for use later on in part 2
for digit in disk_map:
    if next_representation == "file":
        for i in range(0, int(digit)):
            output.append(str(id_number))
        output_part2.append([id_number, int(digit)])
        file_id_and_length[id_number] = int(digit)
        next_representation = "space"
        id_number += 1
    else: # next_representation == "space"
        for i in range(0, int(digit)):
            output.append(".")
        if digit != "0":
            output_part2.append([".", int(digit)])
        next_representation = "file"

assert "".join(output) == "00...111...2...333.44.5555.6666.777.888899" if TESTDATA else True

split_point = len(output) - output.count(".")
disk_to_fill = output[:split_point]
disk_to_move = [d for d in output[split_point:] if d != "."]
answer_part1 = []
for block in disk_to_fill:
    if block == ".":
        answer_part1.append(disk_to_move.pop(-1))
    else:
        answer_part1.append(block)

checksum_part1 = 0
for block in range(0, len(answer_part1)):
    checksum_part1 += block * int(answer_part1[block])

print("part 1:", checksum_part1)

for n in range(id_number-1, 0, -1):
    length_to_fit = file_id_and_length[n]
    for i in range(0, len(output_part2)):
        if output_part2[i][0] == n: # if find the whole file, we can stop looking for spaces
            break
        if output_part2[i][0] == "." and output_part2[i][1] >= length_to_fit:
            output_part2[output_part2.index([n, length_to_fit])] = [".", length_to_fit]
            dots_remaining = output_part2[i][1]-length_to_fit
            if dots_remaining > 0:
                output_part2[i] = [".", output_part2[i][1]-length_to_fit]
                output_part2.insert(i, [n, length_to_fit])
            else: # exact fit, so we just replace
                output_part2[i] = [n, length_to_fit]
            break

answer_part2 = []
for each in output_part2:
    for i in range(0, each[1]):
        answer_part2.append(each[0])

checksum_part2 = 0
for block in range(0, len(answer_part2)):
    if answer_part2[block] != ".":
        checksum_part2 += block * answer_part2[block]

print("part 2:", checksum_part2)
