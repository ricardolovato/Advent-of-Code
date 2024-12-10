import numpy as np
import queue

filename = '2024_day10/test_input1.txt'
with open(filename) as f_in:
    lines = np.array([[v for v in line.strip()] for line in f_in.readlines()])

start_positions = [int(x) + 1j*int(y) for x, y in zip(*np.where(lines == '0'))]

directions = [-1, 1j, 1, -1j]


def within_bounds(location):
    # loc_re = np.real(location)
    # loc_im = np.imag(location)
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
    explored = {}
    Q = queue.Queue()
    explored[start_position] = 0
    Q.put(start_position)
    while not Q.empty():
        position = Q.get()
        if lines[imag2coord(position)] == '9':
            return True

        for edge in get_edges(position):
            if edge not in explored:
                explored[edge] = 0
                Q.put(edge)



for start_position in start_positions:
    BFS(start_position)