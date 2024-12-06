import numpy as np 
import heapq

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
    # Top of grid
    if node[0] < 0: 
        return False
    
    # Left side of grid
    if node[1] < 0: 
        return False
    
    # Bottom of grid
    if node[0] >= grid.shape[0]:
        return False
    
    if node[1] >= grid.shape[1]:
        return False
    
    return True

def line_too_long(current_node, previous_node, came_from):
    if previous_node is None:
        return False

    directions = [get_direction(current_node, previous_node)]
    for i in range(3):
        current_node = previous_node   
        previous_node = came_from[current_node]
        # previous_node = came_from[(current_node, directions[-1])]
        if previous_node is None:
            return False
        direction = get_direction(current_node, previous_node)        
        directions.append(direction)
    if len(set(directions)) == 1:
        return True
    else:
        return False

def heuristic(grid, end_node, next_node):
    return 0

def get_next_nodes(grid, current_node, direction, straight_count):
    next_nodes = []
    if direction is None:
        next_nodes.append(((current_node[0] + 1, current_node[1]), 'S', 1))
        next_nodes.append(((current_node[0], current_node[1] + 1), 'E', 1))
    else:
        # Turning left and right
        turns = {'N':[(0, 1), (0, -1)],
                 'S':[(0, 1), (0, -1)],
                 'E':[(1, 0), (-1, 0)],
                 'W':[(1, 0), (-1, 0)]}
        # Part 2: Only turn if we've been going 4 nodes 
        if straight_count >= 4:
            for idx_offset in turns[direction]:
                next_node = add_tuples(current_node, idx_offset)

                # Check bounds
                if check_bounds(grid, next_node):            
                    next_direction = get_direction(current_node=next_node, previous_node=current_node)
                    # Straight count becomes 1 if we turn
                    next_nodes.append((next_node, next_direction, 1))

        # Check line length if going straight 
        if straight_count < 10:
            straight = {'N':(-1, 0),
                        'S':(1, 0),
                        'E':(0, 1),
                        'W':(0, -1)}
            next_node = add_tuples(current_node, straight[direction])

            # Check bounds
            if check_bounds(grid, next_node): 
                next_direction = get_direction(current_node=next_node, previous_node=current_node)
                next_nodes.append((next_node, next_direction, straight_count + 1))
    return next_nodes


with open('input.txt') as f_in:
    grid = np.array([[int(c) for c in line.strip()] for line in f_in.readlines()])

start_node = (0, 0)
start_state = (start_node, None, 0)
end_node = (grid.shape[0] - 1, grid.shape[1] - 1)

frontier = []
heapq.heappush(frontier, (0, start_state))
came_from = {start_state:None}
cost_so_far = {start_state:0}

while frontier:
    current_priority, current_state = heapq.heappop(frontier)
    current_node, direction, straight_count = current_state

    # I don't think we need this?
    # if current_node == end_node:
    #     # Part 2
    #     if straight_count >= 4:
    #         break

    for next_state in get_next_nodes(grid, current_node, direction, straight_count):
        next_node, next_direction, next_straight_count = next_state
        # print(next_state)
        next_cost = cost_so_far[current_state] + grid[current_node]
        if next_state not in cost_so_far or next_cost < cost_so_far[next_state]:
            cost_so_far[next_state] = next_cost
            priority = next_cost 
            heapq.heappush(frontier, (priority, next_state))
            came_from[next_state] = current_state

# Part 1
min_state = None
min_cost = np.max([v for k, v in cost_so_far.items()])
for (current_state, cost) in cost_so_far.items():
    current_node, direction, straight_length = current_state
    if current_node == end_node:
        if cost < min_cost:
            # Part 2 
            if straight_length >= 4:
                min_cost = cost
                min_state = current_state
                print(f'{current_state}, {cost}')
print()

heat_loss = []
test_grid = np.full(grid.shape, '.')
current_state = min_state
test_grid[current_state[0]] = grid[current_state[0]]
heat_loss.append(grid[current_state[0]])
while current_state != start_state:
    # print(current_state)
    next_state = came_from[current_state]
    current_node, direction, straight_length = next_state
    test_grid[current_node] = grid[current_node]
    heat_loss.append(grid[current_node])
    current_state = next_state

del heat_loss[-1]

# print_grid(test_grid)
# print(f'\n{heat_loss[::-1]}')
print(f'Heat Loss: {np.sum(heat_loss)}')








