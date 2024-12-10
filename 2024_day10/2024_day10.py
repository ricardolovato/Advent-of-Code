import numpy as np
import queue

filename = '2024_day10/input.txt'
# filename = '2024_day10/test_input3.txt'
with open(filename) as f_in:
    lines = np.array([[v for v in line.strip()] for line in f_in.readlines()])

start_positions = [int(x) + 1j*int(y) for x, y in zip(*np.where(lines == '0'))]

directions = [-1, 1j, 1, -1j]


def within_bounds(location):
    loc_re, loc_im = imag2coord(location)

    if loc_re < 0 or loc_re >= lines.shape[0]:
        return False
    if loc_im < 0 or loc_im >= lines.shape[1]:
        return False
    return True

def imag2coord(p):
    return int(np.real(p)), int(np.imag(p))

def get_edges(position):
    edges = []
    for direction in directions:
        edge = position + direction
        if not within_bounds(edge):
            continue

        value = lines[imag2coord(edge)]
        if ord(value) == ord(lines[imag2coord(position)]) + 1:
            edges.append(edge)
    return edges

def BFS(start_position):
    paths = []
    explored = {}
    Q = queue.Queue()
    explored[start_position] = 0
    Q.put(start_position)
    while not Q.empty():
        position = Q.get()
        if lines[imag2coord(position)] == '9':
            paths.append(position)

        for edge in get_edges(position):
            if edge not in explored or explored[edge] == len(paths):
                explored[edge] = len(paths)
                Q.put(edge)
    return paths

trails = {}
for start_position in start_positions:
    trails[start_position] = BFS(start_position)
print(trails)
print(sum([len(v) for k, v in trails.items()]))