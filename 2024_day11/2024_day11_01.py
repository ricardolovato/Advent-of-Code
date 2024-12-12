class Node:
    def __init__(self, value):
        self.value = value

        # self.prev = None
        self.next = None


class Stones:
    def __init__(self, stones):
        self.head = Node(None)
        self.tail = Node(None)

        current_node = self.head
        for stone in stones:
            new_node = Node(stone)
            current_node.next = new_node
            new_node.prev = current_node
            current_node = new_node
        current_node.next = self.tail
        self.tail.prev = current_node
        self.unique_values = {}

    def insert_after(self, node, insert_node):
        insert_node.next = node.next
        node.next = insert_node
        insert_node.prev = node
        node.next.prev = insert_node

    def delete_node(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def replace_node(self, node: Node, new_nodes: list):
        end_node = node.next
        node = node.prev
        for new_node in new_nodes:
            node.next = new_node
            new_node.prev = node
            node = new_node

        node.next = end_node
        end_node.prev = node
        return end_node

    def display_stones(self):
        current_node = self.head.next
        while current_node.value is not None:
            print(current_node.value, end=' ')
            current_node = current_node.next
        print()

    def add_unique(self, value):
        if value not in self.unique_values:
            self.unique_values[value] = 1
        else:
            self.unique_values[value] += 1

    def blink(self):
        current_node = self.head.next
        while current_node.value is not None:
            if current_node.value == 0:
                current_node.value = 1
                self.add_unique(current_node.value)
                current_node = current_node.next
                continue

            value_str = f'{current_node.value}'
            if len(value_str) % 2 == 0:
                self.add_unique(current_node.value)
                new_nodes = [Node(int(value_str[0:len(value_str)//2])),
                             Node(int(value_str[len(value_str)//2::]))]
                current_node = self.replace_node(current_node, new_nodes)
                continue

            current_node.value *= 2024
            self.add_unique(current_node.value)
            current_node = current_node.next

    def num_stones(self):
        current_node = self.head.next
        count = 0
        while current_node.value is not None:
            count += 1
            current_node = current_node.next
        return count


stones = '0 1 10 99 999'
stones = '125 17'
# stones = '572556 22 0 528 4679021 1 10725 2790'

num_blinks = 25
num_blinks = list(range(num_blinks))

stones = [int(v) for v in stones.split(' ')]
stones = Stones(stones)
stones.display_stones()

num_stones = []
unique = []
for blink_num in num_blinks:
    print(f'Blink {blink_num + 1}')
    stones.blink()
    # stones.display_stones()
    num_stones.append(stones.num_stones())
    unique.append(len(stones.unique_values))
    print(f'\tNum stones: {num_stones[-1]}')
    print(f'\tUnique values: {unique[-1]}')

# import matplotlib.pyplot as plt
# import numpy as np
# plt.plot(num_blinks, num_stones, color='b')
# plt.plot(num_blinks, [x**2 for x in num_blinks], color='r')
# plt.yscale('log')
# plt.xscale('log')
# plt.show()
#
# plt.plot(np.diff(num_stones))
# plt.show()

