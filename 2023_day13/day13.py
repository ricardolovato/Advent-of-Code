import numpy as np
import re

def compare_segment(row, compare_index):
    remaining_length = len(row) - compare_index
    
    # The length to compare should be the same in both directions
    check_length = min(compare_index, remaining_length)

    segment_left = row[compare_index - check_length:compare_index]
    segment_right = row[compare_index:compare_index + check_length]

    segment_comparison = segment_left == segment_right[::-1]

    # print(row)
    # spaces = ''.join(['    '] * (compare_index - check_length))
    # print(f'{spaces}{segment_left}{segment_right}')
    return segment_comparison

def find_reflection(grid):
    reflections = []
    for row in grid:
        row_reflections = []
        for compare_index in np.arange(1, len(row)):
            segment_comparison = compare_segment(row, compare_index)

            segments_match = all(segment_comparison)
            if segments_match:
                row_reflections.append(compare_index)

            num_incorrect = len([c for c in segment_comparison if not c])

            # print(f'{segments_match}')
            # print(f'Number incorrect: {num_incorrect}')
            # # print(f'compare_index: {compare_index}')
            # # print(f'remaining length: {remaining_length}')
            # # print(f'check length: {check_length}')
            # print()
        
        reflections.append(row_reflections)
        # break

    # Part 1
    reflection_idx = -1
    unique_idx = list(set([v for vals in reflections for v in vals]))
    for idx in unique_idx:
        if all(idx in row for row in reflections):
            reflection_idx = idx
            break
    
    # Part 2
    occurances = {}
    for idx in unique_idx:
        occurances[idx] = 0
        for row in reflections:
            if idx in row:
                occurances[idx] += 1

    new_reflection_idx = [idx for idx, num in occurances.items() if num == len(reflections) - 1]
    if len(new_reflection_idx) == 1:
        new_reflection_idx = new_reflection_idx[0]
        # naughty_line_idx = [idx for idx, contents in enumerate(reflections) if new_reflection_idx not in contents][0]
        # row = grid[naughty_line_idx]
    
        # segment_comparison = compare_segment(row, new_reflection_idx)
        # change_index = np.where(segment_comparison == False)[0][0]
    else:
        new_reflection_idx = -1

    return reflection_idx, new_reflection_idx

with open('input.txt') as f_in:
    lines = [line.strip() for line in f_in.readlines()]

grids = []
stop_indices = [idx for idx, line in enumerate(lines) if line == ''] + [len(lines)]
start_indices = [0] + [idx + 1 for idx in stop_indices[0:-1]]
for start_index, stop_index in zip(start_indices, stop_indices):
    grids.append(np.array([[l for l in line] for line in lines[start_index:stop_index]]))

grid_sum = []
part2_sum = []
for iG, grid in enumerate(grids):
    ref_idx, new_ref_idx = find_reflection(grid)
    
    # Part 1
    if ref_idx == -1:
        # No reflections
        ref_idx, _ = find_reflection(grid.T)
        grid_sum.append(ref_idx * 100)
    else:
        grid_sum.append(ref_idx)
    
    if new_ref_idx == -1:
        _, new_ref_idx = find_reflection(grid.T)
        part2_sum.append(new_ref_idx * 100)
    else:
        part2_sum.append(new_ref_idx)


    # print(f'Grid {iG} - {ref_idx}')
    print(f'Grid {iG} - {new_ref_idx}')
    # break

print(f'Part 1: {sum(grid_sum)}')
print(f'Part 2: {sum(part2_sum)}')


































