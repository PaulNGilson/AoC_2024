import sys
import re
import math
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
    height = 7
    width = 11
else:
    height = 103
    width = 101

data = open_input()

seconds = 100

quadrant_counts = {
    "top-left": 0,
    "top-right": 0,
    "bottom-left": 0,
    "bottom-right": 0
}
midpoint_width = (width-1) / 2
midpoint_height = (height-1) / 2

robots = []

for robot in data:
    _, _, x_start, _, y_start, _, _, _, x_vel, _, y_vel = re.split("(=|,| )", robot)
    x_start = int(x_start)
    y_start = int(y_start)
    x_vel = int(x_vel)
    y_vel = int(y_vel)
    end_x = (x_vel*seconds + x_start) % width
    end_y = (y_vel*seconds + y_start) % height
    robots.append({"x": x_start, "y": y_start, "x_vel": x_vel, "y_vel": y_vel})
    if end_x < midpoint_width and end_y < midpoint_height:
        quadrant_counts["top-left"] += 1
    elif end_x > midpoint_width and end_y < midpoint_height:
        quadrant_counts["top-right"] += 1
    elif end_x < midpoint_width and end_y > midpoint_height:
        quadrant_counts["bottom-left"] += 1
    elif end_x > midpoint_width and end_y > midpoint_height:
        quadrant_counts["bottom-right"] += 1

assert math.prod(quadrant_counts.values()) == 12 if TESTDATA else 217132650
print("part 1:", math.prod(quadrant_counts.values()))

# part 2 begins

def draw_picture(robots):
    coords = []
    for robot in robots:
        coords.append((robot["x"], robot["y"]))
    for y in range(0, height):
        output_line = ""
        for x in range(0, width):
            if (x, y) in coords:
                output_line += "#"
            else:
                output_line += "."
        print(output_line)

"""
Assume tree will look something like this:

etc
   #     #
  #       #
 ##       ##
  #       #
 #         #
###### ###### <--- looking to find this, given assumption (pretty close!)
     # #
     ###
"""
def move_and_detect(robots):
    new_robots = []
    y_robots = defaultdict(set)
    for robot in robots:
        x_new = (robot["x_vel"] + robot["x"]) % width
        y_new = (robot["y_vel"] + robot["y"]) % height
        new_robots.append({"x": x_new, "y": y_new, "x_vel": robot["x_vel"], "y_vel": robot["y_vel"]})
        y_robots[y_new].add(x_new)
    return new_robots, max([len(xs) for xs in y_robots.values()])

for s in range(1, 100001):
    robots, max_y_robots = move_and_detect(robots)
    if max_y_robots > 30: # find something exceptional - _what_ a lucky guess
        #print("time passed:", s, max_y_robots)
        #draw_picture(robots)
        break

assert s == 6516 if not TESTDATA else True
print("part 2:", s)
