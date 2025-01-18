import re
filename = '2021_day02/test_input.txt'
filename = '2021_day02/input.txt'

with open(filename) as f_in:
    lines = f_in.readlines()

instructions = []
for line in lines:
    direction, distance = re.findall(r'(\w+)\s(\d+)', line)[0]
    instructions.append((direction, int(distance)))

directions = {'forward':1,
              'down':-1,
              'up':1}

x = 0
z = 0
for direction, distance in instructions:
    if direction == 'forward':
        x += distance
    elif direction in ['down', 'up']:
        z += directions[direction] * distance

print(f'x: {x}, z: {z}: {x*z}')

# Part 2
aim = 0
x = 0
z = 0
aim_directions = {'down':1, 'up':-1}
for direction, distance in instructions:
    if direction == 'forward':
        x += distance
        z += aim * distance
    elif direction in ['down', 'up']:
        aim += aim_directions[direction] * distance
    # print(f'{direction} {distance} -->\t x: {x}\t z: {z}\t aim: {aim}')
print(f'x: {x}, z: {z}: {x*z}')