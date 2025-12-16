import re
from collections import deque


def bfs(desired_state, buttons):
    stack = deque([0])
    visited = {0:0}

    path = {}
    path_btn = {}

    while stack:
        current_state = stack.popleft()

        if current_state == desired_state:
            btn_sequence = []
            cs = current_state
            while cs in path:
                btn_sequence.append(path_btn[cs])
                cs = path[cs]

            return visited[current_state], btn_sequence

        for button in buttons:
            next_state = current_state ^ button 
            if next_state not in visited:
                visited[next_state] = visited[current_state] + 1
                stack.append(next_state)

                path[next_state] = current_state
                path_btn[next_state] = button 


def bfs_p2(buttons):
    start = tuple([0]*len(joltage))
    stack = deque([start])
    visited = {start:0}

    path = {}
    path_btn = {}
    goal_joltage = tuple(joltage)

    while stack:
        current_state = stack.popleft()

        if current_state == goal_joltage:# and btn_counts[current_state] == joltage:
            btn_sequence = []
            cs = current_state
            while cs in path:
                btn_sequence.append(path_btn[cs])
                cs = path[cs]

            return visited[current_state], btn_sequence

        for button in buttons:
            next_state = list(current_state)
            b_skip = False
            for idx in button_positions[button]:
                next_state[idx] += 1
                if next_state[idx] > goal_joltage[idx]:
                    b_skip = True
                    break
            if b_skip:
                continue
            next_state = tuple(next_state)

            if next_state not in visited:
                visited[next_state] = visited[current_state] + 1
                stack.append(next_state)

                path[next_state] = current_state
                path_btn[next_state] = button 


def convert_state(ary):
    state_int = 0
    for bit in ary:
        state_int = (state_int << 1) | bit
    # state_bin = bin(state_int) 
    return state_int

def button_bitmask(button):
    bm = [0] * num_bits
    for idx in button:
        bm[idx] = 1
    return convert_state(bm) 

filename = '2025_day10/test_input.txt'
filename = '2025_day10/input.txt'
with open(filename) as f_in:
    lines = f_in.readlines()

button_positions = {}
total_p1 = 0
total_p2 = 0
for line in lines:
    desired_state = re.findall(r'[\.|\#]', line)
    desired_state = [{'.':0, '#':1}[p] for p in desired_state]
    num_bits = len(desired_state)
    desired_state = convert_state(desired_state)

    buttons = re.findall(r'\(([^)]*)\)', line)
    for button in buttons:
        button_idx = tuple(int(b) for b in button.split(','))
        button_positions[button_bitmask([int(_b) for _b in button.split(',')])] = button_idx
    buttons = [button_bitmask([int(_b) for _b in b.split(',')]) for b in buttons]

    joltage = [int(_v) for _v in re.findall(r'\{([^\}]*)\}', line)[0].split(',')]

    state = 0
    num_presses, btn_sequence = bfs(desired_state, buttons)
    print(f'{num_presses} button presses: ', end = '')
    for btn in btn_sequence:
        print(f'{btn}, ', end = '')
    print()
    total_p1 += num_presses
    # break
    
    state = 0
    num_presses, btn_sequence = bfs_p2(buttons)
    print(f'{num_presses} button presses: ', end = '')
    for btn in btn_sequence:
        print(f'{btn}, ', end = '')
    print()
    total_p2 += num_presses

print(total_p1)
print(total_p2)