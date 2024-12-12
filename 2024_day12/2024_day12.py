import numpy as np
import queue

def print_grid(grid):
    print('     ', end='')
    print(''.join([f'{i:^3}' for i in range(grid.shape[1])]))
    print('   ', end='')
    print(''.join(['---' for i in range(grid.shape[1])]) + '-')
    for iR, row in enumerate(grid):
        print(f'{iR:^2} | ', end='')
        print(''.join([f'{c:^3}' for c in row]))

def within_bounds(location):
    loc_re, loc_im = j2c(location)

    if loc_re < 0 or loc_re >= crop_map.shape[0]:
        return False
    if loc_im < 0 or loc_im >= crop_map.shape[1]:
        return False
    return True

# Complex to coordinate
def j2c(p):
    return int(np.real(p)), int(np.imag(p))

def get_edges(position):
    edges = []
    for direction in [-1, 1j, 1, -1j]:
        edge = position + direction
        if not within_bounds(edge):
            continue

        value = crop_map[j2c(edge)]
        if value == crop_map[j2c(position)]:
            edges.append(edge)
    return edges

def BFS(start_position, plant):
    paths = []
    explored = {}
    Q = queue.Queue()
    explored[start_position] = 0
    Q.put(start_position)
    while not Q.empty():
        position = Q.get()
        if crop_map[j2c(position)] == plant:
            paths.append(position)

        for edge in get_edges(position):
            if edge not in explored or explored[edge] == len(paths):
                explored[edge] = len(paths)
                Q.put(edge)
    return paths

def show_crops(crop_map, crop_start):
    for start_location, plant_locations in crop_start.items():
        current_map = np.full(crop_map.shape, '.')
        for plant_location in plant_locations:
            current_map[j2c(plant_location)] = crop_map[j2c(plant_location)]
        print_grid(current_map)
        print()

filename = '2024_day12/test_input1.txt'
# filename = '2024_day12/test_input2.txt'
filename = '2024_day12/test_input3.txt'
filename = '2024_day12/input.txt'

with open(filename) as f_in:
    crop_map = np.array([[v for v in line.strip()] for line in f_in.readlines()])

crop_start = {}
visited = []
for iX in range(crop_map.shape[0]):
    for iY in range(crop_map.shape[1]):
        location = iX + 1j*iY
        if location in visited:
            continue

        crop_start[location] = BFS(location, crop_map[iX, iY])
        visited += crop_start[location]

price = 0
for start_location, plant_locations in crop_start.items():
    num_perimeters = 0
    for plant_location in plant_locations:
        # edges = get_edges(plant_location)
        # edges = []
        for direction in [-1, 1j, 1, -1j]:
            edge = plant_location + direction
            if not within_bounds(edge):
                num_perimeters += 1
                continue

            value = crop_map[j2c(edge)]
            if value != crop_map[j2c(plant_location)]:
                # edges.append(edge)
                num_perimeters += 1
    current_price = num_perimeters * len(plant_locations)
    print(f'{crop_map[j2c(start_location)]}: Perimeter {num_perimeters}, Area {len(plant_locations)}, Price {current_price}')

    price += current_price
print(f'Total price: {price}')