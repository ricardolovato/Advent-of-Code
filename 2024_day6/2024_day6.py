import numpy as np
filename = '2024_day6/input.txt'
# filename = 'input.txt'

def get_next_direction(current_direction):
    direction_keys = [value for key, value in directions.items()]
    direction_idx = (direction_keys.index(current_direction) + 1) % 4
    next_direction = direction_keys[direction_idx]
    print(f'Current direction: {dir_char[tuple(current_direction)]}; next direction: {dir_char[tuple(next_direction)]}')
    return dir_char[tuple(next_direction)]

# Part 1
with open(filename) as f_in:
    lines = np.array([[_v for _v in v.strip()] for v in f_in.readlines()])

map = np.full((lines.shape[0] + 2, lines.shape[1] + 2), '@', dtype=str)
map[1:lines.shape[0] + 1, 1:lines.shape[1] + 1] = lines

directions = {'^':[-1, 0], # North
              '>':[0, 1],  # East
              'v':[1, 0],  # South
              '<':[0, -1]} # West
dir_char = {tuple(value):key for key, value in directions.items()}
print(map)

current_idx = np.where(np.isin(map, list(directions.keys())))
current_idx = [int(_v) for _v in [v[0] for v in current_idx]]

current_direction = directions[map[tuple(current_idx)]]

x = current_idx[0] + current_direction[0]
y = current_idx[1] + current_direction[1]
current_tile = map[tuple(current_idx)]
next_tile = map[x, y]
while next_tile != '@':
    if next_tile == '#':
        # Turn 90 degrees
        x = x - current_direction[0]
        y = y - current_direction[1]
        current_direction = directions[get_next_direction(current_direction)]

    map[x, y] = dir_char[tuple(current_direction)]
    current_tile = map[x, y]
    x = x + current_direction[0]
    y = y + current_direction[1]
    next_tile = map[x, y]
    # print(map)
    # print()
num_steps = len(np.where(np.isin(map, list(directions.keys())))[0])
print(num_steps)