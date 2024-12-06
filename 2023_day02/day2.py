import numpy as np
import re

with open('input.txt') as f_in:
    games = [_d.strip() for _d in f_in.readlines()]

colors = ['red', 'blue', 'green']
limits = {'red':12, 'blue':14, 'green':13}

counts = {}
for iG, game in enumerate(games):
    game_num = int(re.findall(r'^Game (\d+):.*', game)[0])
    counts[game_num] = {color:[] for color in colors}

    rolls = game.split(': ')[1].split(';')
    for roll in rolls:
        roll = roll.strip()
        # print(roll)

        for color in colors:
            num_cubes = re.findall(f'(\d+)\s{color}', roll)

            if num_cubes == []:
                num_cubes = 0
            else:
                num_cubes = int(num_cubes[0])
            # print(f'\t{color}')
            # print(f'\t{num_cubes}')
            counts[game_num][color].append(num_cubes)

game_sum = 0
for game_num, cube_counts in counts.items():
    if all(all(v <= limits[color] for v in cube_counts[color]) for color in colors):
        game_sum += game_num
        print(f'{game_num}: pass')
print(f'Total: {game_sum}')



power_sum = 0
for game_num, cube_counts in counts.items():
    max_counts = [max(cube_counts[color]) for color in colors]
    current_sum = max_counts[0] * max_counts[1] * max_counts[2]
    print(f'{game_num}: {current_sum}')
    power_sum += current_sum
print(f'Power sum: {power_sum}')





















