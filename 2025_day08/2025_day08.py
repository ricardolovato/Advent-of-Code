import numpy as np
import math 
class Point:
    def __init__(self, num):
        self.x = num[0]
        self.y = num[1]
        self.z = num[2] 
    
    def __sub__(self, p2) -> float:
        dx = self.x - p2.x
        dy = self.y - p2.y
        dz = self.z - p2.z
        return math.sqrt(dx**2 + dy**2 + dz**2)

    def __str__(self):
        return f'{self.x}, {self.y}, {self.z}'
    

def merge_circuits(circuits):
    merge = set()
    for iC, circuit1 in enumerate(circuits):
        for jC, circuit2 in enumerate(circuits):
            if iC == jC: 
                continue
            if any(p in circuit1 for p in circuit2):
                merge.add(tuple(sorted([iC, jC])))

    # merged_circuits = [circuit for iC, circuit in enumerate(circuits) if iC not in merge] 
    merged_circuits = []
    for iC, circuit in enumerate(circuits):
        if not any([iC in m for m in merge]):
            merged_circuits.append(circuit)
    for iC, jC in merge:
        merged_circuits.append(set([element for idx in [iC, jC] for element in circuits[idx] ]))
    return merged_circuits


filename = '2025_day08/test_input.txt'
filename = '2025_day08/input.txt'

stop_connections = {'2025_day08/test_input.txt':10,
                    '2025_day08/input.txt':1000}[filename]
with open(filename) as f_in:
    lines = f_in.readlines()

locations = [[int(_v) for _v in v.strip().split(',')] for v in lines]
locations = [Point(v) for v in locations]

distances = {}
for p1 in locations:
    for p2 in locations:
        if p1 == p2: 
            continue 

        if (str(p1), str(p2)) not in distances and (str(p2), str(p1)) not in distances:
            distances[(str(p1), str(p2))] = p1 - p2 
point_pairs = list(distances.keys())
sorted_points = [point_pairs[idx] for idx in np.argsort([distances[key] for key in point_pairs])]

circuits = []
num_connections = 0
current_idx = 0
while True:
    point1, point2 = sorted_points[current_idx] 

    b_box = False
    for circuit_idx in range(len(circuits)):
        if any(p in circuits[circuit_idx] for p in [point1, point2]):
            if point1 in circuits[circuit_idx] and point2 in circuits[circuit_idx]:
                # Nothing happens because both junction boxes are already in the circuit
                b_box = True
                # num_connections += 1        
                break

            circuits[circuit_idx].add(point1)
            circuits[circuit_idx].add(point2)
            b_box = True
            # num_connections += 1
            break
    if not b_box:
        circuits.append({point1, point2})
        # num_connections += 1        
    current_idx += 1
    
    num_connections += 1       
    circuits = merge_circuits(circuits)

    if num_connections == stop_connections - 1:        
        # circuits = merge_circuits(circuits)
        top_3 = sorted([len(circuit) for circuit in circuits])[::-1][0:3]
        print(f'part 1: {top_3}: {top_3[0] * top_3[1] * top_3[2]}')

    if len(circuits) == 1 and len(circuits[0]) == len(locations):
        p1_x = int(point1.split(',')[0])
        p2_x = int(point2.split(',')[0])
        print(f'Part 2: {p1_x * p2_x}')
        break
