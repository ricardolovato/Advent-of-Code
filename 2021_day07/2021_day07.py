filename = '2021_day07/test_input.txt'
filename = '2021_day07/input.txt'
with open(filename) as f_in:
    numbers = f_in.readlines()
numbers = [int(v) for v in numbers[0].strip().split(',')]

median = sorted(numbers)[int(len(numbers)/2)]
mean = sum(numbers)/len(numbers)
print(f'median: {median}, mean: {mean}')
for n in range(median-10,median+11):
    s = sum([abs(v - n) for v in numbers])
    print(f'{n}: {s}')

# Part 2
x = []
y = []
for n in range(int(mean)-10,int(mean)+11):
    s2 = sum([sum(list(range(abs(v - n) + 1))) for v in numbers])
    print(f'{n}: {s2}')
    x.append(n)
    y.append(s2)

plt.plot(x,y)

print(f'Min value: {x[y.index(min(y))]} -> {min(y)}')