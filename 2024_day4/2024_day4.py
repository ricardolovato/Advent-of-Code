import numpy as np
filename = 'test_input2.txt'
# filename = 'input.txt'

# Part 1
with open(filename) as f_in:
    lines = np.array([[_v for _v in v.strip()] for v in f_in.readlines()])

data = np.full((lines.shape[0] + 6, lines.shape[1] + 6), '.', dtype=str)
data[3:lines.shape[0]+3, 3:lines.shape[1]+3] = lines
# print(data)

s = ['X', 'M', 'A', 'S']
directions = [(0, 1),   # East
              (1, 1),   # SE Diagonal
              (1, 0),   # South
              (1, -1),  # SW Diagonal
              (0, -1),  # West
              (-1, -1), # NW Diagonal
              (-1, 0),  # North
              (-1, 1),  # NE Diagonal
]

count = 0
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        if data[i,j] == 'X':
            # check grid
            for (dx, dy) in directions:
                if ''.join([data[i + iS * dx, j + iS * dy] for iS, ch in enumerate(s)]) == 'XMAS':
                    count += 1
# print(count)



filename = 'test_input2.txt'
filename = 'input.txt'

# Part 2
with open(filename) as f_in:
    lines = np.array([[_v for _v in v.strip()] for v in f_in.readlines()])

data = np.full((lines.shape[0] + 6, lines.shape[1] + 6), '.', dtype=str)
data[3:lines.shape[0]+3, 3:lines.shape[1]+3] = lines
# print(data)


s = ['M', 'A', 'S']
directions = [[(-1, -1), (0, 0), (1,  1)], # Northwest to southeast
              [(-1,  1), (0, 0), (1, -1)], # Northeast to southwest
              [(1, 1), (0, 0), (-1, -1)], # Southeast to Northwest
              [(1, -1), (0, 0), (-1, 1)]] # Southwest to Northeast

count = 0
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        if data[i,j] == 'A':
            # check grid

            num_matches = 0
            for d in directions:
                if ''.join([data[i + dx, j + dy] for (dx, dy) in d]) in ['MAS', 'SAM']:
                    num_matches += 1
            if num_matches == 4:
                count += 1
print(count)

