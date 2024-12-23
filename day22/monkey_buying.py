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

def step_one(n):
    return ((n*64) ^ n) % 16777216
def step_two(n):
    return (int(n/32) ^ n) % 16777216
def step_three(n):
    return ((n*2048) ^ n) % 16777216

total_two_thousandth_secret_nums = 0
for secret_number in [int(line) for line in data]:
    for _ in range(0, 2000):
        secret_number = step_three(step_two(step_one(secret_number)))
    total_two_thousandth_secret_nums += secret_number

print("part 1:", total_two_thousandth_secret_nums)

# part 2 begins

overall_sequence_prices = defaultdict(int)

for secret_number in [int(line) for line in data]:
    change_prices = []
    for _ in range(0, 2000):
        new_secret_number = step_three(step_two(step_one(secret_number)))
        change_prices.append((str(new_secret_number % 10 - secret_number % 10), new_secret_number % 10))
        secret_number = new_secret_number
    sequence_prices = {}
    for i in range(0, len(change_prices)-3):
        sequence = ",".join([change_prices[i][0], change_prices[i+1][0], change_prices[i+2][0], change_prices[i+3][0]])
        if sequence not in sequence_prices:
            sequence_prices[sequence] = change_prices[i+3][1]

    for sequence_price in sequence_prices:
        overall_sequence_prices[sequence_price] += sequence_prices[sequence_price]

best_price = max(overall_sequence_prices.values())
#print(list(overall_sequence_prices.keys())[list(overall_sequence_prices.values()).index(best_price)])
print("part 2:", best_price)
