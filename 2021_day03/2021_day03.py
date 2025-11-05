import numpy as np
filename = '2021_day03/test_input.txt'
filename = '2021_day03/input.txt'
with open(filename) as f_in:
    bits = np.array([[int(v) for v in line.strip()] for line in f_in.readlines()])

gamma_bits = []
for current_bits in bits.T:
    if sum(current_bits) > bits.shape[0]/2:
        gamma_bits.append(1)
    else:
        gamma_bits.append(0)

b2d = lambda bits, flip: sum([2**pow for pow, bit in enumerate(gamma_bits[::-1]) if bit == flip])

gamma, epsilon = [b2d(gamma_bits, flip) for flip in [1, 0]]
print(f'Sum: {gamma * epsilon}')