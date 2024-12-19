import numpy as np
import queue

def show_grid(grid):
    print('     ', end='')
    print(''.join([f'{i:^3}' for i in range(grid.shape[1])]))
    print('   ', end='')
    print(''.join(['---' for i in range(grid.shape[1])]) + '-')
    for iR, row in enumerate(grid):
        print(f'{iR:^2} | ', end='')
        print(''.join([f'{c:^3}' for c in row]))
    print('     ', end='')
    print(''.join(['---' for i in range(grid.shape[1])]) + '-')
    print('     ', end='')
    print(''.join([f'{i:^3}' for i in range(grid.shape[1])]))


def within_bounds(location, boundaries):
    loc_re, loc_im = j2c(location)

    if loc_re in [-1] or loc_re == grid_shape[0]:
        return False
    if loc_im in [-1] or loc_im == grid_shape[1]:
        return False

    if location in boundaries:
        return False

    return True


def show_map(start, end, boundaries, path=None):
    grid = np.full((grid_shape[0], grid_shape[1]), '.')

    if path is not None:
        for p in path:
            grid[j2c(p)] = '*'
    grid[j2c(start)] = 'S'
    grid[j2c(end)] = 'E'

    for iX in range(grid.shape[0]):
        for iY in range(grid.shape[1]):
            if not within_bounds(iX + 1j*iY, boundaries):
                grid[j2c(iX + 1j*iY)] = '#'
    show_grid(grid)

# Complex to coordinate
def j2c(p):
    return int(np.real(p)), int(np.imag(p))

def get_adjacent(position, boundaries):
    edges = []
    for direction in [-1, 1, -1j, 1j]:
        if within_bounds(position + direction, boundaries):
            edges.append(position + direction)
    return edges

def traverse_grid(start, end, boundaries):
    came_from = {start:None}
    frontier = queue.Queue()
    frontier.put(start)
    while not frontier.empty():
        current = frontier.get()
        if current == end:
            break

        for adjacent in get_adjacent(current, boundaries):
            if adjacent not in came_from:
                came_from[adjacent] = current
                frontier.put(adjacent)

    if end not in came_from:
        return None

    path = [end]
    position = end
    while position != start:
        position = came_from[position]
        path.append(position)
    return path

# filename = '2024_day18/test_input1.txt'
# grid_shape = (7, 7)
# end_byte = 12

filename = '2024_day18/input.txt'
grid_shape = (71, 71)
end_byte = 1024

with open(filename) as f_in:
    lines = f_in.readlines()

boundaries = [int(imag) + 1j*int(real)  for line in lines for real, imag in [line.strip().split(',')]]
boundaries = boundaries[0:end_byte]
start = 0
end = grid_shape[0]-1 + 1j * (grid_shape[1] - 1)
show_map(start, end, boundaries)
path = traverse_grid(start, end, boundaries)
show_map(start, end, boundaries, path)
print(len(path) - 1)

# Part 2 - binary search
boundaries = [int(imag) + 1j*int(real)  for line in lines for real, imag in [line.strip().split(',')]]
path = []
L = end_byte
R = len(boundaries)-1
while L != R:
    bounds_idx = (L + R) // 2
    print(f'L: {L}, R: {R}, bounds_idx: {bounds_idx}\t', end = '')
    current_bounds = boundaries[0:bounds_idx ]
    path = traverse_grid(start, end, current_bounds)

    if path is None:
        print(f'--> no path')
        # Too big: search backwards
        R = bounds_idx - 1
    else:
        print(f'--> yes path')
        L = bounds_idx + 1
bounds_idx = (L + R) // 2
print(f'bounds_idx: {bounds_idx} -> {lines[bounds_idx - 1]}')

# 2,12 wrong
