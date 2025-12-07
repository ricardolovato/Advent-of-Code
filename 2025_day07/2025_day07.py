def within_bounds(n, grid_size):
    if n is None:
        return False

    if not 0 <= n.real < grid_size[0]:
        return False
    elif not 0 <= n.imag < grid_size[1]:
        return False

    return True

def print_grid():
    print(f'\n{num_split} splits')
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            p = i + 1j*j
            if p in all_beam_positions:
                print('|', end='')
            elif p in splitters:
                print('^', end='')
            elif p == start_node:
                print('S', end='')
            else:
                print('.', end = '')
        print()
    print('-'*15)
    print()


filename = '2025_day07/test_input.txt'
filename = '2025_day07/input.txt'
with open(filename) as f_in:
    lines = [[c for c in line.strip()] for line in f_in.readlines()]

start_node = 1j*lines[0].index('S')
grid_size = (len(lines), len(lines[0]))

splitters = set()
for iR, row in enumerate(lines):
    for iC, col in enumerate(row):
        if col == '^':
            splitters.add(iR + 1j * iC)

num_split = 0
all_beam_positions = []
beams = {start_node}
while any(within_bounds(beam, grid_size) for beam in beams):
    new_beams = []
    # for iB in range(len(beams)):
    for beam in list(beams):
        if not within_bounds(beam, grid_size):
            continue
        # print([b for b in beams if b is not None])
        # print_grid()

        next_point = beam + 1
        if next_point in splitters:
            # split the beam
            for direction in [-1j, 1j]:
                new_beam = next_point + direction
                # The beam already exists
                if new_beam in beams:
                    continue

                if within_bounds(new_beam, grid_size):
                    new_beams.append(new_beam)
                    all_beam_positions.append(new_beam)
            num_split += 1
        else:
            # beam += 1
            beams.add(beam + 1)
        all_beam_positions.append(beam)
        beams.remove(beam)
    for new_beam in new_beams:
        beams.add(new_beam)
print(num_split)

# Part 2
def next_points(point):
    next_points = []
    if point in splitters:
        for direction in [-1j, 1j]:
            new_beam = point + direction

            if within_bounds(new_beam, grid_size):
                next_points.append(new_beam)
    else:
        next_points.append(point + 1)
    return next_points


# DFS, saves each path. too slow and not hashable
def beam_dfs(point, path = None):
    # path is the current path
    if path is None:
        path = [point]
    else:
        path.append(point)

    # list of all paths
    paths = []
    if point.real == grid_size[0] - 1:
        # End position is bottom row
        paths.append(path.copy())
    else:
        for current_point in next_points(point):
            current_path = beam_dfs(current_point, path)
            paths.extend(current_path)

    path.pop()
    return paths

# too slow
# visited = beam_dfs(start_node)
# print(len(visited) )

from functools import lru_cache
@lru_cache(maxsize=None)
def count_paths(point):
    if point.real == grid_size[0] - 1:
        # End position is bottom row
        return 1

    total = 0
    for current_point in next_points(point):
        total += count_paths(current_point)
    return total

num_paths = count_paths(start_node)
print(num_paths)
