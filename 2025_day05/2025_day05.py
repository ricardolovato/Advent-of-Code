def in_range(num, current_range):
    return current_range[1] >= num >= current_range[0]


def build_ranges(ranges, id_ranges = None):
    if id_ranges is None:
        id_ranges = []

    for start, stop in ranges:
        b_overlap = False
        for idx in range(len(id_ranges)):
            # Find overlaps
            if in_range(start, id_ranges[idx]):
                # print(f'start {start} is within {id_ranges[idx]}')
                # Update the new stop of this range
                id_ranges[idx][1] = max(id_ranges[idx][1], stop)
                b_overlap = True
            if in_range(stop, id_ranges[idx]):
                # print(f'stop {stop} is within {id_ranges[idx]}')
                id_ranges[idx][0] = min(id_ranges[idx][0], start)
                b_overlap = True
        if not b_overlap:
            # print(f'no overlap for range {start}-{stop}')
            id_ranges.append([start, stop])
    return id_ranges


filename = '2025_day05/test_input.txt'
filename = '2025_day05/input.txt'
with open(filename) as f_in:
    lines = f_in.readlines()

ranges = [[int(v) for v in line.strip().split('-')] for line in lines[0:lines.index('\n')]]
ingredients = [int(line.strip()) for line in lines[lines.index('\n')+1::]]

id_ranges = build_ranges(ranges)

# Consolidate ranges
while True:
    current_len = len(id_ranges)
    id_ranges = build_ranges(sorted(id_ranges)) # You must sort the lists each time
    print(f'{current_len} -> {len(id_ranges)}')
    if current_len == len(id_ranges):
        break

count = 0
for ingredient in ingredients:
    if any(start <= ingredient <= stop for start, stop in id_ranges):
        print(f'{ingredient} in range')
        count += 1
print(count)
print(sum([stop - start + 1 for start, stop in id_ranges]))
