import numpy as np
import re

with open('input.txt') as f_in:
    lines = [line for line in f_in.readlines()]

number_idx = lines.index('\n') - 1

box_line = lines[number_idx]
number_indices = [match.span()[0] for match in re.finditer(r'(\d+)', box_line)]

box_numbers = [box_line[idx] for idx in number_indices]
boxes = np.array([[line[idx] for idx in number_indices] for line in lines[0:number_idx]])

stacks = {}
for box_number, box in zip(box_numbers, boxes.T):
    stacks[box_number] = [b for b in box if b != ' '][::-1]

for instruction in lines[number_idx + 2::]:
    qty, src, dst = re.findall('move (\d+) from (\d) to (\d)', instruction)[0]
    qty = int(qty)

    src_stack_len = len(stacks[src])
    items = stacks[src][src_stack_len - qty::]
    stacks[src] = stacks[src][0:src_stack_len - qty]
    stacks[dst] += items

    # for i in range(int(qty)):
    #     item = stacks[src][-1]
    #     stacks[src] = stacks[src][0:-1]
    #     stacks[dst].append(item)

top_stack = ''.join([stack[-1] for stack_num, stack in stacks.items()])
print(f'{top_stack}')






























