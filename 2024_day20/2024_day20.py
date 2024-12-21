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

    if loc_re == 0 or loc_re == grid_shape[0] - 1:
        return False
    if loc_im == 0 or loc_im == grid_shape[1] - 1:
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


def get_adjacent(current_position, boundaries):
    adjacent = []
    for direction in [-1, 1, -1j, 1j]:
        next_position = current_position + direction
        if within_bounds(next_position, boundaries):
            adjacent.append(next_position)
    return adjacent


# Complex to coordinate
def j2c(p):
    return int(np.real(p)), int(np.imag(p))


def traverse_grid(current, start, end, boundaries, visited=None):
    if visited is None:
        visited = {current:None}
    q = queue.Queue()
    q.put(current)
    while not q.empty():
        current_position = q.get()
        if current_position == end:
            break

        for adjacent in get_adjacent(current_position, boundaries):
            if adjacent not in visited:
                q.put(adjacent)
                visited[adjacent] = current_position

    return rebuild_path(start, end, visited)


def rebuild_path(start, end, visited):
    path = []
    current_position = end
    while current_position != start:
        path.append(current_position)
        current_position = visited[current_position]
    path.append(current_position)
    return path[::-1]


def get_surrounding(current_point, boundaries, path):
    pts = []
    for direction in [-1, 1, 1j, -1j]:
        next_position = current_point + direction
        # if within_bounds(next_position, []):
        if next_position in boundaries:
            # pts.append(next_position)
            for d2 in [-1, 1, 1j, -1j]:
                end_position = next_position + d2
                if end_position in path and end_position != current_point:
                    pts.append([next_position, end_position])
    return pts

# def get_surrounding(current_point, boundaries):
#     pts = []
#     for iX in range(int(np.real(current_point)) - 2, int(np.real(current_point)) + 3):
#         for iY in range(int(np.imag(current_point)) - 2, int(np.imag(current_point)) + 3):
#             pt = iX + 1j * iY
#             if within_bounds(pt, []):
#                 pts.append(pt)
#
#     combos = []
#     for pt1 in pts:
#         for pt2 in pts:
#             if pt1 == pt2:
#                 continue
#
#             # Points must be boundary points
#             # if all([pt in boundaries for pt in [pt1, pt2]]):
#             # if len([pt for pt in [pt1, pt2] if pt in boundaries]) == 1:
#             # Must start on a wall and end on a track
#             if pt1 in boundaries and pt2 not in boundaries:
#                 # Points must be adjacent
#                 if any([pt1 + direction == pt2 for direction in [1, -1, 1j, -1j]]):
#                     # if [pt1, pt2] not in combos and [pt2, pt1] not in combos:
#                     combos.append([pt1, pt2])
#     return combos


filename = '2024_day20/test_input1.txt'
# filename = '2024_day20/test_input2.txt'
filename = '2024_day20/input.txt'
with open(filename) as f_in:
    lines = f_in.readlines()

grid = np.array([[v for v in line.strip()] for line in lines])
grid_shape = grid.shape

start, end, boundaries = [[int(x) + 1j*int(y) for x, y in zip(*np.where(np.isin(grid, c)))] for c in ['S', 'E', '#']]
boundaries = [b for b in boundaries if within_bounds(b, [])]
start, end = start[0], end[0]
show_map(start, end, boundaries)

path = traverse_grid(start, start, end, boundaries)
show_map(start, end, boundaries, path)

path_lengths = {}
visited = {start:None}
# for next_idx in range(1, idx + 1):
#     visited[path[next_idx]] = path[next_idx - 1]

for idx in range(1, len(path)):
    print(f'{idx}/{len(path)}')
    visited[path[idx]] = path[idx - 1]
    current_pt = path[idx]
    for cheat_pts in get_surrounding(current_pt, boundaries, path):
        current_bounds = [b for b in boundaries if b not in cheat_pts]

        # visited = {start: None}
        # for next_idx in range(1, idx + 1):
        #     visited[path[next_idx]] = path[next_idx - 1]
        current_path = traverse_grid(current_pt,
                                     start,
                                     end,
                                     current_bounds,
                                     {k:v for k, v in visited.items()})
        path_lengths[tuple(cheat_pts)] = len(path) - len(current_path)

    if idx == 10:
        break

# for test_val in [2, 4, 6, 8, 10, 12, 20, 36, 38, 40, 64]:
#     num_items = len([k for k, v in path_lengths.items() if v == test_val])
#     print(f'{test_val}: {num_items}')

num_items = len([k for k, v in path_lengths.items() if v >= 100])
print(num_items)