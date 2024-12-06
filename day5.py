import numpy as np
import re

def line_to_nums(line):
    return [int(v) for v in re.findall(r'(\d+)', line)]

def traverse_seed_map(seed_maps, seed_num):
    # print(seed_num)
    input_value = seed_num
    for map_name, map_data in seed_maps.items():
        # print(map_name)

        output_value = source_to_dest(map_data, input_value)
        # print(f'\t{input_value} -> {output_value}')
        input_value = output_value
    return output_value

def source_to_dest(seed_map, source_value):
    dest_value = -1
    for source_range, dest_range in seed_map.items():
        source_start = source_range[0]
        source_stop = source_range[1]

        if source_value >= source_start and source_value < source_stop:
            source_offset = source_value - source_start
            dest_value = dest_range[0] + source_offset
            break
    if dest_value == -1:
        return source_value
    else:
        return dest_value

def num_in_map(seed_map, search_value):
    value_in_map = False
    for (source_start, source_stop), _ in seed_map.items():
        if search_value >= source_start and search_value < source_stop:
            value_in_map = True
    return value_in_map

def fill_in_map(seed_map, seed_max):
    count = 0
    while( any(not num_in_map(seed_map, search_value) for search_value in np.arange(0, seed_max))):
        if count == 2: break
        for search_value in np.arange(0, seed_max):
            value_in_map = num_in_map(seed_map, search_value)
            if value_in_map: continue

            stop_value = search_value
            while (not num_in_map(seed_map, stop_value)):
                stop_value += 1
                if stop_value >= seed_max:
                    break
            
            # print(f'{search_value}: {value_in_map}')
            seed_map[(search_value, stop_value)] = (search_value, stop_value)
            break
        count += 1

with open('input.txt') as f_in:
    lines = [line.strip() for line in f_in.readlines()]

seeds = line_to_nums(lines[0])

seed_maps = {}
for line in lines[2:]:
    if line == '': continue
    if ':' in line:
        map_name = line.split(' ')[0]
        seed_maps[map_name] = {}
        continue
    
    dest_start, source_start, v_step = line_to_nums(line)
    dest_range = (dest_start, dest_start + v_step)
    source_range = (source_start, source_start + v_step)

    seed_maps[map_name][source_range] = dest_range

locations = []
for seed_num in seeds:
    locations.append(traverse_seed_map(seed_maps, seed_num))

print(f'Part 1: {np.min(locations)}')


seed_num_start = seeds[0::2]
seed_num_range = seeds[1::2]
all_seeds_range = {(seed_start, seed_start+seed_range):(0,0) for seed_start, seed_range in zip(seed_num_start, seed_num_range)}

# Get max seed value
seed_max = 0
for seed_start, seed_range in zip(seed_num_start, seed_num_range):
    seed_stop = seed_start + seed_range
    if seed_stop > seed_max:
        seed_max = seed_stop

# for map_name, seed_map in seed_maps.items():
#     fill_in_map(seed_map, seed_max)

reverse_seed_map = {}
for map_name in list(seed_maps.keys())[::-1]:
    seed_map = seed_maps[map_name]
    reverse_seed_map[map_name] = {}

    for source, dest in seed_map.items():
        reverse_seed_map[map_name][dest] = source


def find_lowest_location(reverse_seed_map, seed_max):
    start_map = reverse_seed_map['humidity-to-location']
    for loc in range(0, seed_max):
        seed_num = traverse_seed_map(reverse_seed_map, loc)

        if num_in_map(all_seeds_range, seed_num):
            return loc
lowest_location = find_lowest_location(reverse_seed_map, seed_max)
print(f'Part 2: {lowest_location}')



























