import numpy as np


def print_grid():
    buff = 4
    max_x, max_y = [max([loc[i] for loc in locations]) for i in range(2)]
    with open('2025_day09/grid.txt', 'w') as f_out:
        print(f'\t', end='')
        f_out.write(f'\t')
        for jy in range(0, max_y + buff):
            print(f'{jy} ', end='')
            f_out.write(f'{jy} ')
        print()
        f_out.write('\n')
        for ix in range(0, max_x + buff):
            print(f'{ix}\t', end='')
            f_out.write(f'{ix}\t')
            for jy in range(0, max_y + buff):
                # if ix + 1j * jy in red_tiles:
                #     # print('# ', end='')
                #     f_out.write('# ')
                # elif ix + 1j * jy in green_tiles:
                #     # print('X ', end='')
                #     f_out.write('X ')
                if [ix, jy] in locations:
                    print('# ', end='')
                    f_out.write('# ')
                # # elif ix + 1j*jy in all_points:
                # #     print('@ ', end = '')
                elif [ix, jy] in outer_edges:
                    print('X ', end='')
                    f_out.write('X ')
                elif ix+1j*jy in exterior_points:
                    print('O ', end='')
                    f_out.write('X ')
                # elif ix + 1j*jy in inner_points:
                #     print('O ', end = '')
                # elif ix + 1j * jy in fence:
                #     # print('X ', end='')
                #     f_out.write('O ')
                else:
                    print('. ', end='')
                    f_out.write('. ')
            print()
            f_out.write('\n')


filename = '2025_day09/test_input.txt'
# filename = '2025_day09/test_input2.txt'
filename = '2025_day09/input.txt'
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

x_loc, y_loc = [[loc[i] for loc in locations] for i in range(2)]
# Offset by 1 to give a buffer for exterior fill; guarantees we can use 0 as start point
x_loc, y_loc = [{l:i+1 for i, l in enumerate(sorted(set(loc)))} for loc in [x_loc, y_loc]]

x_rev, y_rev =[{val:key for key, val in loc.items()} for loc in [x_loc, y_loc]]

locations = [[x_loc[loc[0]], y_loc[loc[1]]] for loc in locations]


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

x_max = int(max([p.real for p in all_points]))
y_max = int(max([p.imag for p in all_points]))

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


def find_inner_points_recursive(point, visited=None):
    if visited is None:
        visited = set()

    visited.add(point)

    for direction in [1, 1j, -1, -1j]:
        next_point = point + direction
        if next_point not in all_points and next_point not in visited:
            visited = find_inner_points_recursive(next_point, visited)
    return visited


def within_bounds(point):
    if point.real < 0 or point.imag < 0:
        return False
    
    if point.real > x_max + 1 or point.imag > y_max + 1:
        return False
    return True


def find_points(start, condition):
    visited = set()
    stack = [start]

    while stack:
        point = stack.pop()
        if point in visited:
            continue
        visited.add(point)

        for direction in [1, -1, 1j, -1j]:
            next_point = point + direction
            # if next_point not in visited and next_point not in all_points:
            if within_bounds(next_point) and condition(next_point, visited):
                stack.append(next_point)
    return visited


if len(verify_edges(locations[0][0] + 1j * locations[0][1])) != len(all_points):
    print('path not continuous')

exterior_points = find_points(0+0j,
                              lambda point, visited: point not in visited and point not in all_points)
inner_points = set()
for ix in range(0, x_max + 1):
    for jx in range(0, y_max + 1):
        current_point = ix + 1j * jx
    # if not any(ix+1j*jx in points for points in [all_points,exterior_points]):
        if current_point not in all_points and current_point not in exterior_points:
            inner_points.add(ix + 1j*jx)

# Inner points and edges, excluding the given corner points
# green_tiles = set(inner_points)
# for point in outer_edges:
#     green_tiles.add(point[0] + 1j * point[1])
green_tiles = inner_points | {p[0] + 1j * p[1] for p in outer_edges}
red_tiles = {p[0] + 1j * p[1] for p in locations}
all_tiles = green_tiles | red_tiles


# Check if the area is continuous
def valid_location(p1, p2, all_tiles):
    min_x, max_x = [int(func(p1.real, p2.real)) for func in [min, max]]
    min_y, max_y = [int(func(p1.imag, p2.imag)) for func in [min, max]]
    for ix in range(min_x, max_x+1):
        for jy in range(min_y, max_y+1):
            pt = ix + 1j * jy
            if pt not in all_tiles:
                return False
    return True


max_area = [None, None, 0]
for p1 in red_tiles:
    for p2 in red_tiles:
        if p1 == p2:
            continue

        if not valid_location(p1, p2, all_tiles):
            continue

        # rect = (abs(p1.real - p2.real) + 1) * (abs(p1.imag - p2.imag) + 1)
        # if rect > max_area[2]:
        #     max_area = [p1, p2, rect]
        p1_orig = x_rev[int(p1.real)] + 1j * y_rev[int(p1.imag)]
        p2_orig = x_rev[int(p2.real)] + 1j * y_rev[int(p2.imag)]
        rect = (abs(p1_orig.real - p2_orig.real) + 1) * (abs(p1_orig.imag - p2_orig.imag) + 1)
        # print(f'{p1}, {p2}, {rect}')
        if rect > max_area[2]:
            max_area = [p1_orig, p2_orig, rect]

print(max_area)

# print_grid()
