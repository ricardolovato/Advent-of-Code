import numpy as np
import queue

def print_grid(grid):
    print('     ', end='')
    print(''.join([f'{i-1:^3}' for i in range(grid.shape[1])]))
    print('   ', end='')
    print(''.join(['---' for i in range(grid.shape[1])]) + '-')
    for iR, row in enumerate(grid):
        print(f'{iR-1:^2} | ', end='')
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

def get_edges(position, b_ignore_bounds=False):
    edges = []
    for direction in [-1, 1j, 1, -1j]:
        edge = position + direction
        if not b_ignore_bounds and not within_bounds(edge):
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

def edge_search(start_position, edges):
    paths = []
    for current_direction in [[-1, 1], [1j, -1j]]:
        p = []
        explored = {}
        Q = queue.Queue()
        explored[start_position] = 0
        Q.put(start_position)
        while not Q.empty():
            position = Q.get()
            p.append(position)
            for direction in current_direction:
            # for direction in [-1, 1j, 1, -1j]:
                edge = position + direction
                if edge not in explored and edge in edges:
                    explored[edge] = len(p)
                    Q.put(edge)
        paths.append(p)
    return paths


def show_crops(crop_map, crop_start):
    for start_location, plant_locations in crop_start.items():
        current_map = np.full((crop_map.shape[0] + 2, crop_map.shape[1] + 2), '.')
        for plant_location in plant_locations:
            current_map[j2c(plant_location + (1+1j))] = crop_map[j2c(plant_location)]
        print_grid(current_map)
        print()

def show_boundary(crop_map, start_location, plant_locations, perimeter):
    # for start_location, plant_locations in crop_start.items():
    current_map = np.full((crop_map.shape[0] + 2, crop_map.shape[1] + 2), '.')
    for plant_location in plant_locations:
        current_map[j2c(plant_location + (1+1j))] = crop_map[j2c(plant_location)]

    print_grid(current_map)
    print()

    for perimeter_location in perimeter:
        current_map[j2c(perimeter_location + (1 + 1j))] = 'X'

    print_grid(current_map)
    print()

# Concave point P contributes 2 edges:
#   A | P   A  A    A  A    P | A
#     ---    ---   ---      ---
#   A  A   A | P   P | A    A  A
def is_concave(edge_location, plant, plant_locations):
    # directions = [-1, 1j, 1, -1j]
    concave_directions = [[-1j, 1, 1-1j],   # Top right point
                          [-1, -1j, -1-1j], # Bottom right point
                          [-1, 1j, -1+1j],  # Bottom left point
                          [1j, 1, 1+1j],]    # Top left point
    pocket_directions = [[1, -1, 1j],
                         [1, -1, -1j],
                         [1, -1j, 1j],
                         [-1, -1j, 1j],]

    for iD, direction in enumerate([pocket_directions, concave_directions,]):
        for concave_direction in direction:
            b_is_concave = True
            for p in concave_direction:
                if not within_bounds(edge_location + p):
                    b_is_concave = False
                    break
                if edge_location + p not in plant_locations:
                    b_is_concave = False
                    break
            if b_is_concave:
                if iD == 0:
                    print(f'{edge_location}: pocket')
                    return True, 2
                else:
                    print(f'{edge_location}: concave')
                    return True, 1

    return False, 0

def is_top_bottom(edge_location, plant, plant_locations):
    # Top/bottom and left/right
    for good_tiles, bad_tiles in zip([[1, -1], [1j, -1j]], [[1j, -1j], [1, -1]]):
        b_is_concave = True
        for gt in good_tiles:
            if not within_bounds(edge_location + gt):
                b_is_concave = False
                break
            # if crop_map[j2c(edge_location + gt)] != plant:
            if edge_location + gt not in plant_locations:
                b_is_concave = False
                break
        if not b_is_concave:
            continue

        for bt in bad_tiles:
            # if not within_bounds(edge_location + bt):
            #     b_is_concave = False
            #     break
            # if within_bounds(edge_location + bt) and crop_map[j2c(edge_location + bt)] == plant:
            if within_bounds(edge_location + bt) and edge_location + bt in plant_locations:
                b_is_concave = False
                break
        if b_is_concave:
            print(f'{edge_location}: top bottom')
            return True


filename = '2024_day12/test_input1.txt'
filename = '2024_day12/test_input2.txt'
filename = '2024_day12/test_input3.txt'
filename = '2024_day12/test_input4.txt'
# filename = '2024_day12/input.txt'

with open(filename) as f_in:
    crop_map = np.array([[v for v in line.strip()] for line in f_in.readlines()])

# Use BFS to find all connected tiles
crop_start = {}
visited = []
for iX in range(crop_map.shape[0]):
    for iY in range(crop_map.shape[1]):
        location = iX + 1j*iY
        if location in visited:
            # Skip this tile if we've already visited it in a previous search
            continue

        crop_start[location] = BFS(location, crop_map[iX, iY])
        visited += crop_start[location]

show_crops(crop_map, crop_start)

# Calculate the perimeter by checking adjacent cells
price = 0
for start_location, plant_locations in crop_start.items():
    num_perimeters = 0
    for plant_location in plant_locations:
        for direction in [-1, 1j, 1, -1j]:
            edge = plant_location + direction
            if not within_bounds(edge):
                # Out of bounds counts as an edge
                num_perimeters += 1
                continue

            value = crop_map[j2c(edge)]
            if value != crop_map[j2c(plant_location)]:
                # If the adjacent cell isn't the same plant type, it is a perimeter
                num_perimeters += 1
    current_price = num_perimeters * len(plant_locations)
    print(f'{crop_map[j2c(start_location)]}: Perimeter {num_perimeters}, Area {len(plant_locations)}, Price {current_price}')

    price += current_price
print(f'Total price: {price}\n')


price = 0
for start_location, plant_locations in crop_start.items():
    perimeters = []
    for plant_location in plant_locations:
        for direction in [-1, 1j, 1, -1j]:
            edge = plant_location + direction
            if not within_bounds(edge):
                # Out of bounds counts as an edge
                perimeters.append(edge)
                continue
            value = crop_map[j2c(edge)]
            if value != crop_map[j2c(plant_location)]:
                # If the adjacent cell isn't the same plant type, it is a perimeter
                perimeters.append(edge)

    # Do BFS again to check consecutive edges
    visited = {}
    consecutive_perimeters = []
    while perimeters:
        loc = perimeters[0]
        edges = edge_search(loc, perimeters)
        for iE, edge in enumerate(edges):
            b_all_ones = all(v == 1 for v in [len(edge) for edge in edges])
            if b_all_ones and iE == 0:
                # We only need 1 of the paths if both of the paths are length 1
                continue

            if not b_all_ones and len(edge) == 1:
                continue
            consecutive_perimeters.append(edge)
            for e in edge:
                visited[e] = 1
        # Is there a better way to do this? Probably doesnt matter for small sets
        perimeters = [p for p in perimeters if p not in visited]

    show_boundary(crop_map, start_location, plant_locations, [_p for p in consecutive_perimeters for _p in p])
    num_edges = len([len(p) for p in consecutive_perimeters])

    # Check for corner points
    plant = crop_map[j2c(start_location)]
    corners = []
    for edge_location in [_p for p in consecutive_perimeters for _p in p]:
        b_concave, count = is_concave(edge_location, plant, plant_locations)
        num_edges += count
        if b_concave:
            corners.append(edge_location)

    # Check for top/bottom points
    for consecutive_points in consecutive_perimeters:
        # if len(consecutive_points) == 2:
        #     if any(p in corners for p in consecutive_points):
        #         print(f'{consecutive_points}: length 2 with corner')
        #         num_edges -= 1
        for point in consecutive_points:
            if is_top_bottom(point, plant, plant_locations):
                num_edges += 1
                break
    # break

    current_price = num_edges * len(plant_locations)
    price += current_price
    print(f'{plant}: Area {len(plant_locations)}, Perimeter {num_edges}, Price {current_price}')
print(f'Total price: {price}')