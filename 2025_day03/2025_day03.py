def first_index(number: int, ary: list) -> int:
    if number not in ary:
        return -1
    
    return ary.index(number)


filename = '2025_day03/test_input.txt'
filename = '2025_day03/input.txt'
with open(filename) as f_in:
    lines = f_in.readlines()

parts = [(-1, 2), 
         (-11, 12)]

for ary_stop, num_values in parts:
    buf = []
    for line in lines:
        b = []
        battery_bank = [int(v) for v in line.strip()]
        # print(line.strip())
        
        # First value 
        for max_value in range(9, -1, -1):
            idx = first_index(max_value, battery_bank[0:ary_stop])
            if idx != -1:
                break
        b.append((idx, battery_bank[idx]))

        # Second value 
        while len(b) < num_values:
            # current_max = max_value
            start_idx = idx + 1
            for max_value in range(9, -1, -1):
                if ary_stop + len(b) == 0:
                    stop_idx = len(battery_bank)
                else:
                    stop_idx = ary_stop + len(b)
                idx = first_index(max_value, battery_bank[start_idx:stop_idx])
                if idx != -1:
                    break
            b.append((start_idx + idx, battery_bank[start_idx + idx]))
            idx = start_idx + idx

        # print(f'  {"".join([str(_b[1]) for _b in b])} -> {b}')
        buf.append(b)
        # break
    p1 = sum([int(''.join([str(v[1]) for v in b])) for b in buf])
    print(p1)