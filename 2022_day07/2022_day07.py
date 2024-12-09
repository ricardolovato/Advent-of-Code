class Node:
    def __init__(self, name):
        self.name = name

        self.parent = None
        self.children = []
        self.contents = []


filename = '2022_day07/test_input.txt'
with open(filename) as f_in:
    lines = [line.strip() for line in f_in.readlines()]

for line in lines:
    print(line)