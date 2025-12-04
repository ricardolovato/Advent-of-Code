def within_bounds(n, grid_size):
    if n.real < 0:
        return False
    if n.imag < 0:
        return False
    if n.real >= grid_size[0]:
        return False
    if n.imag >= grid_size[1]:
        return False
    
    return True

def check_adjacent(n):
    count = 0
    for direction in [-1,    # N
                      -1+1j, # NE
                      0+1j,  # E
                      1+1j,  # SE
                      1,     # S
                      1-1j,  # SW
                      0-1j,  # W
                      -1-1j]:# NW
        pt = n + direction
        if within_bounds(pt, grid_size) and pt in occupied:
            count += 1
    return count 

def get_count(occupied):
    count = 0
    points = []
    for element in occupied:
        num_adj = check_adjacent(element)
        if num_adj < 4:
            # print(f'{element} -> {num_adj}')
            points.append(element)
            count += 1
    return [count, points]

filename = '2025_day04/test_input.txt'
filename = '2025_day04/input.txt'

with open(filename) as f_in:
    lines = [line.strip() for line in f_in.readlines()]

grid_size = (len(lines), len(lines[0]))

occupied = set()
for iL, line in enumerate(lines):
    for iI, item in enumerate(line):
        if item == '@':
            occupied.add(iL + 1j * iI)

count, points = get_count(occupied)
print(f'Part 1: {count}')

removed = 0
while True:
    count, points = get_count(occupied)
    if count == 0:
        break
    
    for point in points:
        occupied.remove(point)
    # print(f'Remove {count}, {len(occupied)} remaining')
    removed += count
    # break
print(f'Part 2: {removed}')