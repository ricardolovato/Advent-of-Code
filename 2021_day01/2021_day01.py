import numpy as np

filename = '2021_day01/test_input.txt'
filename = '2021_day01/input.txt'

with open(filename) as f_in:
    lines = [int(v) for v in f_in.readlines()]

num_greater = np.shape(np.where(np.diff(lines) > 0))[1]
print(num_greater)

# Part 2
new_lines = []
for i in range(0, len(lines) - 2):
    new_lines.append(lines[i] + lines[i + 1] + lines[i + 2])

num_greater = np.shape(np.where(np.diff(new_lines) > 0))[1]
print(num_greater)