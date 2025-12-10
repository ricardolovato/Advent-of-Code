import numpy as np 

filename = '2025_day09/test_input.txt'
# filename = '2025_day09/input.txt'
with open(filename) as f_in:
    lines = f_in.readlines()

locations = sorted([[int(_v) for _v in v.strip().split(',')] for v in lines])

# Sort the locations and only compare the top/bottom half? 
max_area = [0, 0, 0]
for i in range(0, int(len(locations)/2)):
    for j in range(len(locations)-1,int(len(locations)/2), -1):
        if i == j:
            continue

        rect = (abs(locations[j][0] - locations[i][0]) + 1) * (abs(locations[j][1] - locations[i][1]) + 1)
        if rect > max_area[2]:
            max_area = [locations[i], locations[j], rect]
        # print(f'{locations[i]} | {locations[j]} -> {rect}')
# Part 1: this seems to work 
print(max_area)

# Part 2
locations = [[int(_v) for _v in v.strip().split(',')] for v in lines]

# Outer Edges
locations = locations + [locations[0]]
outer_edges = []
for idx in range(len(locations)-1):
    next_idx = idx + 1
    if locations[idx][0] == locations[next_idx][0]:
        # same x
        min_y = min(locations[idx][1], locations[next_idx][1])
        max_y = max(locations[idx][1], locations[next_idx][1])
        for i in range(min_y, max_y):
            outer_edges.append([locations[idx][0], i])
    elif locations[idx][1] == locations[next_idx][1]:
        min_x = min(locations[idx][0], locations[next_idx][0])
        max_x = max(locations[idx][0], locations[next_idx][0])
        for i in range(min_x, max_x):
            outer_edges.append([i, locations[idx][1]])

all_points = locations + outer_edges

# Inner fill
inner_points = []
max_x, max_y = [max([loc[i] for loc in locations]) for i in range(2)]
for ix in range(0, max_x + 2):
    b_cross = False
    for jy in range(0, max_y + 4):
        if [ix, jy] in all_points and [ix, jy - 1] in all_points and [ix, jy + 1] not in all_points:
            b_cross = False
            continue

        if [ix, jy] in all_points and [ix, jy-1] not in all_points:
            if not b_cross:
                # Enter the curve
                b_cross = True
                print(f'Entering curve at {ix}, {jy}')
            else:
                # Exit curve
                b_cross = False
                print(f'Exiting curve at {ix}, {jy}')

        if b_cross:
            # Inside the curve
            inner_points.append([ix, jy])


max_x, max_y = [max([loc[i] for loc in locations]) for i in range(2)]
print(f'\t', end = '')
for jy in range(0, max_y + 4):
    print(f'{jy} ', end='')
print()
for ix in range(0, max_x + 2):
    print(f'{ix}\t', end = '')
    for jy in range(0, max_y + 4):
        if [ix, jy] in all_points:
            print('@ ', end = '')
        # if [ix, jy] in locations:
        #     print('#', end = '')
        # elif [ix, jy] in outer_edges:
        #     print('X', end = '')
        elif [ix, jy] in inner_points:
            print('O ', end = '')
        else:
            print('. ', end = '')
    print()
