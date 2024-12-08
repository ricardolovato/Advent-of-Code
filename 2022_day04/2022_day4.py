import numpy as np
import re

def pair_contains(r1, r2):
    if all(r >= r2[0] and r <= r2[1] for r in r1):
        return True
    else:
        return False
      
def pair_overlaps(r1, r2):
    if any(r >= r2[0] and r <= r2[1] for r in r1):
        return True
    else:
        return False  


with open('input.txt') as f_in:
    pairs = [line.strip() for line in f_in.readlines()]

contain_count = 0
overlap_count = 0
for pair in pairs:
    nums = [int(v) for v in re.findall(r'(\d+)', pair)]

    range_1 = (nums[0], nums[1])
    range_2 = (nums[2], nums[3])

    if any(pair_contains(r1, r2) for r1, r2 in [[range_1, range_2], [range_2, range_1]]):
        # print(f'{pair}')
        contain_count += 1

    if any(pair_overlaps(r1, r2) for r1, r2 in [[range_1, range_2], [range_2, range_1]]):
        # print(f'{pair}')
        overlap_count += 1


print(f'Contains: {contain_count}')
print(f'Overlaps: {overlap_count}')

    

































