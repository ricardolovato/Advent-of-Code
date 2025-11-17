filename = '2021_day08/test_input.txt'
filename = '2021_day08/input.txt'
with open(filename) as f_in:
    lines = f_in.readlines()

input_segments, output_segments = [[line.strip().split(' ') for line in [line.split('|')[i] for line in lines]] for i in range(2)]


count = 0
for output_segment in output_segments:
    for current_number in output_segment:
        if len(current_number) in [2, 4, 3, 7]:
            # print(f'thats a bingo: {current_number}')
            count += 1

print(f'Total: {count}')


# Part 2
total = 0
for current_segment, output_segment in zip(input_segments, output_segments):
    segments = {i:None for i in range(7)}

    lens = {i:[] for i in range(2, 8)}
    for seg in current_segment:
        lens[len(seg)].append(seg)

    chars = lambda s: [_s for _s in s]
    
    # Need pairs that only overlap a single character using these positions:
    #     0000
    #    1    2
    #    1    2
    #     3333
    #    4    5
    #    4    5
    #     6666

    # Obvious ones
    one = lens[2][0]
    seven = lens[3][0]
    four = lens[4][0]
    eight = lens[7][0]

    # Segment 0:
    #    Character in 7 (len 3) not present in 4 (len 4) is position 0
    segments[0] = [c for c in chars(seven) if c not in chars(four)][0]

    # Number 3 will contain all characters from 1:
    three = [seg for seg in current_segment if all(c in seg for c in chars(one)) and len(seg) == 5][0]
    two_five = [seg for seg in lens[5] if seg != three]

    # We can compare 3 and 4 to get segment 1
    segments[1] = [c for c in chars(four) if c not in one and c not in three][0]

    # Same thing for segment 3 
    segments[3] = [c for c in chars(four) if c not in one and c in three][0]

    # Zero can be uniquely identified if it does not have segment 3 from len 6 group
    zero = [seg for seg in lens[6] if segments[3] not in seg][0]

    # Nine contains everything in 1 and we can exclude zero from len 6 group
    nine = [seg for seg in lens[6] if all(c in seg for c in chars(one)) and seg != zero][0]

    # Six is whatever is left from the len 6 group 
    six = [seg for seg in lens[6] if seg not in [zero, nine]][0]

    # Five can be identified by having five overlaps with 6 
    five = [seg for seg in two_five if all([c in six for c in chars(seg)])][0]
    # Two is whatever is left from two_five 
    two = [seg for seg in two_five if seg != five][0]

    #    1 (len 2) and 6 (len 6) share segment 5 
    segments[5] = [c for c in chars(one) if c in six][0]

    # Decode segment 1: 0 and 4 share position 1; 2 and 5 already decoded 
    segments[1] = [c for c in chars(zero) if c in four and c not in one][0]

    # Decode segment 2: 1 and 2 share position 2 
    segments[2] = [c for c in chars(one) if c in two][0]

    # Segment 4: 2 and 3 share all segments except 4 
    segments[4] = [c for c in chars(two) if c not in three][0]

    # Segment 6: Last reminaing, use 8 and take only unused char
    segments[6] = [c for c in chars(eight) if c not in [segments[i] for i in range(6)]][0]

    # print(f' {segments[0]*4}')
    # print(f'{segments[1]}    {segments[2]}')
    # print(f'{segments[1]}    {segments[2]}')
    # print(f' {segments[3]*4}')
    # print(f'{segments[4]}    {segments[5]}')
    # print(f'{segments[4]}    {segments[5]}')
    # print(f' {segments[6]*4}')

    # Table of segments needed for a number
    lookup = {0:[0,1,2,4,5,6],
            1:[2,5],
            2:[0,2,3,4,6],
            3:[0,2,3,5,6],
            4:[1,2,3,5],
            5:[0,1,3,5,6],
            6:[0,1,4,6,5,3],
            7:[0,2,5],
            8:[0,1,2,3,4,5,6],
            9:[0,1,2,3,5,6]}

    # Create the strings for each number (sorted) 
    numbers = {}
    for number in range(10):
        seg = ''.join(sorted([segments[i] for i in lookup[number]]))
        # print(f'{number}: {seg}')
        numbers[seg] = number

    # Compare this to what we have in the output
    output_num = []
    for seg in output_segment:
        seg = ''.join(sorted(seg))
        output_num.append(numbers[seg])
        # print(f'{seg}: {numbers[seg]}')

    # print(f'{output_segment}: {output_num}')
    total += int(''.join([str(s) for s in output_num]))
print(f'Total: {total}')