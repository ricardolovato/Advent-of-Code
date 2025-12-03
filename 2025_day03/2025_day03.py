def first_index(number: int, ary: list) -> int:
    if number not in ary:
        return -1
    
    return ary.index(number)


filename = '2025_day03/test_input.txt'
filename = '2025_day03/input.txt'
with open(filename) as f_in:
    lines = f_in.readlines()

buf = []
for line in lines:
    b = []
    battery_bank = [int(v) for v in line.strip()]
    print(line.strip())
    
    # First value 
    for max_value in range(9, -1, -1):
        idx = first_index(max_value, battery_bank[0:-1])
        if idx != -1:
            break
    b.append((idx, battery_bank[idx]))

    # Second value 
    current_max = max_value
    start_idx = idx + 1
    for max_value in range(9, -1, -1):
        idx = first_index(max_value, battery_bank[start_idx::])
        if idx != -1:
            break
    b.append((start_idx + idx, battery_bank[start_idx + idx]))

    print(b)
    buf.append(b)
    # break
p1 = sum([int(''.join([str(v) for v in [b[0][1], b[1][1]]])) for b in buf])
print(p1)