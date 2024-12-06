import numpy as np
import heapq
import math

def print_grid(grid):
    print('     ', end = '')
    print(''.join([f'{i:^3}' for i in range(grid.shape[1])]))
    print('   ', end = '')
    print(''.join(['---' for i in range(grid.shape[1])]) + '-')
    for iR, row in enumerate(grid):
        print(f'{iR:^2} | ', end = '')
        print(''.join([f'{c:^3}' for c in row]))

def get_direction(current_node, previous_node):
    direction = (current_node[0] - previous_node[0], current_node[1] - previous_node[1])
    return {(0, 1):'E', (0, -1):'W', (1, 0):'S', (-1, 0):'N'}[direction]

def add_tuples(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])

def check_bounds(grid, node):
    if grid[node] == '#':
        return False
    
    return True

# def get_next_nodes(grid, current_node, direction, straight_count):
def get_next_nodes(grid, current_node, straight_count):
    next_nodes = []
    for idx_offset in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        next_node = add_tuples(current_node, idx_offset)

        # Check bounds
        if check_bounds(grid, next_node):
            next_nodes.append((next_node, straight_count + 1))

    return next_nodes

def traverse_grid(grid, num_steps):
    start_node = (grid.shape[0] // 2, grid.shape[1] // 2)
    grid[start_node] = '.'
    start_state = (start_node, 0)

    frontier = []
    heapq.heappush(frontier, (0, start_state))
    came_from = {start_state:None}

    while frontier:
        current_priority, current_state = heapq.heappop(frontier)
        current_node, straight_count = current_state

        if straight_count == num_steps:
            continue

        for next_state in get_next_nodes(grid, current_node, straight_count):
            next_node, next_straight_count = next_state
            if next_state not in came_from:
                priority = 1
                heapq.heappush(frontier, (priority, next_state))
                came_from[next_state] = current_state
    
    nodes = set()
    for (current_state, _) in came_from.items():
        current_node, straight_length = current_state
        if straight_length == num_steps:
            nodes.add(current_node)

    return nodes

def get_grid(expand_grid=0):
    with open('test_input.txt') as f_in:
        grid = np.array([[c for c in line.strip()] for line in f_in.readlines()])

    new_shape = ((2 * expand_grid + 1) * grid.shape[0], (2 * expand_grid + 1) * grid.shape[1])
    new_grid = np.full(new_shape, '#')
    for col_idx in range(0, 2 * expand_grid + 1):
        for row_idx in range(0, 2 * expand_grid + 1):
            new_grid[row_idx * grid.shape[0]:(row_idx + 1) * grid.shape[0],
                    col_idx * grid.shape[1]:(col_idx + 1) * grid.shape[1]] = grid
    new_grid[np.where(new_grid == 'S')] = '.'
    new_grid[(new_grid.shape[0] // 2, new_grid.shape[1] // 2)] = 'S'
    # print_grid(new_grid)

    grid = np.full((new_grid.shape[0] + 2, new_grid.shape[1] + 2), '#')
    grid[1:-1, 1:-1] = new_grid
    return grid 


# https://en.wikipedia.org/wiki/Lagrange_polynomial
def interpolate(x, pts):
    x_, y_ = [[p[i] for p in pts] for i in range(2)]
    l_ = [math.prod([(x - xj)/(xi - xj) for j, xj in enumerate(x_) if j != i]) for i, xi in enumerate(x_)]

    return sum([y * l for y, l in zip(y_, l_)])


grid = get_grid(expand_grid=0)
num_steps = 6
expand_grid = (num_steps // grid.shape[0]) + 2
grid = get_grid(expand_grid=expand_grid)
print(f'Num steps = {num_steps}; expanding grid to {grid.shape}')

# Too slow for part 2 
nodes = traverse_grid(grid, num_steps=num_steps)
print(len(nodes)) 

# test_grid = np.array(grid)
# for current_node in nodes:
#     test_grid[current_node] = 'O'
# print_grid(test_grid)
# print(len(nodes)) 


# Don't expand the grid 
with open('input.txt') as f_in:
    grid = np.array([[c for c in line.strip()] for line in f_in.readlines()])

num_steps = 500

A = []
B = []
coefficient_idx = 0
points = {(grid.shape[0] // 2, grid.shape[1] // 2)}
for current_num_steps in range(1, num_steps + 1):
    visited = set()
    for point in points:
        for idx_offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            p = add_tuples(point, idx_offset)
            if grid[p[0] % grid.shape[0], p[1] % grid.shape[1]] != '#':
                visited.add(p)
    points = visited

    # if current_num_steps in [6, 10, 50, 100]:
    # print(f'{current_num_steps}: {len(visited)}')

    if current_num_steps in [(grid.shape[0] // 2) + grid.shape[0] * n for n in range(3)]:
        print(f'{current_num_steps}: {len(visited)}')
        # Ax^2 + Bx + c
        A.append([current_num_steps**2, current_num_steps, 1])
        # = A(x)
        B.append(len(visited))
        coefficient_idx += 1
        if coefficient_idx == 3:
            break

# a, b, c = np.dot(np.linalg.inv(A), B)
pts = [(a, b) for a, b in zip([_A[1] for _A in A], B)]

n = 26501365 // grid.shape[0]
x = grid.shape[0] // 2 + n * grid.shape[0]
print(f'\n{x}: {interpolate(x, pts)}')


# # Testing the interpolation 
# import matplotlib.pyplot as plt
# _x = np.arange(-4, 4, 0.05)
# plt.plot(_x, list(map(lambda v: v**2, _x)))

# pts = [(1, 1), (2, 4), (3, 9)]

# y = [interpolate(x=v, pts=pts) for v in _x]
# plt.plot(_x, y)




