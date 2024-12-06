import numpy as np 
import heapq

def print_grid(grid):
    print('     ', end = '')
    print(''.join([f'{i:^3}' for i in range(grid.shape[0])]))
    print('   ', end = '')
    print(''.join(['---' for i in range(grid.shape[0])]))
    for iR, row in enumerate(grid):
        print(f'{iR:^2} | ', end = '')
        print(''.join([f'{c:^3}' for c in row]))

def get_direction(current_node, previous_node):
    direction = (current_node[0] - previous_node[0]) + 1j*(current_node[1] - previous_node[1])
    return direction

def add_tuples(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])


with open('test_input3.txt') as f_in:
    grid = np.array([[int(c) for c in line.strip()] for line in f_in.readlines()])

start_node = (0, 0)
end_node = (grid.shape[0] - 1, grid.shape[1] - 1)

frontier = []
heapq.heappush(frontier, (0, start_node))
came_from = {start_node:None}
cost_so_far = {start_node:0}

visited_grid = np.full(grid.shape, '.')


# heat_loss = []
# test_grid = np.full(grid.shape, '.')
# current_node = end_node
# while current_node != start_node:
#     heat_loss.append(grid[current_node])
#     test_grid[current_node] = grid[current_node]
#     current_node = came_from[current_node]
# test_grid[current_node] = grid[current_node]  
# # heat_loss += grid[current_node]
# heat_loss.append(grid[current_node])
# print_grid(test_grid)
# print(f'\n{heat_loss[::-1]}')
# print(f'Heat Loss: {np.sum(heat_loss)}')
