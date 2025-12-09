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

# Straight line connections
locations = locations + [locations[0]]
for idx in 

max_x, max_y = [max([loc[i] for loc in locations]) for i in range(2)]
for ix in range(0, max_x + 2):
    for jy in range(0, max_y + 2):
        if [ix, jy] in locations:
            # print(f'{ix}, {jy}')
            print('#', end = '')
        else:
            print('.', end = '')
    print()