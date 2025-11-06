import numpy as np
import re

def search_card(card, number):
    idx = []
    for i in range(len(card)):
        for j in range(len(card[0])):
            if card[i][j] == number:
                idx.append([i, j])
    return idx

def is_bingo(card, current_matches):
    #unique_rows, unique_cols = [list(set(v)) for v in np.array(card).T]
    # Just hardcode 5 rows and cols 

    # Number of times an index appears in either a row or col
    num_elements = [[len([_v for _v in v if _v == i]) for v in np.array(current_matches).T] for i in range(5)]
    return any(v == 5 for v in [_v for v in num_elements for _v in v ])

def get_bingo(cards, b_p2 = False):
    winning_cards = []
    bingos = []
    matches = [[] for i in range(len(cards))]
    for iN, number in enumerate(numbers):
        #if number == 10: break
        for iC, card in enumerate(cards):
            if tuple(card.reshape(25)) in winning_cards:
                continue
            # Check if the number is in the current card 
            for current_pair in search_card(card, number):
                matches[iC].append(current_pair)
            
            # Test bingo-ness 
            if is_bingo(card, matches[iC]):
                print(f'that\'s a bingo: card {iC} at number {iN}')
                if not b_p2: 
                    return card, matches[iC], number
                else:
                    winning_cards.append(tuple(card.reshape(25)))
                    bingos.append([card, matches[iC], number])
    return bingos[-1]

def calculate_score(card, current_matches, number):
    unmatched = []
    for i in range(len(card)):
        for j in range(len(card[0])):
            if [i, j] in current_matches: 
                continue
            unmatched.append(card[i][j])
    print(np.sum(unmatched) * number)

filename = '2021_day04/test_input.txt'
filename = '2021_day04/input.txt'

with open(filename) as f_in:
    lines = f_in.readlines()

numbers = [int(v) for v in lines[0].strip().split(',')]
start_indices = [idx for idx,line in enumerate(lines) if line == '\n']

cards = []
for idx, line_idx in enumerate(start_indices):
    current_card = lines[line_idx+1:line_idx + 6]
    current_card = np.array([re.findall(r'(\d+)', line) for line in current_card], dtype = np.int64)

    cards.append(current_card)

card, current_matches, number = get_bingo(cards)
calculate_score(card, current_matches, number)

# Part 2

card, current_matches, number = get_bingo(cards, True)
calculate_score(card, current_matches, number)