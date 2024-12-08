import numpy as np

filename = '2024_day06/input.txt'
filename = '2024_day06/test_input.txt'
# filename = '2024_day06/test_input2.txt'


def print_grid(grid):
    print('     ', end='')
    print(''.join([f'{i:^3}' for i in range(grid.shape[1])]))
    print('   ', end='')
    print(''.join(['---' for i in range(grid.shape[1])]) + '-')
    for iR, row in enumerate(grid):
        print(f'{iR:^2} | ', end='')
        print(''.join([f'{c:^3}' for c in row]))


def get_next_direction(current_direction):
    direction_keys = [value for key, value in directions.items()]
    direction_idx = (direction_keys.index(current_direction) + 1) % 4
    next_direction = direction_keys[direction_idx]
    # print(f'Current direction: {dir_char[tuple(current_direction)]}; next direction: {dir_char[tuple(next_direction)]}')
    return dir_char[tuple(next_direction)]


# Part 1
with open(filename) as f_in:
    lines = np.array([[_v for _v in v.strip()] for v in f_in.readlines()])

closet_map = np.full((lines.shape[0] + 2, lines.shape[1] + 2), '@', dtype=str)
closet_map[1:lines.shape[0] + 1, 1:lines.shape[1] + 1] = lines

directions = {'^': [-1, 0],  # North
              '>': [0, 1],  # East
              'v': [1, 0],  # South
              '<': [0, -1]}  # West
dir_char = {tuple(value): key for key, value in directions.items()}

blockers, boundary = [[[int(x), int(y)] for x, y in zip(*np.where(np.isin(closet_map, c)))] for c in ['#', '@']]

# print(closet_map)


def traverse_grid(closet_map, current_idx):
    current_direction = directions[closet_map[tuple(current_idx)]]
    num_loops = 0
    visited = {}

    x = current_idx[0] + current_direction[0]
    y = current_idx[1] + current_direction[1]
    current_tile = closet_map[tuple(current_idx)]
    next_tile = closet_map[x, y]
    while next_tile != '@':
        # Keep rotating until the next tile is not #
        while next_tile == '#':
            # Turn 90 degrees
            x = x - current_direction[0]
            y = y - current_direction[1]
            current_direction = directions[get_next_direction(current_direction)]
            next_tile = closet_map[x, y]

        closet_map[x, y] = dir_char[tuple(current_direction)]

        if (x, y) in visited:
            visited[(x, y)].append(current_direction)
        else:
            visited[(x, y)] = [current_direction]

        current_tile = closet_map[x, y]
        x = x + current_direction[0]
        y = y + current_direction[1]
        next_tile = closet_map[x, y]
    return visited


    # b_loop = False
    # test_x = x
    # test_y = y
    # # for _, test_direction in directions.items():
    # test_direction = directions[get_next_direction(current_direction)]
    # test_x = test_x + test_direction[0]
    # test_y = test_y + test_direction[1]
    # test_tile = closet_map[test_x, test_y]
    # count = 0
    # while test_tile not in ['@']:
    #     count += 1
    #     if (test_x, test_y) in visited:
    #         if test_direction in visited[(test_x, test_y)]:
    #             b_loop = True
    #             # print(f'Loop: ({x+ current_direction[0]}, {y+ current_direction[1]})')
    #             # test_map = np.array(closet_map)
    #             # test_map[x+ current_direction[0], y+ current_direction[1]] = 'X'
    #             # print_grid(test_map)
    #             # print()
    #             break
    #     if b_loop:
    #         break
    #
    #     test_x = test_x + test_direction[0]
    #     test_y = test_y + test_direction[1]
    #     test_tile = closet_map[test_x, test_y]
    #     a = 1
    #
    #     count2 = 0
    #     while test_tile == '#':
    #         count2 += 1
    #         # Turn 90 degrees
    #         test_x = test_x - test_direction[0]
    #         test_y = test_y - test_direction[1]
    #         test_direction = directions[get_next_direction(test_direction)]
    #         test_tile = closet_map[test_x, test_y]
    # # if b_loop:
    # #     break
    # if b_loop:
    #     num_loops += 1

    # print_grid(closet_map)
    # print()


current_idx = np.where(np.isin(closet_map, '^'))
current_idx = [int(_v) for _v in [v[0] for v in current_idx]]
visited = traverse_grid(closet_map, current_idx)

# num_steps = len(np.where(np.isin(closet_map, list(directions.keys())))[0])
num_steps = len(visited)
print(num_steps)
# print(num_loops)


# 598 too low
# 2244 too high
