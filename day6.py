import numpy as np
import re

def line_to_nums(line):
    return [int(v) for v in re.findall(r'(\d+)', line)]

def find_first_index(time, distance_record):
    start_index = 0
    for iS, t in enumerate(range(time)):
        d = (time - iS) * (1 * t)
        if d > distance_record:
            start_index = iS
            break
    return start_index

def find_last_index(time, distance_record):
    stop_index = time
    for iS, t in enumerate(range(time - 1, -1, -1)):
        d = (iS) * (1 * t)
        if d > distance_record:
            stop_index = iS
            break
    return stop_index

def get_ways_to_win(times, distance_records):
    ways_to_win = []
    for time, distance_record in zip(times, distance_records):
        # print(f'time: {time}')
        ways_to_win.append(0)
        speeds = [1 * t for t in range(time)]
        distances = []
        for iS, speed in enumerate(speeds):
            d = (time - iS) * speed
            distances.append(d)
            if d > distance_record:
                ways_to_win[-1] += 1

            if ways_to_win[-1] != 0 and d < distance_record:
                break
    return ways_to_win

def ways_to_win_quadratic(times, distance_records):
    ways_to_win = []
    for time, distance_record in zip(times, distance_records):
        d_lower = int((-time + np.sqrt(time**2 - 4*distance_record))/-2)
        d_upper = int((-time - np.sqrt(time**2 - 4*distance_record))/-2)
        
        lowest = d_lower
        for lower in range(d_lower - 1, d_lower + 2):
            if (time - lower) * lower > distance_record:
                lowest = lower
                break
        highest = d_upper
        for higher in range(d_upper - 1, d_upper + 2):
            if (time - higher) * higher > distance_record:
                highest = higher
                # break
                
        
        ways_to_win.append(highest - lowest + 1)
        # break
    return ways_to_win




with open('test_input.txt') as f_in:
    lines = [line.strip() for line in f_in.readlines()]

times, distance_records = [line_to_nums(line) for line in lines]

# ways_p1 = np.product(get_ways_to_win(times, distance_records))
ways_p1 = np.product(ways_to_win_quadratic(times, distance_records))
print(f'Part 1: {ways_p1}')

time, distance_record = [int(line.split(':')[1].strip().replace(' ', '')) for line in lines]
# # Brute force method
# start_index = find_first_index(time, distance_record)
# stop_index = find_last_index(time,  distance_record)
# stop_index = time - stop_index
# ways_p2 = stop_index - start_index + 1
# print(f'Part 2: {ways_p2}')

ways_p2 = ways_to_win_quadratic([time], [distance_record])[0]
print(f'Part 2: {ways_p2}')
























