from functools import cache, lru_cache

@cache
def parse_pattern(pattern, colors):
    if pattern == '':
        return True

    for color in colors:
        if pattern[0:len(color)] == color:
            if parse_pattern(pattern[len(color):], colors):
                # print(f'\t{color}')
                return True
    return False


# This is too slow
# @lru_cache
# def parse_pattern_p2(pattern, colors):
#     if pattern == '':
#         return [[]]
#
#     all = []
#
#     for color in colors:
#         if pattern[0:len(color)] == color:
#             sub_colors = parse_pattern_p2(pattern[len(color):], colors)
#             for sub_color in sub_colors:
#                 all.append([color] + sub_color)
#     return all

# Same thing as above but only counts instead of forming paths
@cache
def parse_pattern_p2(pattern, colors):
    if pattern == '':
        return 1

    # all = []
    count = 0

    for color in colors:
        if pattern[0:len(color)] == color:
            count += parse_pattern_p2(pattern[len(color):], colors)

    return count


filename = '2024_day19/test_input1.txt'
filename = '2024_day19/input.txt'

with open(filename) as f_in:
    lines = f_in.readlines()

colors = tuple(c.strip() for c in lines[0].strip().split(','))
patterns = [p.strip() for p in lines[2:]]
count = 0
for pattern in patterns:
    # print(f'{pattern}:')
    exists = parse_pattern(pattern, colors)
    # print(f'{pattern}: {exists}')
    if exists:
        count += 1
print(count)

# Part 2
count = 0
for iP, pattern in enumerate(patterns):
    print(f'{iP}/{len(patterns)}')
    exists = parse_pattern_p2(pattern, colors)
    count += exists
print(count)
