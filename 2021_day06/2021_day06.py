def print_fish(fish):
    for fish_num, num_fish in fish.items():
        print(f'{fish_num}:\t{num_fish}')
    print('-'*12)

filename = '2021_day06/test_input.txt'
with open(filename) as f_in:
    numbers = f_in.readlines()
numbers = [int(v) for v in numbers[0].strip().split(',')]

fish = {i:[0] for i in range(9)}
# Initial state
for number in numbers:
    fish[number][-1] += 1

# print_fish(fish)
num_days = 18
for day in range(num_days + 1):
    # Shuffle them down 
    next_val = fish[0][-1]
    for i in range(8):
        current_val = fish[i][-1]
        fish[i].append(next_val)
        next_val = current_val
    
    fish[6][-1] += next_val
    fish[8].append(next_val)
    
    # print_fish(fish)
a = 1
