import operator
# filename = '2024_day07/test_input.txt'
filename = '2024_day07/input.txt'
with open(filename) as f_in:
    lines = [line.strip().split(':') for line in f_in.readlines()]

all_values = [int(v[0]) for v in lines]
all_numbers = [[int(_v) for _v in v[1].strip().split(' ')] for v in lines]
cat = lambda v1, v2: int(''.join([str(v) for v in [v1, v2]]))

def test_operators(value, numbers, op, num_valid=0):
    if len(numbers) == 1:
        return numbers[0] == value
    if numbers[-1] > value:
        return False

    if op != None:
        n1 = numbers.pop()
        n2 = numbers.pop()
        total = op(n1, n2)
        numbers.append(total)

    if test_operators(value, list(numbers), operator.mul):
        num_valid += 1
    if test_operators(value, list(numbers), operator.add):
        num_valid += 1
    if test_operators(value, list(numbers), cat):
        num_valid += 1
    return num_valid


cal_result = []
for value, numbers in zip(all_values, all_numbers):
    # print(f'{value}: {numbers}')

    # num_valid = 0
    valid = test_operators(value, numbers[::-1], None)
    # print(valid)
    if valid != 0:
        cal_result.append(value)
print(sum(cal_result))