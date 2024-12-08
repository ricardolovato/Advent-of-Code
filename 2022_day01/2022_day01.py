filename = '2022_day01/test_input.txt'
filename = '2022_day01/input.txt'
with open(filename) as f_in:
    lines = f_in.readlines()

calories = []
while lines != []:
    value = lines.pop()
    c = []
    while value != '\n' and lines != []:
        c.append(int(value.strip()))
        value = lines.pop()
    calories.append(c)
print(f'max calories: {max([sum(v) for v in calories])}')

print(f'part 2: {sum(sorted([sum(v) for v in calories])[-3:])}')