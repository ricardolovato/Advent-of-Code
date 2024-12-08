import re

# Part 1
filename = 'input.txt'
with open(filename) as f_in:
    lines = f_in.readlines()

total = 0
for line in lines:
    # print(line)
    nums = re.findall(r'mul\((\d+),(\d+)\)', line)
    nums = [[int(v[0]), int(v[1])] for v in nums]

    line_sum = [v[0] * v[1] for v in nums]
    total += sum(line_sum)
# print(total)


# Part 2
filename = 'test_input2.txt'
filename = 'input.txt'
with open(filename) as f_in:
    lines = f_in.readlines()

b_mul = True
total = 0
for line in lines:
    print(line)
    nums = re.findall(r'(do\(\))|(don\'t\(\))|mul\((\d+),(\d+)\)', line)[::-1]
    while nums:
        value = nums.pop()
        if value[0] != '':
            b_mul = True
        elif value[1] != '':
            b_mul = False
        else:
            if b_mul:
                print(value)
                total += int(value[2]) * int(value[3])

# 75466465 too high
# 59097164
print(total)