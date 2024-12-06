import numpy as np
import re

def get_search_grp(current_index):
    iR, iC = current_index
    row_start_index = np.max([0, iR - 1])
    row_stop_index = np.min([iR + 2, schematic.shape[0]])
    col_start_index = np.max([0, iC - 1])
    col_stop_index = np.min([iC + 2, schematic.shape[1]])

    search_grp = schematic[row_start_index:row_stop_index, col_start_index:col_stop_index]
    # print(f'{search_grp}') 
    return search_grp

def get_next_index(current_index, path):
    pipe_shape, iR, iC = path

    if pipe_shape == '-':
        if iC > current_index[1]:
            # Left to right
            next_index = (current_index[0], current_index[1] + 1)
        else:
            # Right to left
            next_index = (current_index[0], current_index[1] - 1)
    elif pipe_shape == '|':
        if iR > current_index[0]:
            # Bottom to top
            next_index = (current_index[0] + 1, current_index[1])
        else:
            # Top to bottom
            next_index = (current_index[0] - 1, current_index[1])
    elif pipe_shape == '7':
        if iC > current_index[1]:
            # Moving down to the right
            next_index = (current_index[0], current_index[1] + 1)
        else:
            # Moving up to the left
            next_index = (current_index[0] - 1, current_index[1])
    elif pipe_shape == 'J':
        if iC == current_index[1]:
            # Moving down and left
            next_index = (current_index[0] + 1, current_index[1])
        else:
            # Moving right then up
            next_index = (current_index[0], current_index[1] + 1)
    elif pipe_shape == 'L':
        if iR == current_index[0]:
            # Moving left then up
            next_index = (current_index[0], current_index[1] - 1)
        else:
            # Moving down then right
            next_index = (current_index[0] + 1, current_index[1])
    elif pipe_shape == 'F':
        if iC == current_index[1]:
            # Moving up then right
            next_index = (current_index[0] - 1, current_index[1])
        else:
            # Moving left then down
            next_index = (current_index[0], current_index[1] - 1)
    
    
    return next_index

def find_pipes(search_grp, current_index):
    paths = []

    search_indices = []
    current_pipe = search_grp[1,1]
    if current_pipe == '|':
        search_indices = [(0, 1), (2, 1)]
    elif current_pipe == '-':
        search_indices = [(1, 0), (1, 2)]
    elif current_pipe == 'F':
        search_indices = [(1, 2), (2, 1)]
    elif current_pipe == 'L':
        search_indices = [(0, 1), (1, 2)]
    elif current_pipe == 'J':
        search_indices = [(0, 1), (1, 0)]
    elif current_pipe == '7':
        search_indices = [(1, 0), (2, 1)]
    elif current_pipe == 'S':
        search_indices = [(0, 1), (1, 0), (1, 2), (2, 1)]

    for iR, iC in search_indices:
        next_pipe = search_grp[iR][iC]
        if next_pipe not in ['.']:
            if current_pipe == 'S':
                if (iR, iC) == (0, 1):
                    if next_pipe not in ['|', '7', 'F']:
                        continue
                elif (iR, iC) == (1, 0):
                    if next_pipe not in ['L', '-', 'F']:
                        continue
                elif (iR, iC) == (1, 2):
                    if next_pipe not in ['-', 'J', '7']: 
                        continue
                elif (iR, iC) == (2, 1):
                    if next_pipe not in ['|', 'L', 'J']:
                        continue
            paths.append((search_grp[iR][iC], 
                          current_index[0] + iR - 1, 
                          current_index[1] + iC - 1))
    return paths

with open('input.txt') as f_in:
    lines = np.array([[c for c in line.strip()] for line in f_in.readlines()])
schematic = np.full((lines.shape[0] + 2, lines.shape[1] + 2), '.')
schematic[1:schematic.shape[0]-1, 1:schematic.shape[1] - 1] = lines

start_index = [(line_index, list(line).index('S')) for line_index, line in enumerate(schematic) if 'S' in line][0]
current_index = start_index

search_grp = get_search_grp(current_index)
points = []
# Two main branches
paths = find_pipes(search_grp, current_index)
for path in paths:
    next_index = get_next_index(current_index, path)
    search_grp = get_search_grp(next_index)

    count = 0
    pts = [start_index, next_index]
    while next_index != start_index:
        p = [(p_type, iR, iC) for p_type, iR, iC in find_pipes(search_grp, next_index) if (iR, iC) not in pts]
        if len(p) != 1:
            print(search_grp)
            break
        p = p[0]

        next_index = get_next_index(next_index, p)
        search_grp = get_search_grp(next_index)
        pts.append(next_index)

        count += 1
    points.append(pts)

# Output a drawing of the paths 
draw_path = np.full(schematic.shape, '.')
for iP, (point1, point2) in enumerate(zip(*points)):
    draw_path[point1] = 1
    draw_path[point2] = 2
    if point1 == point2 and iP != 0:
        print(f'{iP}: {point1} {point2}')
        draw_path[point1] = 'X'
        break
draw_path[start_index] = 'S'
with open('path.txt', 'w') as f_out:
    for row in draw_path:
        for col in row:
            f_out.write(f'{col}')
        f_out.write('\n')

# Part 2
# Convert junk pipes to empty cells
loop_schematic = np.full(schematic.shape, '.')
for iR in range(schematic.shape[0]):
    for iC in range(schematic.shape[1]):
        if (iR, iC) in points[0]:
            loop_schematic[iR][iC] = schematic[iR][iC]

inside_pts = []
crossings_regex = '|'.join(['L7', 'FJ', '\|'])
for iR in range(1, loop_schematic.shape[0] - 1):
    for iC in range(1, loop_schematic.shape[1] - 1):
        if (iR, iC) in points[0]:
            # Skip point if it's part of the loop
            continue

        row_left =  ''.join(loop_schematic[iR][1:iC]).replace('-', '')
        row_right = ''.join(loop_schematic[iR][iC + 1::]).replace('-', '')

        # Check number of crossings to see if the point is inside or outside the loop
        crossings = [re.findall(f'({crossings_regex})', current_row) for current_row in [row_left, row_right]]
        if all(len(crossing) % 2 == 1 for crossing in crossings):
            loop_schematic[iR][iC] = 'I'
            inside_pts.append((iR, iC))
        else:
            loop_schematic[iR][iC] = 'O'

# Output drawing of points inside/outside loop
with open('part2.txt', 'w') as f_out:
    for row in loop_schematic:
        for col in row:
            if col in ['O', 'I', '.']:
                f_out.write(f'{col}')
            else:
                f_out.write('.')
        f_out.write('\n')
print(f'Points inside loop: {len(inside_pts)}')

























