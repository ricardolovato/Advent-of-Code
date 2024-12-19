from functools import cache

@cache
def parse_pattern(pattern, colors):
    if pattern == '':
        return True

    for color in colors:
        if pattern[0:len(color)] == color:
            if parse_pattern(pattern[len(color):], colors):
                return True
    return False


filename = '2024_day19/test_input1.txt'
# filename = '2024_day19/input.txt'

with open(filename) as f_in:
    lines = f_in.readlines()

colors = tuple(c.strip() for c in lines[0].strip().split(','))
patterns = [p.strip() for p in lines[2:]]
count = 0
for pattern in patterns:
    exists = parse_pattern(pattern, colors)
    # print(f'{pattern}: {exists}')
    if exists:
        count += 1
print(count)