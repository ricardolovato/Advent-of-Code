import numpy as np
import re

def get_sum(histories):
    sums = []
    for iH, history in enumerate(histories):
        hist_diff = [history] + [list(np.diff(history))]
        while not all(h == 0 for h in hist_diff[-1]):
            hist_diff.append(list(np.diff(hist_diff[-1])))
        for iL in np.arange(len(hist_diff)-1, 0, -1):
            current_end = hist_diff[iL][-1]
            next_end = hist_diff[iL-1][-1]

            # When iL - 1 = 0, this updates history in the original
            # histories array 
            hist_diff[iL - 1].append(next_end + current_end)

        sums.append(hist_diff[0][-1])

    return sums

with open('input.txt') as f_in:
    lines = [line.strip() for line in f_in.readlines()]
histories = [[int(v) for v in re.findall('(\-*\d+)', line)] for line in lines]

sums = get_sum(histories)
print(f'Part 1: {sum(sums)}')

sums = get_sum([h[::-1] for h in histories])
print(f'Part 2: {sum(sums)}')