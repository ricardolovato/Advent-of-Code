filename = '2022_day06/input.txt'
# filename = '2022_day06/test_input.txt'

with open(filename) as f_in:
    lines = [line.strip() for line in f_in.readlines()]

for line in lines:
    contents = list(line[::-1])
    char_count = 0
    sequential = []
    while contents != [] and len(sequential) != 14:
        c = contents.pop()
        if c not in sequential:
            sequential.append(c)
        else:
            idx = sequential.index(c)
            sequential = sequential[idx+1:] + [c]
        # print(f'{c:}:\n\t{"".join(sequential)}')
        char_count += 1
    print(f'{char_count}')