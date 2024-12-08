import numpy as np
import re

letters = [letter for letter in 'abcdefghijklmnopqrstuvwxyz']
for iL in range(26):
    letters.append(letters[iL].upper())

with open('input.txt') as f_in:
    bags = [line.strip() for line in f_in.readlines()]

items = []
for iB, bag in enumerate(bags):
    if len(bag) % 2 != 0:
        print('something is wrong')

    compartment_len = int(len(bag)/2)
    contents = [bag[start_idx:stop_idx] for start_idx, stop_idx in [(0, compartment_len), (compartment_len, compartment_len * 2)]]

    common_item = [letter for letter in letters if all(letter in compartment for compartment in contents)]
    if len(common_item) != 1:
        print('Too many items in compartment')
    common_item = common_item[0]
    item_priority = letters.index(common_item) + 1
    # print(f'{iB}: {common_item} ({item_priority})')

    items.append([common_item, item_priority])

    # break

item_sum = sum([item[1] for item in items])
print(f'Item sum: {item_sum}')

badges = []
for iB in np.arange(0, len(bags), 3):
    badge_item = [letter for letter in letters if all(letter in bag for bag in [bags[iB + 0], bags[iB + 1], bags[iB + 2]])]
    
    if len(badge_item) != 1:
        print('Too many items in compartment')
    badge_item = badge_item[0]
    item_priority = letters.index(badge_item) + 1
    # print(f'{iB}: {badge_item} ({item_priority})')
    badges.append([badge_item, item_priority])

badge_sum = sum([item[1] for item in badges])
print(f'Badge sum: {badge_sum}')



























