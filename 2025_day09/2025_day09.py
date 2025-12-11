import numpy as np


def print_grid():
    buff = 4
    max_x, max_y = [max([loc[i] for loc in locations]) for i in range(2)]
    with open('2025_day09/grid.txt', 'w') as f_out:
        # print(f'\t', end='')
        f_out.write(f'\t')
        for jy in range(0, max_y + buff):
            # print(f'{jy} ', end='')
            f_out.write(f'{jy} ')
        # print()
        f_out.write('\n')
        for ix in range(0, max_x + buff):
            # print(f'{ix}\t', end='')
            f_out.write(f'{ix}\t')
            for jy in range(0, max_y + buff):
                if ix + 1j * jy in red_tiles:
                    # print('# ', end='')
                    f_out.write('# ')
                elif ix + 1j * jy in green_tiles:
                    # print('X ', end='')
                    f_out.write('X ')
                # if [ix, jy] in locations:
                #     # print('# ', end='')
                #     f_out.write('# ')
                # # elif ix + 1j*jy in all_points:
                # #     print('@ ', end = '')
                # elif [ix, jy] in outer_edges:
                #     # print('X ', end='')
                #     f_out.write('X ')
                # elif ix + 1j*jy in inner_points:
                #     print('O ', end = '')
                elif ix + 1j * jy in fence:
                    # print('X ', end='')
                    f_out.write('O ')
                else:
                    # print('. ', end='')
                    f_out.write('. ')
            # print()
            f_out.write('\n')


filename = '2025_day09/test_input.txt'
# filename = '2025_day09/test_input2.txt'
# filename = '2025_day09/input.txt'
with open(filename) as f_in:
    lines = f_in.readlines()

locations = sorted([[int(_v) for _v in v.strip().split(',')] for v in lines])

# Sort the locations and only compare the top/bottom half? 
max_area = [0, 0, 0]
for i in range(0, int(len(locations) / 2)):
    for j in range(len(locations) - 1, int(len(locations) / 2), -1):
        if i == j:
            continue

        rect = (abs(locations[j][0] - locations[i][0]) + 1) * (abs(locations[j][1] - locations[i][1]) + 1)
        if rect > max_area[2]:
            max_area = [locations[i], locations[j], rect]
# Part 1: this seems to work 
print(max_area)

# Part 2
locations = [[int(_v) for _v in v.strip().split(',')] for v in lines]

# Outer Edges
locations = locations + [locations[0]]
outer_edges = []
for idx in range(len(locations) - 1):
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


# Verify that the curve is continuous by walking the edge
def verify_edges(start):
    visited = set()
    stack = [start]

    while stack:
        point = stack.pop()
        if point in visited:
            continue
        visited.add(point)

        for direction in [1, -1, 1j, -1j]:
            next_point = point + direction
            if next_point not in visited and next_point in all_points:
                stack.append(next_point)
    return visited

#
# if len(verify_edges(locations[0][0] + 1j * locations[0][1])) != len(all_points):
#     print('path not continuous')


# visited = set()
# for point in all_points:
#     num_adjacent = 0
#     for direction in [-1, 1, -1j, 1j]:
#         if point + direction in all_points:
#             num_adjacent += 1
#     if num_adjacent < 2:
#         print(f'{point}: {num_adjacent} adjacent')


def find_inner_points_recursive(point, visited=None):
    if visited is None:
        visited = set()

    visited.add(point)

    for direction in [1, 1j, -1, -1j]:
        next_point = point + direction
        if next_point not in all_points and next_point not in visited:
            visited = find_inner_points_recursive(next_point, visited)
    return visited


def find_inner_points(start):
    visited = set()
    stack = [start]

    while stack:
        point = stack.pop()
        if point in visited:
            continue
        visited.add(point)

        for direction in [1, -1, 1j, -1j]:
            next_point = point + direction
            if next_point not in visited and next_point not in all_points:
                stack.append(next_point)
    return visited


# Find an inner point
def first_inner_pt(locations, all_points):
    max_x, max_y = [max([loc[i] for loc in locations]) for i in range(2)]
    for ix in range(0, max_x):
        for jy in range(0, max_y):
            pt = ix + 1j * jy
            if pt not in all_points and pt - 1j in all_points and pt - 1 in all_points and pt - 1 - 1j in all_points:
                return pt

#
# def find_points(start, condition):
#     visited = set()
#     stack = [start]
#
#     while stack:
#         point = stack.pop()
#         if point in visited:
#             continue
#         visited.add(point)
#
#         for direction in [1, -1, 1j, -1j]:
#             next_point = point + direction
#             if condition(next_point, visited):
#                 stack.append(next_point)
#     return visited
#
#
# outer_cond = lambda x, visited: x not in visited and x in all_points
# inner_cond = lambda x, visited: x not in visited and x not in all_points

if len(verify_edges(locations[0][0] + 1j * locations[0][1])) != len(all_points):
    print('path not continuous')


start_pt = first_inner_pt(locations, all_points)
print(f'start location: {start_pt}')
inner_points = find_inner_points(start_pt)

# Inner points and edges, excluding the given corner points
# green_tiles = set(inner_points)
# for point in outer_edges:
#     green_tiles.add(point[0] + 1j * point[1])
green_tiles = inner_points | {p[0] + 1j * p[1] for p in outer_edges}
red_tiles = {p[0] + 1j * p[1] for p in locations}


# Check if the area is continuous
def valid_location(p1, p2, all_tiles):
    min_x, max_x = [int(func(p1.real, p2.real)) for func in [min, max]]
    min_y, max_y = [int(func(p1.imag, p2.imag)) for func in [min, max]]
    for ix in range(min_x, max_x):
        for jy in range(min_y, max_y):
            pt = ix + 1j * jy
            if pt not in all_tiles:
                return False
    return True


all_tiles = green_tiles | red_tiles
max_area = [None, None, 0]
for p1 in red_tiles:
    for p2 in red_tiles:
        if p1 == p2:
            continue

        if not valid_location(p1, p2, all_tiles):
            continue

        rect = (abs(p1.real - p2.real) + 1) * (abs(p1.imag - p2.imag) + 1)
        if rect > max_area[2]:
            max_area = [p1, p2, rect]

print(max_area)

print_grid()
