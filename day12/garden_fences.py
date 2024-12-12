import sys
import itertools

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

coords = []
for y in range(0, len(data)):
    for x in range(0, len(data[0])):
        coords.append((x, y))

def get_neighbours(coord, include_outside_grid=False):
    neighbours = []
    if coord[0] > 0 or include_outside_grid:
        neighbours.append((coord[0]-1, coord[1]))
    if coord[1] > 0 or include_outside_grid:
        neighbours.append((coord[0], coord[1]-1))
    if coord[0] < len(data[0])-1 or include_outside_grid:
        neighbours.append((coord[0]+1, coord[1]))
    if coord[1] < len(data)-1 or include_outside_grid:
        neighbours.append((coord[0], coord[1]+1))
    return neighbours

def get_region_neighbours(coord):
    neighbours = get_neighbours(coord)
    region_neighbours = []
    for neighbour in neighbours:
        if data[coord[1]][coord[0]] == data[neighbour[1]][neighbour[0]]:
            region_neighbours.append(neighbour)
    return region_neighbours

def expand_region(region_start, coords):
    found_more = True
    current_region = [region_start]
    while found_more:
        found_more = False
        for plant in current_region:
            neighbours = get_region_neighbours(plant)
            new_neighbours = set(neighbours).difference(set(current_region))
            if new_neighbours:
                found_more = True
                current_region += new_neighbours
                for new_neighbour in new_neighbours:
                    coords.remove(new_neighbour)
    return current_region, coords


regions = []
while coords:
    region_start = coords.pop()
    new_regions, remaining_coords = expand_region(region_start, coords)
    regions.append({"coords": new_regions, "fence_length": 0, "plant_type": data[region_start[1]][region_start[0]]})
    coords = remaining_coords

total_price = 0
for region in regions:
    #print(data[region[0][1]][region[0][0]], region)
    fences = 0
    for plant in region["coords"]:
        plant_neighbours = get_neighbours(plant, include_outside_grid=True)
        #print(set(plant_neighbours).difference(set(region)))
        fences += len(set(plant_neighbours).difference(set(region["coords"])))
    total_price += fences * len(region["coords"])
    region["fence_length"] = fences

assert total_price == 1930 if TESTDATA else 1573474
print("part 1:", total_price)

# part 2 begins

"""
Part 2's solution looks at pairs of cells in a plant region and, if they're
adjacent, it looks at the adjacent cells on either side e.g.

  X R

  R R

  M M

If both of the plants on one side are different to the region's plant type,
that's a straight fence continuation and so the fence length of that region is
at least 1 fence shorter.
"""

def adjacent(plant_pair):
    p0 = plant_pair[0]
    p1 = plant_pair[1]
    return (abs(p1[0]-p0[0]) + abs(p1[1]-p0[1])) == 1

def get_adjacent_pairs(plant_pair):
    p0 = plant_pair[0]
    p1 = plant_pair[1]
    if p0[0] == p1[0]:
        return [[(p0[0]-1, p0[1]), (p1[0]-1, p1[1])], [(p0[0]+1, p0[1]), (p1[0]+1, p1[1])]]
    elif p0[1] == p1[1]:
        return [[(p0[0], p0[1]-1), (p1[0], p1[1]-1)], [(p0[0], p0[1]+1), (p1[0], p1[1]+1)]]

def get_plant(coord):
    if 0 <= coord[0] < len(data[0]) and 0 <= coord[1] < len(data):
        return data[coord[1]][coord[0]]
    else:
        return "."

total_discount_price = 0
for region in regions:
    fence_reduction = 0
    plant_pairs = list(itertools.combinations(region["coords"], 2))
    for plant_pair in plant_pairs:
        if adjacent(plant_pair):
            adjacent_plant_pair_pairs = get_adjacent_pairs(plant_pair)
            for adjacent_plant_pair_pair in adjacent_plant_pair_pairs:
                plants = [get_plant(p) for p in adjacent_plant_pair_pair]
                if plants[0] != region["plant_type"] and plants[1] != region["plant_type"]:
                    fence_reduction += 1
    total_discount_price += (region["fence_length"]-fence_reduction) * len(region["coords"])

print("part 2:", total_discount_price)
