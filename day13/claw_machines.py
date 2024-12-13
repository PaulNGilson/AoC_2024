import sys
import sympy

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

machines = []
machine = {}
for line in data:
    if line == "":
        machines.append(machine)
        machine = {}
    elif "Button A" in line:
        machine["A"] = {"x": int(line.split("+")[1].split(",")[0]), "y": int(line.split("+")[2])}
    elif "Button B" in line:
        machine["B"] = {"x": int(line.split("+")[1].split(",")[0]), "y": int(line.split("+")[2])}
    elif "Prize" in line:
        machine["x_target"] = int(line.split("=")[1].split(",")[0])
        machine["y_target"] = int(line.split("=")[2])
machines.append(machine)

# example machine:
# machine = {
#     "A": {"x": 94, "y": 34},
#     "B": {"x": 22, "y": 67},
#     "x_target": 8400,
#     "y_target": 5400
# }

total_token_spend = 0

for machine in machines:
    valid_presses = []
    for b_presses in range(0, 101):
        x_reached_with_b = machine["B"]["x"]*b_presses
        y_reached_with_b = machine["B"]["y"]*b_presses
        if x_reached_with_b <= machine["x_target"] and y_reached_with_b <= machine["y_target"]:
            x_target_remaining = machine["x_target"] - x_reached_with_b
            y_target_remaining = machine["y_target"] - y_reached_with_b
            if x_target_remaining % machine["A"]["x"] == 0:
                a_presses = int(x_target_remaining / machine["A"]["x"])
                if a_presses * machine["A"]["y"] == y_target_remaining:
                    valid_presses.append({"a_presses": a_presses, "b_presses": b_presses})
                    break
        else:
            break
    optimal_tokens = 100000 # we just set this to a too-high number
    for valid_press_combination in valid_presses:
        tokens = valid_press_combination["a_presses"] * 3 + valid_press_combination["b_presses"] * 1
        optimal_tokens = min(optimal_tokens, tokens)

    if optimal_tokens != 100000:
        total_token_spend += optimal_tokens

assert total_token_spend == 480 if TESTDATA else 30973
print("part 1:", total_token_spend)

# part 2 begins

total_token_spend = 0

a, b = sympy.symbols('a,b')
for machine in machines:
    button_a_x = machine["A"]["x"]
    button_a_y = machine["A"]["y"]
    button_b_x = machine["B"]["x"]
    button_b_y = machine["B"]["y"]
    eq1 = sympy.Eq(button_a_x*a + button_b_x*b, machine["x_target"]+10000000000000)
    eq2 = sympy.Eq(button_a_y*a + button_b_y*b, machine["y_target"]+10000000000000)
    valid_presses = sympy.solve([eq1, eq2], dict=True)
    
    optimal_tokens = 10000000000000 # we just set this to a too-high number
    for valid_press_combination in valid_presses:
        if valid_press_combination[a].is_Integer and valid_press_combination[b].is_Integer:
            tokens = valid_press_combination[a] * 3 + valid_press_combination[b] * 1
            optimal_tokens = min(optimal_tokens, tokens)

    if optimal_tokens != 10000000000000:
        total_token_spend += optimal_tokens

print("part 2:", total_token_spend)
