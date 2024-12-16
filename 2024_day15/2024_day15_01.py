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

def within_bounds(location, boundaries):
    loc_re, loc_im = j2c(location)

    if loc_re == 0 or loc_re == grid_shape[0] - 1:
        return False
    if loc_im == 0 or loc_im == grid_shape[1] - 1:
        return False

    if location in boundaries:
        return False

    return True

# Complex to coordinate
def j2c(p):
    return int(np.real(p)), int(np.imag(p))

def show_map(robot, boundaries, boxes):
    grid = np.full((grid_shape[0], grid_shape[1]), '.')

    for iT, thing in enumerate([boundaries, boxes, [robot]]):
        for item in thing:
            grid[j2c(item)] = {0:'#', 1:'O', 2:'@'}[iT]
    grid[0, :] = '#'
    grid[grid_shape[0] - 1, :] = '#'
    grid[:, 0] = '#'
    grid[:, grid_shape[1] - 1] = '#'

    show_grid(grid)


filename = '2024_day15/test_input1.txt'
filename = '2024_day15/test_input2.txt'
# filename = '2024_day15/input.txt'
with open(filename) as f_in:
    lines = f_in.readlines()

split_idx = lines.index('\n')
grid = np.array([[v for v in line.strip()] for line in lines[0:split_idx]])
grid_shape = grid.shape
actions = [v for v in ''.join([line.strip() for line in lines[split_idx+1:]])[::-1]]

boundaries, robot, boxes = [[int(x) + 1j*int(y) for x, y in zip(*np.where(np.isin(grid, c)))] for c in ['#', '@', 'O']]
boundaries = [b for b in boundaries if within_bounds(b, [])]
robot = robot[0]
# show_map(robot, boundaries, boxes)

action_directions = {'^':-1, '>':1j, 'v':1, '<':-1j}

while actions:
    # show_map(robot, boundaries, boxes)
    action = actions.pop()
    action_direction = action_directions[action]
    next_position = robot + action_direction
    print(f'Move {action}: {next_position}')

    # Next position is a box
    if next_position in boxes:
        next_box_position = next_position + action_direction
        boxes_to_move = [[next_position, boxes.index(next_position)]]
        while next_box_position in boxes:
            boxes_to_move.append([next_box_position, boxes.index(next_box_position)])
            next_box_position = next_box_position + action_direction
        print(f'\tMoving {len(boxes_to_move)} boxes: {[b[0] for b in boxes_to_move]}')

        if within_bounds(next_box_position, boundaries):
            while boxes_to_move:
                box, box_idx = boxes_to_move.pop()
                print(f'\tMoving box from {box} to {next_box_position}')
                boxes[box_idx] = next_box_position
                next_box_position -= action_direction
            robot = next_position
            print(f'\tMoving robot from {robot} to {next_position}')
        else:
            print(f'\tBox at {next_position} cannot move')
        continue

    # Robot moves
    if not within_bounds(next_position, boundaries):
        # Robot hits a wall
        print(f'\tRobot hits wall at {next_position}')
        continue
    robot = next_position
    print(f'\tMoving robot from {next_position} to {next_position}')
    # break

show_map(robot, boundaries, boxes)
gps = sum([np.real(box) * 100 + np.imag(box) for box in boxes])
print(f'GPS: {gps}')