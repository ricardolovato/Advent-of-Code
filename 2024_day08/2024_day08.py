import string

import numpy as np

filename = '2024_day08/input.txt'
filename = '2024_day08/test_input3.txt'

def print_grid(grid):
    print('     ', end='')
    print(''.join([f'{i:^3}' for i in range(grid.shape[1])]))
    print('   ', end='')
    print(''.join(['---' for i in range(grid.shape[1])]) + '-')
    for iR, row in enumerate(grid):
        print(f'{iR:^2} | ', end='')
        print(''.join([f'{c:^3}' for c in row]))

def visualize_map(lines, nodes, antinodes):
    ary = np.full(lines.shape, '.')

    for iT, thing in enumerate([nodes, antinodes]):
        for node_name, node_locations in thing.items():
            for node_location in node_locations:
                node_x, node_y = [int(f(node_location)) for f in [np.real, np.imag]]
                ary[node_x, node_y] = {0:node_name,
                                       1:'#'}[iT]
    print_grid(ary)


with open(filename) as f_in:
    lines = np.array([[c for c in line.strip()] for line in f_in.readlines()])

is_alphanum = np.vectorize(lambda c: c.isalnum())
# nodes = [int(x) + 1j*int(y) for x, y in zip(*np.where(is_alphanum(lines)))]
nodes = {}
for iX in range(lines.shape[0]):
    for iY in range(lines.shape[1]):
        c = str(lines[iX, iY])
        if is_alphanum(c):
            if c not in nodes:
                nodes[c] = [iX + 1j*iY]
            else:
                nodes[c].append(iX + 1j*iY)
print(nodes)

antinodes = {}
for node_name, node_locations in nodes.items():
    antinodes[node_name] = []
    for node1 in node_locations:
        for node2 in node_locations:
            if node1 == node2:
                continue
            d = node1-node2
            print(f'{node1} -> {node2} = {d}')
            antinode_location = node1 + d
            if np.real(antinode_location) < lines.shape[0] and np.imag(antinode_location) < lines.shape[1]:
                antinodes[node_name].append(node1 + d)
visualize_map(lines, nodes, antinodes)