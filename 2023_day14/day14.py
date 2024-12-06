import numpy as np
import re

def tilt_table(loc_direction, rocks, cubes):
    movement = True
    while movement:
        movement = False
        for rock_loc in list(rocks.keys()):
            new_loc = (rock_loc[0] + loc_direction[0], rock_loc[1] + loc_direction[1])
            if new_loc not in cubes and new_loc not in rocks:

                while new_loc not in cubes and new_loc not in rocks:
                    new_loc = (new_loc[0] + loc_direction[0], new_loc[1] + loc_direction[1])
                del rocks[rock_loc]
                rocks[(new_loc[0] - loc_direction[0], new_loc[1] - loc_direction[1])] = 0
                movement = True

def visualize_platform(platform, rocks, cubes):
    print(platform)
    print()
    test_platform = np.full(platform.shape, '.')
    for cube_location, _ in cubes.items():
        test_platform[cube_location] = '#'
    for rock_location, _ in rocks.items():
        test_platform[rock_location] = 'O'
    print(test_platform)

    load = []
    for iR in np.arange(test_platform.shape[0]):
        num_rocks = len([idx for idx, c in enumerate(test_platform[iR]) if c == 'O'])
        load.append((test_platform.shape[0] - iR - 1 , num_rocks))

    total_load = sum([a * b for a, b in load])
    print(f'Total load: {total_load}')

def get_locations(platform):
    cubes = {}
    rocks = {}
    for iR in np.arange(platform.shape[0]):
        for iC in np.arange(platform.shape[1]):
            if platform[iR][iC] == 'O':
                rocks[(iR, iC)] = 0
            elif platform[iR][iC] == '#':
                cubes[(iR, iC)] = 0
    return cubes, rocks

with open('test_input.txt') as f_in:
    contents = np.array([[c for c in line.strip()] for line in f_in.readlines()])

# Ring of cubes along the outside to simplify bound checks
platform = np.full((contents.shape[0] + 2, contents.shape[1] + 2), '#')
platform[1:platform.shape[0] - 1, 1:platform.shape[1] - 1] = contents

directions = {'N':(-1, 0),
              'S':(1, 0),
              'E':(0, 1),
              'W':(0, -1)}

# Part 1
cubes, rocks = get_locations(platform)
loc_direction = directions['N']
tilt_table(loc_direction, rocks, cubes)
visualize_platform(platform, rocks, cubes)


repeats = []
platforms = {}
# Reset locations for part 2
cubes, rocks = get_locations(platform)
for cycle in np.arange(100):
    for direction in ['N', 'W', 'S', 'E']:
        loc_direction = directions[direction]
        tilt_table(loc_direction, rocks, cubes)

        test_platform = np.full(platform.shape, '.')
        for cube_location, _ in cubes.items():
            test_platform[cube_location] = '#'
        for rock_location, _ in rocks.items():
            test_platform[rock_location] = 'O'
        
        platform_key = tuple(test_platform.ravel())
        if platform_key in platforms:
            repeat_num = list(platforms.keys()).index(platform_key)
            print(f'Cycle {cycle}, {direction} - {repeat_num}')
            if direction == 'E':
                repeats.append((cycle, direction, repeat_num))
        else:
            platforms[platform_key] = 0

# visualize_platform(platform, rocks, cubes)



























