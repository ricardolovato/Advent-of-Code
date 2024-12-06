import numpy as np
import re

def print_grid(grid):
    print('     ', end = '')
    print(''.join([f'{i:^3}' for i in range(grid.shape[1])]))
    print('   ', end = '')
    print(''.join(['---' for i in range(grid.shape[1])]) + '-')
    for iR, row in enumerate(grid):
        print(f'{iR:^2} | ', end = '')
        print(''.join([f'{c:^3}' for c in row]))

def write_grid(grid):
    with open('grid.txt', 'w') as f_out:
        f_out.write('     ')
        f_out.write(''.join([f'{i:^3}' for i in range(grid.shape[1])]))
        f_out.write('\n')
        f_out.write('   ')
        f_out.write(''.join(['---' for i in range(grid.shape[1])]) + '-')
        f_out.write('\n')
        for iR, row in enumerate(grid):
            f_out.write(f'{iR:^2} | ')
            f_out.write(''.join([f'{c:^3}' for c in row]))
            f_out.write('\n')

def add_tuple(t1, t2):
    return (int(t1[0] + t2[0]), int(t1[1] + t2[1]))

# Gets all coords
def get_next_coords(current_coord, direction, length):
    direction = {'U':-1, 'D':1, 'L':-1j, 'R':1j}[direction]
    coords = []
    for current_length in range(length + 1):
        offset = direction * current_length
        coords.append(add_tuple(current_coord, (np.real(offset), np.imag(offset))))
    return coords

def get_next_vertex(current_coord, direction, length):
    direction = {'U':-1, 'D':1, 'L':-1j, 'R':1j}[direction]
    
    offset = direction * length
    return add_tuple(current_coord, (np.real(offset), np.imag(offset)))

# https://en.wikipedia.org/wiki/Shoelace_formula#Example
# Two implementations
def shoelace_area(pts):
    A = 0
    vertices = [pts[-1]] + pts + [pts[0]]
    for i in range(1, len(vertices) - 1):
        a = vertices[i][0] * (vertices[i + 1][1] - vertices[i - 1][1])
        A += a
    A = A / 2
    return A

def shoelace_area_det(pts):
    A = 0
    vertices = np.array(pts + [pts[0]]).T
    for i in np.arange(vertices.shape[1] - 1):
        segment = vertices[0:2, i:i+2]
        A += np.linalg.det(segment)
    A = A / 2
    return A
    
with open('input.txt') as f_in:
    lines = [line.strip() for line in f_in.readlines()]

max_coord = (0, 0)
min_coord = (0, 0)
current_coord = (0, 0)
layout = {}
for line in lines:
    direction, length, color = line.split(' ')
    length = int(length)

    # Part 2
    color = color[2:-1]
    length = int(f'0x{color[0:-1]}', 0)
    direction = {'0':'R', '1':'D', '2':'L', '3':'U'}[color[-1]]
    # --- 

    current_state = (direction, length, color)
    # Part 1
    # layout[current_state] = get_next_coords(current_coord, direction, length)
    layout[current_state] = [get_next_vertex(current_coord, direction, length)]
    current_coord = layout[current_state][-1]

    # Keep track of grid size     
    current_max = [max([c[i] for c in layout[current_state]]) for i in range(2)]
    max_coord = (max(max_coord[0], current_max[0]), max(max_coord[1], current_max[1]))
    
    current_min = [min([c[i] for c in layout[current_state]]) for i in range(2)]
    min_coord = (min(min_coord[0], current_min[0]), min(min_coord[1], current_min[1]))

# Disable grid visualization for part 2
x_offset, y_offset = min_coord
all_points = []
vertices = []
# grid = np.full((max_coord[0] - min_coord[0] + 1, max_coord[1] - min_coord[1] + 1), '.')
for current_state, coords in layout.items():
    for c in coords:
        c = add_tuple(c, tuple(map(abs, min_coord)))
        # grid[c] = '#'
        if c not in all_points:
            all_points.append(c)
    
    vertices.append(add_tuple(coords[0], tuple(map(abs, min_coord))))
# print_grid(grid)
# for coord in vertices:
#     grid[coord] = 'x'
# print_grid(grid)
# write_grid(grid)

# Count outer points
vertices = [vertices[-1]] + vertices
outer_length = 0
for i in range(len(vertices) - 1):
    outer_length += abs(vertices[i+1][0] - vertices[i][0])
    outer_length += abs(vertices[i+1][1] - vertices[i][1])

# https://en.wikipedia.org/wiki/Pick%27s_theorem
#  :  A = i + b/2 - 1   ->  i = A - b/2 + 1
inner_area = abs(shoelace_area(vertices))
i = inner_area - outer_length // 2 + 1
# Area = inner points + outer points
A = i + outer_length
print(A)



























