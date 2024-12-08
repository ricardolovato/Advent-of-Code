# Part 1
with open('input.txt') as f_in:
    lines = [[int(v) for v in line.strip().split(' ')] for line in f_in.readlines()]

count = 0
for line in lines:
    # print(line)
    diffs = [line[idx] - line[idx - 1] for idx in range(1, len(line))]

    # All levels are increasing or decreasing
    all_neg = all(d < 0 for d in diffs)
    all_pos = all(d > 0 for d in diffs)
    if not (all_neg or all_pos):
        # print('Not all neg or pos')
        continue

    within_bounds = all(abs(d) > 0 and abs(d) <= 3 for d in diffs)
    if not within_bounds: 
        # print('Not within bounds')
        continue

    # print('safe')
    count += 1

# print(count)



# Part 2
def check_levels(line):
    diffs = [line[idx] - line[idx - 1] for idx in range(1, len(line))]
    print(f'{line} -> {diffs}')

    num_neg = len([d for d in diffs if d < 0])
    num_pos = len([d for d in diffs if d > 0])
    
    if num_neg > num_pos:
        b_pos = False
    else:
        b_pos = True

    # First check: all increasing or decreasing
    for idx in range(0, len(diffs)):
        # if (diffs[idx] < 0 and diffs[idx - 1] > 0) or (diffs[idx] > 0 and diffs[idx - 1] < 0) or diffs[idx] == 0:
        if (diffs[idx] < 0 and b_pos) or (diffs[idx] > 0 and not b_pos) or diffs[idx] == 0:
            if diffs[idx] == 0:
                bad_idx = [idx - 1, idx, idx + 1]
            else:
                print(f'Issue found at diffs index {idx} = {diffs[idx]}')
                # neg_idx = [i for i in [idx, idx - 1] if diffs[i] < 0][0]
                # pos_idx = [i for i in [idx, idx - 1] if diffs[i] > 0][0]
                bad_idx = [idx - 1, idx, idx + 1]
                
                # # Find the index that is not like the rest
                # if num_neg > num_pos:
                #     print(f'\tComparing numbers {line[idx]}, {line[idx + 1]} to give diff {diffs[idx]}')
                #     if line[idx] < line[idx + 1]:
                #         bad_idx = idx
                #         print(f'\t{line[idx]} < {line[idx + 1]}: returning line idx {bad_idx} = {line[bad_idx]}')
                #     else:
                #         bad_idx = idx + 1
                #         print(f'\t{line[idx]} > {line[idx + 1]}: returning line idx {bad_idx} = {line[bad_idx]}')
                #
                # elif num_pos > num_neg:
                #     if line[idx] > line[idx + 1]:
                #         bad_idx = idx + 1
                #         print(f'\t{line[idx]} > {line[idx + 1]}: returning line idx {bad_idx} = {line[bad_idx]}')
                #     else:
                #         bad_idx = idx
                #         print(f'\t{line[idx]} < {line[idx + 1]}: returning line idx {bad_idx} = {line[bad_idx]}')
                # else:
                #     print('error: shouldnt be possible to get here')

            print(f'\tFailed increasing/decreasing test at diffs index {bad_idx}')
            return bad_idx
    
    # Second check: within bounds
    for idx in range(len(diffs)):
        if not (abs(diffs[idx]) > 0 and abs(diffs[idx]) <= 3):
            print(f'\tFailed bounds check at diff index {idx}')
            return [idx - 1, idx, idx + 1]
    
    return [None]


input_file = 'input.txt'
# input_file = 'test_input.txt'
# input_file = 'test_input2.txt'

with open(input_file) as f_in:
    lines = [[int(v) for v in line.strip().split(' ')] for line in f_in.readlines()]

count = 0
for line in lines:
    problem_indices = check_levels(line)

    if problem_indices != [None]:
        b_any_pass = False
        for problem_idx in problem_indices:
            current_line = [line[idx] for idx in range(len(line)) if idx != problem_idx]
            current_problem_indices = check_levels(current_line)
            # if problem_idx is [None]:
            if any(v is None for v in current_problem_indices):
                b_any_pass = True
                break

        if not b_any_pass:
            print('unsafe')
            continue



    # line = [line[idx] for idx in range(len(line)) if idx != problem_idx]
    # problem_idx = check_levels(line)

    # if problem_idx != None:
    #     print('unsafe')
    #     continue

    count += 1
    print('safe')
    
# 405, 406, 415 is too low
print(count)