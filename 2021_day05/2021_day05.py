import re

filename = '2021_day05/test_input.txt'
filename = '2021_day05/input.txt'

with open(filename) as f_in:
    lines = f_in.readlines()

lines = [[int(v) for v in re.findall(r'(\d+)', line)] for line in lines]

points = {}
for x1, y1, x2, y2 in lines:
    start = [x1, y1]
    stop = [x2, y2]    

    if x1 == x2:
        # Same row
        for yi in range(min(y1, y2), max(y1, y2) + 1):
            if (x1, yi) not in points:
                points[(x1, yi)] = 1
            else:
                points[(x1, yi)] += 1
    elif y1 == y2:
        # Same col
        for xi in range(min(x1, x2), max(x1, x2) + 1):
            if (xi, y1) not in points:
                points[(xi, y1)] = 1
            else:
                points[(xi, y1)] += 1
    else:
        print(f'non-vertical points: ({x1}, {y1}) -> ({x2}, {y2})')
print(len([k for k, v in points.items() if v > 1]))