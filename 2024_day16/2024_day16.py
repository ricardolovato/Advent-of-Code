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

    if loc_re in [0] or loc_re == grid_shape[0] - 1:
        return False
    if loc_im in [0] or loc_im == grid_shape[1] - 1:
        return False

    if location in boundaries:
        return False

    return True


def show_map(start, end, boundaries):
    grid = np.full((grid_shape[0], grid_shape[1]), '.')

    grid[j2c(start)] = 'S'
    grid[j2c(end)] = 'E'

    for iX in range(grid.shape[0]):
        for iY in range(grid.shape[1]):
            if not within_bounds(iX + 1j*iY, boundaries):
                grid[j2c(iX + 1j*iY)] = '#'

    show_grid(grid)

# def BFS(start_position, end_position):
#     paths = []
#     explored = {}
#     Q = queue.Queue()
#     explored[start_position] = 0
#     Q.put(start_position)
#     while not Q.empty():
#         position = Q.get()
#         if position == end_position:
#             paths.append(position)
#
#         for edge in get_edges(position):
#             if edge not in explored or explored[edge] == len(paths):
#                 explored[edge] = len(paths)
#                 Q.put(edge)
#     return paths

def get_adjacent(current_position):
    adjacent = []
    for direction in [-1, 1, -1j, 1j]:
        next_position = current_position + direction
        if within_bounds(next_position, boundaries):
            adjacent.append([next_position, direction])
    return adjacent

def DFS(current_position, current_direction, end_position, explored):
    explored.append([current_position, current_direction])

    adjacent_cells = get_adjacent(current_position)
    for (adjacent_cell, adjacent_direction) in adjacent_cells:
        if adjacent_cell not in explored:
            DFS(adjacent_cell, adjacent_direction, end_position, explored)


# Complex to coordinate
def j2c(p):
    return int(np.real(p)), int(np.imag(p))

filename = '2024_day16/test_input1.txt'
# filename = '2024_day15/test_input2.txt'
# filename = '2024_day15/input.txt'
with open(filename) as f_in:
    lines = f_in.readlines()

grid = np.array([[v for v in line.strip()] for line in lines])
grid_shape = grid.shape

start, end, boundaries = [[int(x) + 1j*int(y) for x, y in zip(*np.where(np.isin(grid, c)))] for c in ['S', 'E', '#']]
boundaries = [b for b in boundaries if within_bounds(b, [])]
show_map(start, end, boundaries)

