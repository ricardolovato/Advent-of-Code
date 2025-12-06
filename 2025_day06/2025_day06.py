import numpy as np
import re
import operator

filename = '2025_day06/test_input.txt'
filename = '2025_day06/input.txt'
with open(filename) as f_in:
    lines = f_in.readlines()

nums = np.array([[int(v) for v in re.findall(r'(\d+)', n)] for n in lines[0:-1]])
operators = re.findall(r'[*+]', lines[-1])

op_lookup = {'+': operator.add,
             '*': operator.mul}
total = 0
for iC, col in enumerate(nums.T):
    cum = None
    for iI, item in enumerate(col):
        if cum is None:
            cum = item
        else:
            cum = op_lookup[operators[iC]](cum, item)
    total += cum
    print(f'{iC}: {cum}')
print(total)

# Part 2
# Pad the lines so they are all the same length
lines = [' ' + line[0:-1] for line in lines]
num_chars = max(list(set([len(l) for l in lines])))
for iL in range(len(lines)):
    if len(lines[iL]) < num_chars:
        lines[iL] += (num_chars - len(lines[iL])) * ' '

# Find where the whitespace marker is for every single row
sep_idx = [0]
for iC in range(len(lines[0])):
    if all([line[iC] == ' ' for line in lines]):
        sep_idx.append(iC)
sep_idx.append(len(lines[0]))

total = 0
for idx in range(1, len(sep_idx) - 1):
    start_idx = sep_idx[idx] + 1
    stop_idx = sep_idx[idx + 1]
    nums = [line[start_idx:stop_idx][::-1] for line in lines[0:-1]]
    # print(nums)

    if not all([len(n) == len(nums[0]) for n in nums]):
        print('whoops')
    num_chars = len(nums[0])
    nums = [int(''.join([n[char_idx] for n in nums if n[char_idx] != ' '])) for char_idx in range(num_chars)]

    cum = None
    for iI, item in enumerate(nums):
        if cum is None:
            cum = item
        else:
            cum = op_lookup[operators[idx - 1]](cum, item)
    total += cum
    print(f'({operators[idx - 1]}) {nums} -> {cum}')
print(total)