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

for part in [1, 2]:
    calibration_total = 0
    for line in data:
        total_string, number_string = line.split(": ")
        total = int(total_string)
        numbers = [int(n) for n in number_string.split(" ")]
        calculations = [(numbers[0], numbers[1:])] # list of (total, [remaining numbers])
        still_looking = True
        while len(calculations) > 0 and still_looking:
            calculation = calculations.pop()

            calc_add = calculation[0] + calculation[1][0]
            calc_mul = calculation[0] * calculation[1][0]
            calc_con = int(str(calculation[0]) + str(calculation[1][0]))
            calcs = [calc_add, calc_mul] if part == 1 else [calc_add, calc_mul, calc_con]

            for calc in calcs:
                if calc == total and len(calculation[1]) == 1:
                    calibration_total += total
                    still_looking = False
                    break
                elif calc == total:
                    calculations.append((calc, calculation[1][1:]))
                elif calc < total and len(calculation[1]) > 1:
                    calculations.append((calc, calculation[1][1:]))

    assert calibration_total == 3749 if (TESTDATA and part == 1) else True
    assert calibration_total == 11387 if (TESTDATA and part == 2) else True
    print(f"part {part}:", calibration_total)
