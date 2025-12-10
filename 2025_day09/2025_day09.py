import numpy as np 

filename = '2025_day09/test_input.txt'
# filename = '2025_day09/test_input2.txt'
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
all_points = set(p[0] + 1j * p[1] for p in all_points)

def find_inner_points(point, visited = None):
    if visited is None:
        visited = set()

    visited.add(point)

    for direction in [1, 1j, -1, -1j]:
        next_point = point + direction
        if next_point not in all_points and next_point not in visited:
            
            visited = find_inner_points(next_point, visited)
    return visited

inner_points = find_inner_points(3+4j)


# Inner fill
buff = 4
# inner_points = []
max_x, max_y = [max([loc[i] for loc in locations]) for i in range(2)]
# for ix in range(0, max_x + buff):
#     jy = 0
#     while jy < max_y + buff:
#         if [ix, jy] in all_points:
#             # Scan edge points until we hit a non-edge (horiz lines)
#             print(f'found edge at {ix},{jy}')
#             while [ix, jy] in all_points:
#                 print(f'   skipping {ix}, {jy} -> ')
#                 jy += 1
#             print(f'ending at {ix}, {jy}')

#             # Scan to the end of the line or until we hit another wall 
#             jy_skip = jy
#             temp_pts = []
#             while [ix, jy_skip] not in all_points and jy_skip < max_y + buff:
#                 temp_pts.append([ix, jy_skip])
#                 jy_skip += 1
#             if jy_skip == max_y + buff:
#                 # If we hit the end of the line, these are not inner pts
#                 jy = jy_skip 
#             else:
#                 # If we hit another wall, these were inner points 
#                 inner_points = inner_points + temp_pts
        
#         jy += 1

max_x, max_y = [max([loc[i] for loc in locations]) for i in range(2)]
print(f'\t', end = '')
for jy in range(0, max_y + buff):
    print(f'{jy} ', end='')
print()
for ix in range(0, max_x + buff):
    print(f'{ix}\t', end = '')
    for jy in range(0, max_y + buff):
        if [ix, jy] in locations:
            print('# ', end = '')
        elif ix + 1j*jy in all_points:
            print('@ ', end = '')
        # elif [ix, jy] in outer_edges:
        #     print('X ', end = '')
        elif ix + 1j*jy in inner_points:
            print('O ', end = '')
        else:
            print('. ', end = '')
    print()
