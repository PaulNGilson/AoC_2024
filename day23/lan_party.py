import sys
from collections import defaultdict
from itertools import combinations

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

connections = defaultdict(list)
for line in data:
    pc1, pc2 = line.split("-")
    connections[pc1].append(pc2)
    connections[pc2].append(pc1)

inter_connected_threes = set()
for pc in connections.keys():
    if pc[0] == "t":
        pc_connections = connections[pc]
        potential_inter_connecting_pairs = list(combinations(pc_connections, 2))
        for pair in potential_inter_connecting_pairs:
            if pair[1] in connections[pair[0]]:
                 inter_connected_threes.add("-".join(sorted([pc, pair[0], pair[1]])))

assert len(inter_connected_threes) == 7 if TESTDATA else True
print("part 1:", len(inter_connected_threes))

# part 2 begins

best_blooms = []
best_bloom = 0

for pc in connections.keys():
    bloom_numbers = defaultdict(int)
    for connection in connections[pc]:
        bloom_numbers[connection] += 1
        for connected_connection in connections[connection]:
            bloom_numbers[connected_connection] += 1
    highest = max(bloom_numbers.values())
    if highest >= best_bloom:
        best_blooms.append(bloom_numbers)
        best_bloom = highest

most_connections_with_good_blooms = 0

for bloom in best_blooms:
    n = list(bloom.values()).count(best_bloom) + list(bloom.values()).count(best_bloom-1)
    if n >= most_connections_with_good_blooms:
        good_enough_bloom = bloom
        most_connections_with_good_blooms = n

out = []
for k, v in good_enough_bloom.items():
    if v >= best_bloom-1:
        out.append(k)

assert ",".join(sorted(out)) == "co,de,ka,ta" if TESTDATA else True
print("part 2:", ",".join(sorted(out)))
