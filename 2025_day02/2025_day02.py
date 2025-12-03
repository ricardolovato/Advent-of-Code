filename = '2025_day02/test_input.txt'
filename = '2025_day02/input.txt'

with open(filename) as f_in:
    line = f_in.readline()

nums_p1 = 0
nums_p2 = 0
for segment in line.strip().split(','):
    first_id, last_id = [int(v) for v in segment.split('-')]
    for current_id in range(first_id, last_id + 1):
        id_str = str(current_id)

        if len(id_str) == 1:
            continue 

        mid_pt = int(len(id_str)/2)

        if id_str[0:mid_pt] == id_str[mid_pt::]:            
            # print(segment)
            # print(f'\t{id_str}')
            nums_p1 += current_id

        # Quick check to see if all chars are the same
        if all(c == id_str[0] for c in id_str):
            print(f'{segment} -> {id_str} (all)')
            nums_p2 += current_id
            continue

        for str_len in range(2, mid_pt + 1):
            # If the number isn't cleanly divisible, skip
            # Ex: 3333330 for len 3 -> 333 333 0 
            # This catches the case where you have a repeat (333) but not the last digit
            if len(id_str)/str_len % 1 != 0:
                continue

            # Show intermediate progress
            # for idx in range(0, int(len(id_str)/str_len)):
                # print(f'{id_str[str_len*idx:str_len*idx+str_len]} ', end = '')
            # print()
            if all([id_str[0:str_len] == id_str[str_len*idx:str_len*idx+str_len] for idx in range(0, int(len(id_str)/str_len))]):
                print(f'{segment} -> {id_str} (len {str_len})')
                nums_p2 += current_id
                # Break dont continue or you double count 
                break 

print(nums_p1)
print(nums_p2)
