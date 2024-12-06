import numpy as np
import re

def check_char(c):
    if (c.isdigit() or c == '.'):
        return False
    else:
        return True

with open('input.txt') as f_in:
    lines = [_d.strip() for _d in f_in.readlines()]

schematic = np.array([[c for c in _d] for _d in lines])

# num_list = []
# for iR, row in enumerate(schematic):
#     # Find the numbers in the current line
#     line = lines[iR]
#     numbers_indices = [match.span() for match in re.finditer(r'(\d+)', line)]

#     for iN, (start_index, stop_index) in enumerate(numbers_indices):
#         number = int(''.join(row[start_index:stop_index]))

#         row_start_index = np.max([0, iR - 1])
#         row_stop_index = np.min([iR + 2, schematic.shape[1]])
#         col_start_index = np.max([0, start_index - 1])
#         col_stop_index = np.min([stop_index + 1, schematic.shape[0]])

#         search_grp = schematic[row_start_index:row_stop_index, col_start_index:col_stop_index]
#         if any([check_char(c) for c in search_grp.ravel()]):
#             num_list.append(number)
#             print(f'\n{number}')
#             print(search_grp)

# num_total = sum(num_list)
# print(num_total)

gear_sum = 0
for iR, row in enumerate(schematic):
    # Find the numbers in the current line
    line = lines[iR]

    gear_indices = [match.span() for match in re.finditer(r'(\*)', line)]
    for iG, (gear_index, _) in enumerate(gear_indices):
        row_start_index = np.max([0, iR - 1])
        row_stop_index = np.min([iR + 2, schematic.shape[1]])
        col_start_index = np.max([0, gear_index - 1])
        col_stop_index = np.min([gear_index + 2, schematic.shape[0]])

        search_grp = schematic[row_start_index:row_stop_index, col_start_index:col_stop_index]
        # print(f'\n{search_grp}') 

        # print(col_start_index)
        gear_numbers = []
        for row_index in np.arange(row_start_index, row_stop_index):
            current_start_index = col_start_index
            current_stop_index = col_stop_index
           
            # Move backwards 
            while current_start_index > 0:
                if schematic[row_index, current_start_index].isdigit():
                    current_start_index -= 1
                else:
                    break

            # Move forwards
            while current_stop_index < schematic.shape[1]:
                if schematic[row_index, current_stop_index - 1].isdigit():
                    current_stop_index += 1
                else:
                    break
            
            augmented_row = schematic[row_index, current_start_index:current_stop_index]
            # print(schematic[row_index])
            # print(augmented_row)
            # print()
            gear_numbers += [int(v) for v in re.findall(r'(\d+)', ''.join(augmented_row))]
        # print(gear_numbers)
        if len(gear_numbers) != 2:
            print(f'number of gear numbers on row {iR}, index {gear_index}: {len(gear_numbers)}')
        else:
            gear_sum += gear_numbers[0] * gear_numbers[1]

print(f'Gear sum: {gear_sum}')
































