
filename ='2025_day01/test_input.txt'
filename ='2025_day01/input.txt'

with open (filename) as f_in:
    lines = f_in.readlines()

dial = list(range(100))
dial_idx = 50

count = 0
count_p2 = 0
for line in lines:
    direction = {'L':-1, 'R':1}[line[0]]
    turn = int(line[1::])

    new_position = dial_idx + direction * turn
    print(f'{dial[dial_idx]}: {line.strip()} -> {dial[new_position % 100]} ', end = '')

    if new_position == 0:
        print(f'\tclick 0 (1)', end = '')
        count_p2 += 1
    if new_position > 99:
        num_turns = abs(new_position // 100)
        print(f'\tclick + ({num_turns})', end = '')
        count_p2 += num_turns    
    elif new_position < 0:
        if dial_idx == 0:
            # Starting at zero
            num_turns = abs(new_position) // 100
        else:
            num_turns = (abs(direction * turn) - dial_idx) // 100 + 1

        print(f'\tclick - ({num_turns})', end = '')
        count_p2 += num_turns    

    dial_idx = new_position % 100

    print()

print()
print(f'Part 1: {count}')
print(f'Part 2: {count_p2}')
