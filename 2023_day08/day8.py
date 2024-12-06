import numpy as np
import re

def get_nodes(lines):
    sequence = [{'L':0, 'R':1}[c] for c in lines[0]]

    nodes = {}
    for line in lines[2::]:
        current_node, next_L, next_R = re.findall('(\w{3})', line)
        nodes[current_node] = (next_L, next_R)
    return sequence, nodes

with open('input.txt') as f_in:
    lines = [line.strip() for line in f_in.readlines()]

sequence, nodes = get_nodes(lines)

steps = 0
current_node = 'AAA'
while current_node != 'ZZZ':
    for next_node in sequence:
        current_node = nodes[current_node][next_node]
        steps += 1
        if current_node == 'ZZZ':
            break

print(f'Step 1: {steps}')

with open('input.txt') as f_in:
    lines = [line.strip() for line in f_in.readlines()]

sequence, nodes = get_nodes(lines)
current_nodes = [current_node for current_node, (_, _) in nodes.items() if current_node[-1] == 'A']

# Brute Force
# steps = 0
# check_nodes = lambda current_nodes: all(current_node[-1] == 'Z' for current_node in current_nodes)
# while not check_nodes(current_nodes):
#     for next_node in sequence:
#         current_nodes = [nodes[cn][next_node] for cn in current_nodes]
#         # print(current_nodes)
#         steps += 1
#         if check_nodes(current_nodes):
#             break

# print(f'Step 2: {steps}')



def get_matches(current_node, iterations_limit, steps):
    hits = []
    # steps = 0
    iterations = 0
    while iterations < iterations_limit:
        for next_node in sequence:
            current_node = nodes[current_node][next_node]
            steps += 1
            if current_node[-1] == 'Z':
                hits.append(steps)
        iterations += 1
    return current_node, hits, steps

def check_matches(matches):
    shortest_idx = np.argmin([len(ary) for ary in matches])
    for v in matches[shortest_idx]:
        if all(v in ary for ary in matches):
            return True, v
    
    return False, 0

lowest_found = False
matches = [[] for i in range(len(current_nodes))]
steps = [0 for i in range(len(current_nodes))]
# while not lowest_found:
for iC in range(len(current_nodes)):
    current_node, hits, s = get_matches(current_nodes[iC], 
                                        iterations_limit=50, 
                                        steps=steps[iC])
    current_nodes[iC] = current_node
    steps[iC] = s
    for h in hits:
        matches[iC].append(h)
    # print(matches)

    # lowest_found, lowest_match = check_matches(matches)






























