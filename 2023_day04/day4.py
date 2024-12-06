import numpy as np
import re

with open('input.txt') as f_in:
    lines = [d.strip() for d in f_in.readlines()]

cards = {}
card_pts = {}
for line in lines:
    card_num = int(re.findall('^Card\s+(\d+):.*', line)[0])
    
    numbers = line.split(': ')[1]
    winning_numbers = numbers.split(' | ')[0]
    winning_numbers = [int(n) for n in re.findall('(\d+)', winning_numbers)]

    my_numbers = numbers.split(' | ')[1]
    my_numbers = [int(n) for n in re.findall('(\d+)', my_numbers)]

    cards[card_num] = 0
    num_pts = 0
    for my_number in my_numbers:
        if my_number in winning_numbers:
            cards[card_num] += 1
            if num_pts == 0:
                num_pts = 1
            else:
                num_pts *= 2
    card_pts[card_num] = num_pts

    # break
# Part 1
total = sum([v for k, v in card_pts.items()])
print(total)


def count_cards(cards, card_num):
    num_matches = cards[card_num]
    if num_matches == 0: return []

    # print(card_num)
    all_cards = []
    for match_num in range(num_matches):
        card_copy_num = card_num + match_num + 1
        all_cards.append(card_copy_num)
        # print(f'\t{card_copy_num}')

        sub_cards = count_cards(cards, card_copy_num)
        if sub_cards != []:
            for v in sub_cards:
                all_cards.append(v)
    return all_cards


# Part 2
all_cards = []
for card_num, num_matches in cards.items():
    if num_matches == 0: 
        all_cards.append(card_num)
        continue
    
    all_cards.append(card_num)
    new_cards = count_cards(cards, card_num)
    if new_cards != []: 
        for v in new_cards:
            all_cards.append(v)

print(f'Total cards: {len(all_cards)}')



























