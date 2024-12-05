import sys
from collections import Counter

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

page_orders = []
print_orders = []

for line in data:
    if "|" in line:
        page_orders.append(tuple(line.split("|")))
    elif "," in line:
        print_orders.append(line.split(","))

middle_page_sum = 0
middle_page_sum_with_fixes = 0

for print_order in print_orders:
    matching_page_orders = []
    for page_order in page_orders:
        if page_order[0] in print_order and page_order[1] in print_order:
            matching_page_orders.append(page_order)
    correct_ordering_freq = Counter([po[0] for po in matching_page_orders])
    correct_ordering = {v: k for k, v in correct_ordering_freq.items()}
    correct_order_list = []
    for i in range(len(print_order)-1, 0, -1):
        correct_order_list.append(correct_ordering[i])
    correct_order = ",".join(correct_order_list)
    if correct_order == ",".join(print_order[:-1]):
        middle_page_sum += int(print_order[int(len(print_order)/2)])
    else:
        middle_page_sum_with_fixes += int(correct_ordering[int(len(print_order)/2)])

print("part 1:", middle_page_sum)
print("part 2:", middle_page_sum_with_fixes)
