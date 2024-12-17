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

def get_combo_operand(operand):
    if 0 <= operand <= 3:
        return operand
    elif operand == 4:
        return reg_a
    elif operand == 5:
        return reg_b
    elif operand == 6:
        return reg_c
    else: # operand == 7 -- apparently this is "reserved"
        return None

# operand literal or combo has not been calculated by this stage
def do_opcode_instruction(opcode, operand):
    global reg_a, reg_b, reg_c
    if opcode == 0: # adv
        reg_a = int(reg_a / (2 ** get_combo_operand(operand)))
    elif opcode == 1: # bxl
        reg_b = reg_b ^ operand
    elif opcode == 2: # bst
        reg_b = get_combo_operand(operand) % 8
    elif opcode == 3: # jnz
        if reg_a == 0:
            return None, None
        else:
            return "instruction jump", operand
    elif opcode == 4: # bxc
        reg_b = reg_b ^ reg_c
    elif opcode == 5: # out
        return "output", get_combo_operand(operand) % 8
    elif opcode == 6: # bdv -- not used
        reg_b = int(reg_a / (2 ** get_combo_operand(operand)))
    elif opcode == 7: # cdv
        reg_c = int(reg_a / (2 ** get_combo_operand(operand)))
    return None, None

reg_a = int(data[0].split()[2])
reg_b = int(data[1].split()[2])
reg_c = int(data[2].split()[2])
program = [int(n) for n in data[4].split()[1].split(",")]
instruction_pointer = 0

output = []

while instruction_pointer < len(program):
    opcode = program[instruction_pointer]
    operand = program[instruction_pointer+1]
    outcome, detail = do_opcode_instruction(opcode, operand)
    if outcome == "output":
        output.append(detail)
    if outcome == "instruction jump":
        instruction_pointer = detail
    else: # where outcome is "output" or None
        instruction_pointer += 2

print("part 1:", ",".join([str(n) for n in output]))

previous_successful_reg_a = 0
target_length = len(program)-1

# work backwards from the end of the required program
while target_length >= 0:
    target_program = program[target_length:]

    found_it = False
    reg_a_attempt = previous_successful_reg_a * 8
    while not found_it:
        reg_a = reg_a_attempt
        #reg_b = int(data[1].split()[2]) - these are unnecessary, as reg_b & reg_c get reset each loop
        #reg_c = int(data[2].split()[2])
        program = [int(n) for n in data[4].split()[1].split(",")]
        instruction_pointer = 0

        output = []

        while instruction_pointer < len(program):
            opcode = program[instruction_pointer]
            operand = program[instruction_pointer+1]
            outcome, detail = do_opcode_instruction(opcode, operand)
            if outcome == "output":
                output.append(detail)
            if outcome == "instruction jump":
                instruction_pointer = detail
            else: # where outcome is "output" or None
                instruction_pointer += 2
        if output == target_program:
            previous_successful_reg_a = reg_a_attempt
            break
        else:
            reg_a_attempt += 1
    target_length -= 1

print("part 2:", previous_successful_reg_a)

