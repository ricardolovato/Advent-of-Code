filename = '2021_day08/test_input.txt'
filename = '2021_day08/input.txt'
with open(filename) as f_in:
    lines = f_in.readlines()
# numbers = [int(v) for v in numbers[0].strip().split(',')]

output_segments = [line.strip().split(' ') for line in [line.split('|')[1] for line in lines]]

count = 0
for output_segment in output_segments:
    for current_number in output_segment:
        if len(current_number) in [2, 4, 3, 7]:
            print(f'thats a bingo: {current_number}')
            count += 1

print(f'Total: {count}')
