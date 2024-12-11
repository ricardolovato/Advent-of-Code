class Node:
    def __init__(self, id):
        self.id = id
        # self.num_blocks = int(num_blocks)
        # self.free_space = int(free_space)

        self.next = None
        self.prev = None

def display_disk(root_node):
    current_node = root_node
    while current_node.next is not root_node:
        print(f'{current_node.id}', end='')
        current_node = current_node.next

    print(f'{current_node.id}')

def is_compressed(root_node):
    current_node = root_node
    b_filled = True
    while current_node.next is not root_node:
        if current_node.id == '.' and current_node.next.id != '.':
            return False
        current_node = current_node.next
    return b_filled

def get_free_node(root_node):
    node = root_node
    while node.next is not root_node:
        if node.id == '.':
            return node
        node = node.next

    return None

def get_last_node(node):
    node = node.prev
    while node.id == '.':
        node = node.prev
    return node


def build_disk_map(disk_map, block_size, free_space_size, step_size):
    root_node = Node(-1)
    previous_node = root_node
    for idx in range(0, len(disk_map), step_size):
        num_blocks = int(disk_map[idx:idx + block_size])
        free_space = int(disk_map[idx + block_size:idx + block_size + free_space_size])
        # print(f'{num_blocks} blocks, {free_space} free space')

        for iP, positions in enumerate([num_blocks, free_space]):
            for position_num in range(positions):
                current_node = Node({0: idx // 2, 1: '.'}[iP])
                current_node.prev = previous_node
                previous_node.next = current_node
                previous_node = current_node

    # Remove placeholder root
    root_node = root_node.next

    # Link to the back
    root_node.prev = previous_node
    previous_node.next = root_node
    return root_node

def calc_checksum(root_node):
    checksum = 0
    current_node = root_node
    position_idx = 0
    while current_node.next is not root_node and current_node.id != '.':
        checksum += position_idx * current_node.id
        position_idx += 1
        current_node = current_node.next
    return checksum

disk_map = '12345'
disk_map = '2333133121414131402'
with open('2024_day09/input.txt') as f_in:
    disk_map = f_in.readlines()[0].strip()

block_size = 1
free_space_size = 1
step_size = block_size + free_space_size

disk_map += '0'

root_node = build_disk_map(disk_map, block_size, free_space_size, step_size)

# display_disk(root_node)
# print(is_compressed(root_node))

while not is_compressed(root_node):
    last_node = get_last_node(root_node)
    free_node = get_free_node(root_node)

    last_node_prev = last_node.prev
    last_node_next = last_node.next

    # Exchange free_node and last_node
    last_node.prev = free_node.prev
    last_node.prev.next = last_node
    last_node.next = free_node.next
    last_node.next.prev = last_node

    # Rearrange the last item
    free_node.prev = last_node_prev
    free_node.prev.next = free_node
    free_node.next = last_node_next
    free_node.next.prev = free_node

    # display_disk(root_node)
print(calc_checksum(root_node))