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


def show_map(start, end, boundaries, path=None):
    grid = np.full((grid_shape[0], grid_shape[1]), '.')

    if path is not None:
        for p in path:
            grid[j2c(p[0])] = '*'
    grid[j2c(start)] = 'S'
    grid[j2c(end)] = 'E'

    for iX in range(grid.shape[0]):
        for iY in range(grid.shape[1]):
            if not within_bounds(iX + 1j*iY, boundaries):
                grid[j2c(iX + 1j*iY)] = '#'


    show_grid(grid)


def get_adjacent(current_position):
    adjacent = []
    for direction in [-1, 1, -1j, 1j]:
        next_position = current_position + direction
        if within_bounds(next_position, boundaries):
            adjacent.append([next_position, direction])
    return adjacent


def traverse_grid(start_location, end_location):
    frontier = queue.Queue()
    frontier.put((start_location, None))
    came_from = {(start_location, None):None}
    while not frontier.empty():
        current_location, current_direction = frontier.get()
        if current_location == end_location:
            continue

        for next_location, next_direction in get_adjacent(current_location):
            if (next_location, next_direction) not in came_from:
                # current_direction = next_location - current_location
                came_from[(next_location, next_direction)] = (current_location, current_direction)
                frontier.put((next_location, next_direction))

    end_locations = [(node, direction) for (node, direction), _ in came_from.items() if node == end_location]
    paths = []
    for end in end_locations:
        # current_node = end_location
        # current_direction = end_direction
        # path = [(current_node, end_direction)]
        # while current_node != start_location:
        #     current_node, current_direction = came_from[(current_node, current_direction)]
        #     path.append((current_node, current_direction))
        # paths.append(path)
        rebuild_path(end, start_location, came_from, [], paths)

    return paths

def rebuild_path(current, start_location, came_from, path, all_paths):
    current_location, current_direction = current
    path.append((current_location, current_direction))

    if current_location == start_location:
        all_paths.append(path)
        return

    previous = came_from[current]
    # for previous in [(node, direction) for (node, direction), _ in came_from.items() if node == current_location]:
    if previous is not None:
        rebuild_path(previous, start_location, came_from, path, all_paths)


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
start, end = start[0], end[0]
show_map(start, end, boundaries)

paths = traverse_grid(start, end)
for path in paths:
    show_map(start, end, boundaries, path )