import numpy as np
import re

def calc_coord_offset(lines, offset_step = 1):
    offsets = np.zeros((len(lines), len(lines[0])), dtype = np.int32)

    if offset_step != 1:
        offset_step -= 1

    line_num = 0
    while line_num < len(lines):
        line = lines[line_num]
        if all(c == '.' for c in line):
            for i in np.arange(line_num, len(lines)):
                offsets[i] += 1 * offset_step

        line_num += 1
    return offsets

with open('input.txt') as f_in:
    lines = [line.strip() for line in f_in.readlines()]

lines_ary = np.array([[c for c in line] for line in lines])
offsets_x = calc_coord_offset(lines_ary, offset_step=1000000)
offsets_y = calc_coord_offset(lines_ary.T, offset_step=1000000).T

# Record locations and a list of numbers for debugging
star_numbers = {}
star_locations = {}
for iR, row in enumerate(lines_ary):
    for iC, col in enumerate(row):
        if col != '#':
            continue
        original_location = (iR, iC)
        offset_location = (iR + offsets_x[original_location], iC + offsets_y[original_location])
        star_locations[offset_location] = 0
        star_numbers[offset_location] = len(star_locations)

star_distances = {}
for i1, star1 in enumerate(star_locations):
    for i2, star2 in enumerate(star_locations):
        if star1 == star2: continue
        if i2 > i1 or i1 == i2:
            continue

        # Direct calculation
        steps = abs((star2[0] - star1[0])) + abs((star2[1] - star1[1]))
        
        star_distances[(star1, star2)] = steps
        # print(f'{star_numbers[star1]} -> {star_numbers[star2]} = {steps}')

distance = sum([v for k, v in star_distances.items()])
print(f'Shortest distance: {distance}')



















    