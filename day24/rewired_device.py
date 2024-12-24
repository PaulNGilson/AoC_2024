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

wires = {}
gates = defaultdict(list)

for line in data:
    if ":" in line:
        wire, val = line.split(": ")
        wires[wire] = int(val)
    elif "->" in line:
        w1, gate_type, w2, _, o = line.split(" ")
        ws = sorted([w1, w2])
        gates[(ws[0], ws[1])].append({"type": gate_type, "out": o})

def get_output_val(determined_wires, in_wires, gate_type):
    w1 = determined_wires[in_wires[0]]
    w2 = determined_wires[in_wires[1]]
    if gate_type == "AND":
        return w1 & w2
    elif gate_type == "OR":
        return w1 | w2
    elif gate_type == "XOR":
        return w1 ^ w2

while gates:
    for input_wires in gates.keys():
        if input_wires[0] in wires and input_wires[1] in wires:
            #print("####", gates[input_wires]["out"])
            for output_gate_and_wire in gates[input_wires]:
                out_val = get_output_val(wires, input_wires, output_gate_and_wire["type"])
                wires[output_gate_and_wire["out"]] = out_val
            gates.pop(input_wires)
            break

binary_num = ""
i = 0
while True:
    if "z" + "{:02d}".format(i) in wires:
        binary_num = str(wires["z" + "{:02d}".format(i)]) + binary_num
        i += 1
    else:
        break

print("part 1:", int(binary_num, 2))

# part 2 begins

if TESTDATA:
    exit()

gates = defaultdict(list)
for line in data:
    if "->" in line:
        w1, gate_type, w2, _, o = line.split(" ")
        ws = sorted([w1, w2])
        gates[(ws[0], ws[1])].append({"type": gate_type, "out": o})

# identify curios:
# * Where a z## output doesn't come from an XOR
# * Where inputs to z## output gate don't have either from an x## XOR y## gate output

preceding_zs = [] # tuples
for input_wires in gates.keys():
    for gate in gates[input_wires]:
        if gate["out"][0] == "z" and gate["type"] != "XOR":
            #print(input_wires, gate)
            pass # uncomment line above to see the notes below
        elif gate["out"][0] == "z":
            preceding_zs.append(input_wires)

for preceding_z_options in preceding_zs:
    found_one = False
    for input_wires in gates.keys():
        for gate in gates[input_wires]:
            if gate["out"] == preceding_z_options[0] or gate["out"] == preceding_z_options[1]:
                if input_wires[0][0] == "x":
                    if gate["type"] != "XOR":
                        #print(input_wires, gate)
                        pass # uncomment line above to see the notes below
"""
('jdd', 'rbm') {'type': 'AND', 'out': 'z36'}
('hgp', 'mkv') {'type': 'OR', 'out': 'z45'}
('jcd', 'wdr') {'type': 'OR', 'out': 'z23'}
('x16', 'y16') {'type': 'AND', 'out': 'z16'}
('x00', 'y00') {'type': 'AND', 'out': 'bwv'}
('x11', 'y11') {'type': 'AND', 'out': 'qnw'}
"""

# ignoring start and end - 00 and 45 - we have 4 curios
# * 11
# * 16
# * 23
# * 36

output_switches = []
# switch 1
gates[("x11", "y11")] = [{"type": "AND", "out": "qff"}, {"type": "XOR", "out": "qnw"}]
output_switches += ["qff", "qnw"]
# switch 2
gates[("x16", "y16")] = [{"type": "AND", "out": "pbv"}, {"type": "XOR", "out": "dfn"}]
gates[("dfn", "qcr")] = [{"type": "XOR", "out": "z16"}, {"type": "AND", "out": "mvp"}]
output_switches += ["pbv", "z16"]
# switch 3
gates[("bcd", "cts")] = [{"type": "AND", "out": "jcd"}, {"type": "XOR", "out": "z23"}]
gates[("jcd", "wdr")] = [{"type": "OR", "out": "qqp"}]
output_switches += ["qqp", "z23"]
# switch 4
gates[("jdd", "rbm")] = [{"type": "AND", "out": "fbq"}, {"type": "XOR", "out": "z36"}]
output_switches += ["fbq", "z36"]

# set one example input
wires = {}
for i in range(0, 45):
    wires["x" + "{:02d}".format(i)] = 0
    wires["y" + "{:02d}".format(i)] = 1
wires["x00"] = 1

while gates:
    for input_wires in gates.keys():
        if input_wires[0] in wires and input_wires[1] in wires:
            #print("####", gates[input_wires]["out"])
            for output_gate_and_wire in gates[input_wires]:
                out_val = get_output_val(wires, input_wires, output_gate_and_wire["type"])
                wires[output_gate_and_wire["out"]] = out_val
            gates.pop(input_wires)
            break

z_output = ""
for i in range(0, 46):
    z_output = str(wires["z" + "{:02d}".format(i)]) + z_output

assert int(z_output, 2) == 35184372088832 if not TESTDATA else True

print("part 2:", ",".join(sorted(output_switches)))
