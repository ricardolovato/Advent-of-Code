import numpy as np
def in_bounds(point, shape):
    if np.real(point) < 0:
        return False
    elif np.real(point) >= shape[0]:
        return False
    elif np.imag(point) < 0: 
        return False
    elif np.imag(point) >= shape[1]:
        return False
    return True

def check_adjacent(point, grid, shape) -> bool:
    for direction in [1j, -1, -1j, 1]:
        adj_point = point + direction
        
        # Don't break, corner points are candidates
        if not in_bounds(adj_point, shape):
            continue

        if grid[point] >= grid[adj_point]:
            return False 
    return True

filename = '2021_day09/test_input.txt'
# filename = '2021_day09/test_input2.txt'
filename = '2021_day09/input.txt'
with open(filename) as f_in:
    lines = [[int(c) for c in line.strip()] for line in f_in.readlines()]

shape = (len(lines), len(lines[0]))

grid = {}
for i in range(len(lines)):
    for j in range(len(lines[0])):
        grid[i+j*1j] = lines[i][j]

low_points = []
risk_level = 0
for point, height in grid.items():
    if check_adjacent(point, grid, shape):
        print(f'{point} ({height}): {check_adjacent(point, grid, shape)}')
        risk_level += 1 + height
        low_points.append(point)
print(risk_level)

def BFS(point, grid, visited = None):
    if visited is None:
        visited = []
    visited.append(point)
    for direction in [1j, -1, -1j, 1]:
        adj_point = point + direction
        if adj_point in visited: 
            continue
        
        if not in_bounds(adj_point, shape):
            continue

        if grid[adj_point] == 9: 
            continue

        visited = BFS(adj_point, grid, visited)
    return visited

sizes = []
for point in low_points:
    v = BFS(point, grid)
    # print(f'{point}: {len(v)}')
    sizes.append(len(v))

p = 1
for _p in (sorted(sizes)[::-1][0:3]):
    p *= _p
print(p)