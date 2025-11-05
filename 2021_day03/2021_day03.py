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

b2d = lambda bits, flip: sum([2**pow for pow, bit in enumerate(bits[::-1]) if bit == flip])

gamma, epsilon = [b2d(gamma_bits, flip) for flip in [1, 0]]
print(f'Sum: {gamma * epsilon}')

# Part 2
ratings = []
for func in [np.greater_equal, np.less]:
    test_bits = np.array(bits)
    for iB in range(test_bits.shape[1]):
        if len(test_bits) == 1: 
            break

        current_bits = test_bits.T[iB]
        mcb = {True:1, False:0}[func(sum(current_bits), test_bits.shape[0]/2)]

        test_bits = np.array([b for b in test_bits if b[iB] == mcb])
    ratings.append(b2d(test_bits[0],  1))

o2_rating = ratings[0]
co2_rating = ratings[1]
print(f'Oxygen generator rating: {o2_rating}')
print(f'CO2 scrubber rating: {co2_rating}')
print(f'{o2_rating * co2_rating}')