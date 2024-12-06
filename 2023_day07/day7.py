import numpy as np
import re

class Hand:
    hand_type_ordered = ['high_card', 
                         'one_pair',
                         'two_pair',
                         'three_kind',
                         'full_house',
                         'four_kind',
                         'five_kind']
    # Part 1
    # card_type_ordered = ['2', '3', '4',
    #                      '5', '6', '7',
    #                      '8', '9', 'T',
    #                      'J', 'Q', 'K',
    #                      'A']
    # Part 2
    card_type_ordered = ['J', '2', '3', '4',
                        '5', '6', '7',
                        '8', '9', 'T',
                        'Q', 'K',
                        'A']

    def __init__(self, hand_str, bid = 0):
        self.hand_str = hand_str
        self.bid = bid

        self.determine_hand_type()

    def determine_hand_type(self,): 
        self.hand_chr = [v for v in self.hand_str]
        unique_chr = list(set(self.hand_chr))
        chr_counts = [len([v for v in self.hand_chr if v == c]) for c in unique_chr]
        
        # Part 2
        if 'J' in unique_chr:
            J_idx = unique_chr.index('J')
            J_count = chr_counts[J_idx]

            # Remove J's 
            unique_chr, chr_counts = [[v for iV, v in enumerate(ary) if iV != J_idx] for ary in [unique_chr, chr_counts]]
            chr_counts = sorted(chr_counts)

            # Edge case
            if J_count == 5:
                chr_counts = [5]
                unique_chr = ['J']
            else:
                chr_counts[-1] += J_count
        
        chr_counts = sorted(chr_counts)

        # Part 1
        # chr_counts = sorted([len([v for v in self.hand_chr if v == c]) for c in unique_chr])

        if len(unique_chr) == 1:
            self.hand_type = 'five_kind'
        elif len(unique_chr) == 2:
            if chr_counts == [1, 4]:
                self.hand_type = 'four_kind'
            elif chr_counts == [2, 3]:
                self.hand_type = 'full_house'
        elif len(unique_chr) == 3:
            if chr_counts == [1, 1, 3]:
                self.hand_type = 'three_kind'
            elif chr_counts == [1, 2, 2]:
                self.hand_type = 'two_pair'
        elif len(unique_chr) == 4:
            self.hand_type = 'one_pair'
        else:
            self.hand_type = 'high_card'

    def compare_hands(self, other_hand):
        self_rank, other_rank = [self.hand_type_ordered.index(h.hand_type) for h in [self, other_hand]]
        if self_rank > other_rank:
            return 1
        elif self_rank < other_rank:
            return 0
        
        for c_self, c_other in zip(self.hand_chr, other_hand.hand_chr):
            self_rank, other_rank = [self.card_type_ordered.index(c) for c in [c_self, c_other]]
            # print(f'{c_self}({self_rank}) - {c_other}({other_rank})')

            if self_rank > other_rank:
                return 1
            elif self_rank < other_rank:
                return 0
    
    def __gt__(self, other_hand):
        if self.compare_hands(other_hand) == 1:
            return True
        else:
            return False

    def __lt__(self, other_hand):
        if self.compare_hands(other_hand) == 1:
            return False
        else:
            return True

with open('input.txt') as f_in:
    lines = [line.strip() for line in f_in.readlines()]

hands = []
for hand_str, bid in [line.split(' ') for line in lines]:
    hands.append(Hand(hand_str, int(bid)))

    print(f'{hand_str}: {hands[-1].hand_type}')
print('')

# for hand in sorted(hands):
#     print(hand.hand_str)

hands = sorted(hands)
sum = 0
for iH, hand in enumerate(hands):
    print(f'{iH}: {hand.hand_str} - {hand.bid}')
    sum += (iH + 1) * hand.bid

# Part 2 breaks part 1
print(f'Sum: {sum}')

















