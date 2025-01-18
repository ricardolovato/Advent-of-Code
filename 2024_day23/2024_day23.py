class Computer:
    def __init__(self, name):
        self.name = name
        self.connections = []

    def __eq__(self, other):
        if isinstance(other, Computer):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f'Computer(name={self.name})'

    def get_num_connections(self):
        return len(self.connections)

    def show_connections(self):
        print(self.name)
        for connection in self.connections:
            print(f'\t{connection}')


filename = '2024_day23/test_input1.txt'
with open(filename) as f_in:
    connections = [line.strip().split('-') for line in f_in.readlines()]
unique_computers = list(set([c for connection in connections for c in connection]))

computers = {}
for name in unique_computers:
    computers[name] = Computer(name)

for computer1, computer2 in connections:
    computers[computer1].connections.append(computers[computer2])
    computers[computer2].connections.append(computers[computer1])