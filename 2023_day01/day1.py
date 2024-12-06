import numpy as np
import time
import re


def get_sum(lines, regex_expr):
    nums = [re.findall(regex_expr, _d) for _d in lines]

    num_map = {'one':'1',
            'two':'2',
            'three':'3',
            'four':'4',
            'five':'5',
            'six':'6',
            'seven':'7',
            'eight':'8',
            'nine':'9',
                '1':'1',
                '2':'2',
                '3':'3',
                '4':'4',
                '5':'5',
                '6':'6',
                '7':'7',
                '8':'8',
                '9':'9'}

    sum = 0
    for iN, num in enumerate(nums):
        if len(num) == 1:
            n = num_map[num[0]]
            sum += int(f'{n}{n}')
        else:
            n1 = num_map[num[0]]
            n2 = num_map[num[-1]]
            sum += int(f'{n1}{n2}')
    return sum


with open('input.txt') as f_in:
    lines = [_d.strip() for _d in f_in.readlines()][0:-1]

print(get_sum(lines, '(\d)'))


num_str = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', '\d']
num_regex = '|'.join(num_str)
num_regex = f'(?=({num_regex}))'

print(get_sum(lines, num_regex))

# for iL in np.arange(len(lines)):
#     for num_word in re.findall(num_regex, lines[iL]):
#         lines[iL] = lines[iL].replace(num_word, num_map[num_word])
# print(get_sum(lines))