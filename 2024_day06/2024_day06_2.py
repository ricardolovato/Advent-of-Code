import numpy as np
import copy

filename = '2024_day06/input.txt'
# filename = '2024_day06/test_input.txt'
# filename = '2024_day06/test_input2.txt'
# filename = '2024_day06/test_input3.txt'
# filename = '2024_day06/test_input4.txt'


def print_grid(grid):
    print('     ', end='')
    print(''.join([f'{i:^3}' for i in range(grid.shape[1])]))
    print('   ', end='')
    print(''.join(['---' for i in range(grid.shape[1])]) + '-')
    for iR, row in enumerate(grid):
        print(f'{iR:^2} | ', end='')
        print(''.join([f'{c:^3}' for c in row]))


def get_next_direction(current_direction):
    direction_idx = (directions.index(current_direction) + 1) % 4
    next_direction = directions[direction_idx]
    # print(f'Current direction: {dir_char[tuple(current_direction)]}; next direction: {dir_char[tuple(next_direction)]}')
    return next_direction


def visualize_map(visited, blockers, boundary, b_last=False):
    ary = np.full(closet_map.shape, '.')

    for loc in blockers:
        ary[int(np.real(loc)), int(np.imag(loc))] = '#'
    if b_last:
        ary[int(np.real(loc)), int(np.imag(loc))] = 'O'

    for loc in boundary:
        ary[int(np.real(loc)), int(np.imag(loc))] = '@'

    # Update this with blockers and boundary and just redraw the map
    # so that the new blocker shows up
    for index, directions in visited.items():
        for direction in directions:
            x, y = int(np.real(index)), int(np.imag(index))
            if direction == 1:
                ary[x, y] = 'v'
            elif direction == -1j:
                ary[x, y] = '<'
            elif direction == -1:
                ary[x, y] = '^'
            elif direction == 1j:
                ary[x, y] = '>'

    print_grid(ary)


def traverse_grid(visited_inner, blockers_inner, start_location, start_direction, b_test=False):
    current_location = start_location + start_direction
    current_direction = start_direction
    num_loops_inner = 0
    new_blockers = []
    while current_location not in boundary:
        # if not b_test:
        # visualize_map(visited, blockers, boundary)
        # Keep rotating until the next tile is not #
        while current_location in blockers_inner:
            # Turn 90 degrees
            current_location -= current_direction
            current_direction = get_next_direction(current_direction)
            current_location += current_direction

        if current_location in visited_inner:
            if b_test and current_direction in visited_inner[current_location]:
                # print(blockers_inner[-1])
                # visualize_map(visited_inner, blockers_inner, boundary, True)
                return visited_inner, True
            if current_direction not in visited_inner[current_location]:
                visited_inner[current_location].append(current_direction)
        else:
            visited_inner[current_location] = [current_direction]

        # if not b_test and current_location + current_direction not in blockers:
        #     # print(f'Entering at position {current_location}')
        #     # print(visited)
        #     new_blocker = current_location + current_direction
        #     # print(f'new blocker: {new_blocker}')
        #     if new_blocker != start_location:
        #
        #         # _, loop = traverse_grid(copy.deepcopy(visited),
        #         #                      list(blockers) + [new_blocker],
        #         #                      current_location,
        #         #                      get_next_direction(current_direction),
        #         #                      b_test=True)
        #         _, loop = traverse_grid({start_location:[start_direction]},
        #                              list(blockers) + [new_blocker],
        #                              start_location,
        #                              start_direction,
        #                              b_test=True)
        #     # print(visited)
        #     # a = 2
        #     if loop:
        #         # print(f'loop: {current_location + current_direction}')
        #         # print(f'{new_blocker}')
        #         if new_blocker not in new_blockers:
        #             new_blockers.append(new_blocker)
        #         num_loops_inner += 1
        #         # visualize_map(visited, blockers, boundary, True)

        current_location += current_direction
        # visualize_map(visited, blockers, boundary)
    if not b_test:
        # visualize_map(visited, blockers, boundary)
        return visited_inner, new_blockers
    else:
        return {}, False


# Part 1
with open(filename) as f_in:
    lines = np.array([[_v for _v in v.strip()] for v in f_in.readlines()])

closet_map = np.full((lines.shape[0] + 2, lines.shape[1] + 2), '@', dtype=str)
closet_map[1:lines.shape[0] + 1, 1:lines.shape[1] + 1] = lines

directions = [-1, 1j, 1, -1j]

blockers, boundary, start_idx = [[int(x) + 1j*int(y) for x, y in zip(*np.where(np.isin(closet_map, c)))] for c in ['#', '@', '^']]
start_idx = start_idx[0]
start_direction = -1

visited = {start_idx:[start_direction]}
visited, new_blockers = traverse_grid(visited, blockers, start_idx, start_direction)

num_steps = len(visited)
print(f'Steps: {num_steps}')
print(f'Loops: {len(new_blockers)}')

# The block must be placed BEFORE the guard starts moving
loops = []
for iV, (visited_location, visited_directions) in enumerate(list(visited.items())):
    new_blocker = visited_location
    visited_inner, b_loop = traverse_grid({start_idx: [start_direction]},
                                          list(blockers) + [new_blocker],
                                          start_idx,
                                          start_direction,
                                          b_test=True)
    if b_loop:
        if new_blocker not in loops:
            loops.append(new_blocker)
print(f'Loops: {len(loops)}')
# # 598 too low
# # 1932 too low
# # 2244 too high
# 1976