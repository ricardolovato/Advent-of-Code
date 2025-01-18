import numpy as np
filename = '2024_day25/test_input1.txt'
filename = '2024_day25/input.txt'

with open(filename) as f_in:
    lines = [[v for v in line.strip()] for line in f_in.readlines()]

split_idx = [idx for idx, line in enumerate(lines) if line == []] + [len(lines)]
start_idx = 0

keys = []
locks = []
for stop_idx in split_idx:
    pins = np.array(lines[start_idx + 1:stop_idx - 1])
    pin_counts = [len(np.where(pin == '#')[0]) for pin in pins.T]

    if lines[start_idx] == ['.'] * 5:
        # print(f'{start_idx}: key')
        keys.append(pin_counts)
    elif lines[start_idx] == ['#'] * 5:
        # print(f'{start_idx}: lock')
        locks.append(pin_counts)
    else:
        print('something went wrong')

    start_idx = stop_idx + 1

combos = []
for lock in locks:
    for key in keys:
        b_all = True
        for pin_idx in range(5):
            if key[pin_idx] + lock[pin_idx] > 5:
                b_all = False
                break
        if b_all:
            combos.append((lock, key))
print(len(combos))