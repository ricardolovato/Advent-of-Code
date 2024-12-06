import numpy as np

def print_grid(grid):
    print('     ', end = '')
    print(''.join([f'{i:^3}' for i in range(grid.shape[1])]))
    print('   ', end = '')
    print(''.join(['---' for i in range(grid.shape[1])]) + '-')
    for iR, row in enumerate(grid):
        print(f'{iR:^2} | ', end = '')
        print(''.join([f'{c:^3}' for c in row]))

def add_tuples(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])

def is_adjacent(grid, current_node, previous_nodes):
    for idx_offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if add_tuples(current_node, idx_offset) in previous_nodes:
            return True
    else:
        return False
    
with open('test_input.txt') as f_in:
    inner_grid = np.array([[c for c in line.strip()] for line in f_in.readlines()])
grid = np.full((inner_grid.shape[0] + 2, inner_grid.shape[1] + 2), '#')
grid[1:-1, 1:-1] = inner_grid

start_node = np.where(grid == 'S')
start_node = (start_node[0][0], start_node[1][0])
grid[start_node] = '.'

previous_nodes = [start_node]
num_steps = 2
for current_step in range(num_steps - 1, num_steps + 1):
    nodes = set()
    test_grid = np.array(grid)

    corner_nodes = {add_tuples(start_node, (0, current_step)):(1, 1),        # north to east
                    add_tuples(start_node, (current_step, 0)):(1, -1),   # east to south 
                    add_tuples(start_node, (0, -1 * current_step)):(-1, -1), # south to west
                    add_tuples(start_node, (-1 * current_step, 0)):(-1, 1), } # west to north

    # Start at north
    current_node = add_tuples(start_node, (-1 * current_step, 0))
    if grid[current_node] != '#' and is_adjacent(grid, current_node, previous_nodes):
        nodes.add(current_node)
    for next_corner, idx_offset in corner_nodes.items():
        while current_node != next_corner:
            current_node = add_tuples(current_node, idx_offset)
            if grid[current_node] != '#' and is_adjacent(grid, current_node, previous_nodes):
                nodes.add(current_node)

    # test_grid = np.array(grid)
    for current_node in nodes:
        test_grid[current_node] = f'{current_step}'

    previous_nodes = nodes
        
    test_grid[start_node] = 'S'
    print_grid(test_grid)
    print(f'step {current_step}: {len(nodes)}')
