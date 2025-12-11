import re

filename = '2025_day10/test_input.txt'
with open(filename) as f_in:
    lines = f_in.readlines()

for line in lines:
    desired_state = re.findall(r'[\.|\#]', line)
    desired_state = [{'.':0, '#':1}[p] for p in desired_state]

    buttons = re.findall(r'\(([^)]*)\)', line)
    buttons = [[int(_b) for _b in b.split(',')] for b in buttons]

    joltage = [int(_v) for _v in re.findall(r'\{([^\}]*)\}', line)[0].split(',')]