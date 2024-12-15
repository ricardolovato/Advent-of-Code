import re
import numpy as np
import operator


def print_grid(grid):
    print('     ', end='')
    print(''.join([f'{i:^3}' for i in range(grid.shape[1])]))
    print('   ', end='')
    print(''.join(['---' for i in range(grid.shape[1])]) + '-')
    for iR, row in enumerate(grid):
        print(f'{iR:^2} | ', end='')
        print(''.join([f'{c:^3}' for c in row]))


def within_bounds(location):
    loc_re, loc_im = j2c(location)

    if loc_re < 0 or loc_re >= grid.shape[0]:
        return False
    if loc_im < 0 or loc_im >= grid.shape[1]:
        return False
    return True


def populate_grid(grid, robots):
    for position, velocity in robots:
        robot_coord = j2c(position)
        if grid[robot_coord] == '.':
            grid[robot_coord] = 1
        else:
            grid[robot_coord] = chr(ord(grid[robot_coord]) + 1)
    return grid


def show_robots(grid_shape, robots, mid_re=None, mid_im=None):
    grid = np.full(grid_shape, '.')
    grid = populate_grid(grid, robots)

    if mid_re is not None:
        grid[mid_re] = '-'
    if mid_im is not None:
        grid[:,mid_im] = '|'
    if mid_re is not None and mid_im is not None:
        grid[mid_re, mid_im] = '+'

    print_grid(grid)


def calculate_position(robot, time_sec):
    # v = d/t -> d = vt
    position, velocity = robot
    new_position = position + (velocity * time_sec)
    if not within_bounds(new_position):
        new_position_re = np.mod(np.real(new_position), grid.shape[0])
        new_position_im = np.mod(np.imag(new_position), grid.shape[1])
        new_position = new_position_re + 1j * new_position_im
    return new_position
    # show_robots(grid_shape, [[new_position, velocity]])


# Complex to coordinate
def j2c(p):
    return int(np.real(p)), int(np.imag(p))


filename = '2024_day14/test_input.txt'
grid_shape = (7, 11) # (Tall, Wide)

filename = '2024_day14/input.txt'
grid_shape = (103, 101) # (Tall, Wide)

with open(filename) as f_in:
    lines = f_in.readlines()

robots = []
for line in lines:
    pv = [int(v) for v in re.findall(fr'(-*\d+)', line)]
    robots.append([pv[1]+1j*pv[0], pv[3]+1j*pv[2]])

grid = np.full(grid_shape, '.')
show_robots(grid_shape, robots)

time = 100
for iR in range(len(robots)):
    robots[iR][0] = calculate_position(robots[iR], time)
show_robots(grid_shape, robots)

mid_re = grid_shape[0] // 2
mid_im = grid_shape[1] // 2

quad_operators = [[operator.lt, operator.lt], # top left quadrant
                  [operator.lt, operator.gt], # top right quadrant
                  [operator.gt, operator.gt], # bottom right quadrant
                  [operator.gt, operator.lt]] # bottom left quadrant


# safety_robots = [[robot for robot in robots if op1(np.real(robot[0]), mid_re) and op2(np.imag(robot[0]), mid_im)] for op1, op2 in quad_operators]
safety_robots = {iQ:[] for iQ in range(4)}
while robots:
    robot = robots.pop()
    for iQ, (op1, op2) in enumerate(quad_operators):
        if op1(np.real(robot[0]), mid_re) and op2(np.imag(robot[0]), mid_im):
            safety_robots[iQ].append(robot)
            break


for _, quad_robots in safety_robots.items():
    show_robots(grid_shape, quad_robots, mid_re, mid_im)
    # grid = populate_grid(grid, safety_robots)
safety_factor = int(np.prod([len(rb) for _, rb in safety_robots.items()]))
print(f'Safety factor: {safety_factor}')


# Part 2
robots = []
for line in lines:
    pv = [int(v) for v in re.findall(fr'(-*\d+)', line)]
    robots.append([pv[1]+1j*pv[0], pv[3]+1j*pv[2]])

vert = []
horiz = []
count = 0
vmr = [1]
while True:
    for iR in range(len(robots)):
        robots[iR][0] = calculate_position(robots[iR], 1)

    for i_reim in range(2):
        f = {0:np.real, 1:np.imag}[i_reim]
        hist, _ = np.histogram([f(robot[0]) for robot in robots],
                                bins=grid_shape[i_reim])

        mean = np.mean(hist)
        variance = np.var(hist)
        vmr.append(variance / mean)

        if vmr[-1] > 9 and i_reim == 0:
            vert.append(count)
        elif vmr[-1] > 9 and i_reim == 1:
            horiz.append(count)

    if len(vert) > 5 and len(horiz) > 5:
        break
    # print(vmr)
    count += 1
# print(vmr)
show_robots(grid_shape, robots)

print(f'Vertical repetition:    {np.diff(vert)}')
print(f'Horizontal repetition:  {np.diff(horiz)}')

vert_0 = vert[0]
horiz_0 = horiz[0]
vert_rep = np.diff(vert)[0]
horiz_rep = np.diff(horiz)[0]

print(f'Vertical pattern begins at {vert_0} and repeats every {vert_rep} repetitions:')
print(f'\tx ≡ {vert_0} (mod {vert_rep})')
print(f'\tx - {vert_0} is divisible by {vert_rep}')
print(f'Horizontal pattern begins at {horiz_0} and repeats every {horiz_rep} repetitions:')
print(f'\tx ≡ {horiz_0} (mod {horiz_rep})')

# a≡b (mod m) means that the difference a−b is divisible by m
# a≡b -> a mod m = b mod m
# a and b have the same remainder when divided by m
M = vert_rep * horiz_rep
M1 = M / vert_rep
M2 = M / horiz_rep

# M1 * y1 === 1 (mod M2)
# M1 * y1 - 1 % M2 == 0
y1 = 0
while (M1 * y1 - 1) % M2 != 0:
    y1 += 1
y2 = 0
while (M2 * y2 - 1) % M1 != 0:
    y2 += 1

# x = sum from i to n (a_i * M_i * y_i) mod M
time = (vert_0 * M1 * y1 + horiz_0 * M2 * y2) % M
time += 1

robots = []
for line in lines:
    pv = [int(v) for v in re.findall(fr'(-*\d+)', line)]
    robots.append([pv[1]+1j*pv[0], pv[3]+1j*pv[2]])

for iR in range(len(robots)):
    robots[iR][0] = calculate_position(robots[iR], time)
show_robots(grid_shape, robots)
print(time)