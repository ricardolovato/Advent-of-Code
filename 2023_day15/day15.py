import numpy as numpy
import re

with open('input.txt') as f_in:
    line = f_in.readlines()[0].strip()

def get_hash(segment):
    current_value = 0
    for c in segment:
        current_value += ord(c)
        current_value *= 17
        current_value = current_value % 256
    return current_value

def get_box_info(segment):
    if '-' in segment:
        delim = '-'
    else:
        delim = '='

    box_segment, focal_num = segment.split(delim)
    box_num = get_hash(box_segment)
    focal_label = f'{box_segment} {focal_num}'
    return box_num, focal_label

def compare_lens(l1, l2):
    return l1.split(' ')[0] == l2.split(' ')[0]

boxes = {i:[] for i in range(256)}
for segment in line.split(','):
    box_num, focal_label = get_box_info(segment)
    relevant_idx = [idx for idx, lens in enumerate(boxes[box_num]) if compare_lens(focal_label, lens)]

    if '=' in segment:
        if relevant_idx == []:
            boxes[box_num].append(focal_label)
        else:
            for idx in relevant_idx:
                boxes[box_num][idx] = focal_label

    if '-' in segment:
        for idx in relevant_idx:
            del boxes[box_num][idx]

power = []
for box_num, box_contents in boxes.items():
    for item_num, item in enumerate(box_contents):
        focal_length = int(item.split(' ')[1])
        p = (box_num + 1) * (item_num + 1) * focal_length
        power.append(p)
print(f'Power: {sum(power)}')




























