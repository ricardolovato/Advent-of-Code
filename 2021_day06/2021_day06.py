def print_fish(fish):
    for i in range(8, -1, -1):
        print(f'{i}: ', end = '')
        for day_num in range(len(fish[0])):            
            print(f'{fish[i][day_num]} ', end = '')
        print()

filename = '2021_day06/test_input.txt'
filename = '2021_day06/input.txt'
with open(filename) as f_in:
    numbers = f_in.readlines()
numbers = [int(v) for v in numbers[0].strip().split(',')]

fish = {i:[0] for i in range(9)}
# Initial state
for number in numbers:
    fish[number][-1] += 1

num_days = 256
for day in range(num_days):
    # Start at the top and work to 0 
    next_val = fish[8][-1]
    for i in range(7, -1, -1):
        current_val = fish[i][-1]
        fish[i].append(next_val)
        next_val = current_val
    
    fish[6][-1] += next_val
    fish[8].append(next_val)
    
# print_fish(fish)
print(sum([fish[i][-1] for i in range(0, 9)]))

