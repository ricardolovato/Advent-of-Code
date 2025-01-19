import numpy as np
filename = '2021_day03/test_input.txt'
filename = '2021_day03/input.txt'
with open(filename) as f_in:
    bits = np.array([[int(v) for v in line.strip()] for line in f_in.readlines()])

gamma = []
for col_num in range(len(bits[0])):
    num_0, num_1 = [np.where(bits.T[col_num] == v)[0].shape[0] for v in [0, 1]]
    if num_0 > num_1:
        gamma.append(0)
    else:
        gamma.append(1)

# Binary addition
gamma, epsilon = [sum([2**pow for pow, i in enumerate(gamma[::-1]) if i == rate]) for rate in [1, 0]]
print(gamma * epsilon)