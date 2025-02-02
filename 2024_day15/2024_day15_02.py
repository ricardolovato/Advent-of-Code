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


def within_bounds_original(location, boundaries):
    loc_re, loc_im = j2c(location)

    if loc_re in [0] or loc_re == grid_shape[0] - 1:
        return False
    if loc_im in [0] or loc_im == grid_shape[1] - 1:
        return False

    if location in boundaries:
        return False

    return True

def within_bounds(location, boundaries):
    if type(location) != list:
        location = [location]

    b_within = True
    for loc in location:
        loc_re, loc_im = j2c(loc)

        if loc_re == 0 or loc_re == grid_shape[0] - 1:
            b_within = False
        if loc_im in [0, 1] or loc_im in [grid_shape[1] - 1, grid_shape[1] - 2]:
            b_within = False

        if loc in boundaries:
            b_within = False

    return b_within


# Complex to coordinate
def j2c(p):
    return int(np.real(p)), int(np.imag(p))


def show_map(robot, boundaries, boxes):
    grid = np.full((grid_shape[0], grid_shape[1]), '.')

    for iT, thing in enumerate([boundaries, boxes, [robot]]):
        for item in thing:
            if iT == 1:
                grid[j2c(item[0])] = '['
                grid[j2c(item[1])] = ']'
            else:
                grid[j2c(item)] = {0:'#', 1:'O', 2:'@'}[iT]

    for iX in range(grid.shape[0]):
        for iY in range(grid.shape[1]):
            if not within_bounds(iX + 1j*iY, boundaries):
                grid[j2c(iX + 1j*iY)] = '#'

    show_grid(grid)


def get_next_box_positions(action, next_positions):
    if type(next_positions) != list:
        next_positions = [next_positions]

    test_boxes = []
    for next_position in next_positions:
        if action == '<':
            box_positions = [[next_position - 1j, next_position]]
        elif action == '^':
            box_positions = [[next_position, next_position + 1j],
                             [next_position - 1j, next_position]]
        elif action == '>':
            box_positions = [[next_position, next_position + 1j]]
        elif action == 'v':
            box_positions = [[next_position - 1j, next_position],
                             [next_position, next_position + 1j]]
        b_in_boxes = [p in boxes for p in box_positions]
        if any(b_in_boxes):
            test_boxes.append(box_positions[b_in_boxes.index(True)])
    if test_boxes:
        return test_boxes
    return None

def get_vertical_boxes(current_position, action_direction):
    if current_position in boxes:
        left = get_vertical_boxes(current_position=[p + action_direction + 1j for p in current_position],
                       action_direction=action_direction)
        right = get_vertical_boxes(current_position=[p + action_direction - 1j for p in current_position],
                       action_direction=action_direction)
        center = get_vertical_boxes(current_position=[p + action_direction for p in current_position],
                       action_direction=action_direction)
        # return [v for v in [current_position, left, right] if v is not None]
        return [current_position] + (left or []) + (right or []) + (center or [])

    return []
filename = '2024_day15/test_input1.txt'
# filename = '2024_day15/test_input2.txt'
filename = '2024_day15/input.txt'
with open(filename) as f_in:
    lines = f_in.readlines()

split_idx = lines.index('\n')
grid = np.array([[v for v in line.strip()] for line in lines[0:split_idx]])
grid_shape = grid.shape
actions = [v for v in ''.join([line.strip() for line in lines[split_idx+1:]])[::-1]]

boundaries, robot, boxes = [[int(x) + 1j*int(y) for x, y in zip(*np.where(np.isin(grid, c)))] for c in ['#', '@', 'O']]
boundaries = [b for b in boundaries if within_bounds_original(b, [])]
robot = robot[0]
# show_map(robot, boundaries, boxes)

# Update positions to new grid
grid_shape = (grid.shape[0], grid.shape[1] * 2)
boundaries = [[np.real(p) + 2j * np.imag(p), np.real(p) + 2j * np.imag(p) + 1j] for p in boundaries if within_bounds(p, [])]
boundaries = [b for boundary in boundaries for b in boundary]
boxes = [[np.real(b) + 2j * np.imag(b), np.real(b) + 2j * np.imag(b) + 1j] for b in boxes]
robot = np.real(robot) + 2j * np.imag(robot)
# show_map(robot, boundaries, boxes)

action_directions = {'^':-1, '>':1j, 'v':1, '<':-1j}


while actions:
    # show_map(robot, boundaries, boxes)
    action = actions.pop()

    action_direction = action_directions[action]
    next_position = robot + action_direction
    print(f'Move {action}: {robot} -> {next_position}')

    current_box_position = get_next_box_positions(action, next_position)

    # Next position is a box
    if current_box_position:
        current_box_position = current_box_position[0]
        next_box_position = [p + action_direction for p in current_box_position]
        boxes_to_move = [[current_box_position, next_box_position, boxes.index(current_box_position)]]

        if action in ['<', '>']:
            next_box = [p + 2 * action_direction for p in current_box_position]
            while next_box in boxes:
                boxes_to_move.append([next_box,
                                      [p + action_direction for p in next_box],
                                      boxes.index(next_box)])
                next_box = [p + 2 * action_direction for p in next_box]
        else:
            next_boxes = get_vertical_boxes(current_box_position, action_direction)
            while next_boxes:
                next_box = next_boxes.pop()
                boxes_to_move.append([next_box,
                                      [b + action_direction for b in next_box],
                                      boxes.index(next_box)])

        print(f'\tMoving {len(boxes_to_move)} boxes: {[b[0] for b in boxes_to_move]}')

        if all([within_bounds(next_box_position, boundaries) for _, next_box_position, _ in boxes_to_move]):
            # if within_bounds(next_box_position, boundaries):
            while boxes_to_move:
                current_box_position, next_box_position, box_idx = boxes_to_move.pop()
                print(f'\tMoving box from {current_box_position} to {next_box_position}')
                boxes[box_idx] = next_box_position
                next_box_position = [p - action_direction for p in next_box_position]
            print(f'\tMoving robot from {robot} to {next_position}')
            robot = next_position
        else:
            print(f'\tBox at {next_position} cannot move')
        continue

    # Robot moves
    if not within_bounds(next_position, boundaries):
        # Robot hits a wall
        print(f'\tRobot hits wall at {next_position}')
        continue
    print(f'\tMoving robot from {robot} to {next_position}')
    robot = next_position
    # break
#
show_map(robot, boundaries, boxes)
gps = sum([np.real(box[0]) * 100 + np.imag(box[0]) for box in boxes])
print(f'GPS: {gps}')