from queue import Queue

class Part:
    def __init__(self, name: str):
        self.name = name
        self.state = 0
        self.inputs = []

    def __eq__(self, name):
        return self.name == name
    
    def __hash__(self,):
        return hash(self.name)
    
    def __str__(self, ):
        return self.name
    
    def connect_input(self, src):
        self.inputs.append(src)
        
    def receive_pulse(self, pulse_state):
        pulse_src, pulse_dst, pulse_level = pulse_state
        self.state = pulse_level

class FlipFlop(Part):
    def __init__(self, name: str):
        self.state = 0
        self.inputs = []
        self.outputs = []
        
        Part.__init__(self, name)
    
    def connect_input(self, src):
        self.inputs.append(src)
    
    def receive_pulse(self, pulse_state):
        pulse_src, pulse_dst, pulse_level = pulse_state
        
        pulses = []
        if pulse_level == 0:
            self.state = (self.state + 1) % 2
            # pulses.append(self.send_pulse(pulse_level=self.state))
            for dst in self.outputs:
                pulses.append((self, dst, self.state))
        return pulses
    
    def send_pulse(self, pulse_level: int):
        pulses = []
        for dst in self.outputs:
            pulses.append((self, dst, pulse_level))
        return pulses

class Conjunction(Part):
    def __init__(self, name: str):
        self.states = {}
        self.inputs = []
        self.outputs = []
        
        Part.__init__(self, name)

    def connect_input(self, src):
        self.inputs.append(src)
        self.states[src] = 0
    
    def receive_pulse(self, pulse_state):      
        pulse_src, pulse_dst, pulse_level = pulse_state  
        self.states[pulse_src] = pulse_level
        return self.send_pulse()
    
    def send_pulse(self):
        pulses = []
        if all(state == 1 for src, state in self.states.items()):
            output_pulse_level = 0
        else:
            output_pulse_level = 1

        for dst in self.outputs:
            pulses.append((self, dst, output_pulse_level))
        return pulses

class Broadcaster(Part):
    def __init__(self, name):
        self.inputs = []
        self.outputs = []

        Part.__init__(self, name)
    
    def connect_input(self, src):
        self.inputs.append(src)

    def receive_pulse(self, pulse_state):
        pulse_src, pulse_dst, pulse_level = pulse_state
        
        return self.send_pulse(pulse_level)
    
    def send_pulse(self, pulse_level:int) -> []:
        pulses = []
        for dst in self.outputs:
            pulses.append((self, dst, pulse_level))
        return pulses

def print_queue(pulse_queue):
    for iQ, pulse_state in enumerate(pulse_queue):
        pulse_src, pulse_dst, pulse_level = pulse_state
        print(f'{pulse_src} -> {pulse_dst} : {pulse_level}')
        
with open('input.txt') as f_in:
    lines = [line.strip() for line in f_in.readlines()]

# Create the part objects and record their connections
parts = []
part_relations = {}
for line in lines:
    src, dst = line[1:].split(' -> ')
    dst = [d.strip() for d in dst.split(',')]

    if src == 'roadcaster':
        src = 'broadcaster'
    part_relations[src] = dst

    if line[0] == '%':
        parts.append(FlipFlop(src))
    elif line[0] == '&':
        parts.append(Conjunction(src))
    elif 'broadcaster' in line:
        parts.append(Broadcaster('broadcaster'))
    
# Outputs with no connections
output_parts = []
for src_name, dst_names in part_relations.items():
    for dst_name in dst_names:
        if dst_name not in parts:
            # print(dst_name)
            parts.append(Part(dst_name))
            output_parts.append(dst_name)

# Make the connections between parts
for src_name, dst_names in part_relations.items():
    # print(f'Part ({src_name}) connected to ...')
    src_part = parts[parts.index(src_name)]

    for dst in dst_names:
        # print(f'\t{dst}')
        dst_part = parts[parts.index(dst)]
        src_part.outputs.append(dst_part)
        dst_part.connect_input(src_part)


def press_button(num_presses: int):
    pulse_count = [num_presses, 0]
    for i in range(num_presses):
        pulse_queue = []
        for pulse in parts[parts.index('broadcaster')].send_pulse(0):
            pulse_queue.append(pulse)
        # print_queue(pulse_queue)

        while pulse_queue:
            pulse_state = pulse_queue.pop(0)
            pulse_src, pulse_dst, pulse_level = pulse_state
            pulse_label = {0:'low', 1:'high'}[pulse_level]
            # print(f'{pulse_src} -{pulse_label}-> {pulse_dst}')
            pulse_count[pulse_level] += 1
                        
            if pulse_dst in output_parts:
                pulse_dst.receive_pulse(pulse_state)
                continue
            
            for new_state in pulse_dst.receive_pulse(pulse_state):
                pulse_queue.append(new_state)
    return pulse_count

# Part 1
num_presses = 1
pulse_count = press_button(num_presses)
print(f'Num presses: {num_presses}: --> ', end='')
print(f'low: {pulse_count[0]}; ', end='')
print(f'high: {pulse_count[1]}')
print(pulse_count[0] * pulse_count[1])


# Visually do part 2 
with open('graph.dot', 'w') as f_out:
    f_out.write('digraph {\n')
    for input_part, output_parts in part_relations.items():
        if type(parts[parts.index(input_part)]) == FlipFlop:
            f_out.write(f'{input_part} [shape=box color=red];\n')
        else:
            f_out.write(f'{input_part} [shape=circle color=blue];\n')
            
        for output_part in output_parts:
            f_out.write(f'{input_part} -> {output_part};\n')
    f_out.write('}')
    
counters = [0b111111010011,
            0b111110101101,
            0b111101001101,
            0b111011010001]

import math
print(f'LCM: {math.lcm(*counters)}')











