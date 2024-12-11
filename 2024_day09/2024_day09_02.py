class Node:
    def __init__(self, id, num_blocks, free_space):
        self.id = id
        self.num_blocks = int(num_blocks)
        self.free_space = int(free_space)

        self.next = None
        self.prev = None

def display_disk(root_node):
    current_node = root_node
    while current_node.next is not root_node:
        id_str = ''.join([str(current_node.id)] * current_node.num_blocks)
        free_str = ''.join(['.'] * current_node.free_space)
        print(f'{id_str}{free_str}', end='')
        current_node = current_node.next

    id_str = ''.join([str(current_node.id)] * current_node.num_blocks)
    free_str = ''.join(['.'] * current_node.free_space)
    print(f'{id_str}{free_str}')

def is_compressed(root_node):
    current_node = root_node
    b_filled = True
    while current_node.next is not root_node:
        if current_node.free_space != 0:
            return False
        current_node = current_node.next
    return b_filled

def get_free_node(root_node, num_free_space):
    node = root_node
    while node.next is not root_node:
        if node.free_space >= num_free_space:
            return node
        node = node.next

    return None

def get_last_node(node):
    node = node.prev
    while node.id == '.':
        node = node.prev
    return node


def build_disk(disk_map, block_size, free_space_size, step_size):
    root_node = Node(-1, 0, 0)
    # root_node = Node(0, disk_map[0:block_size], disk_map[block_size:block_size + free_space_size])
    previous_node = root_node
    for idx in range(0, len(disk_map), step_size):
        num_blocks = disk_map[idx:idx + block_size]
        free_space = disk_map[idx + block_size:idx + block_size + free_space_size]

        print(f'{num_blocks} blocks, {free_space} free space')
        # print(disk_map[idx:idx + block_size], disk_map[idx + block_size:idx + block_size + free_space_size])
        block_node = Node(id=idx // 2,
                          num_blocks=num_blocks,
                          free_space=0)
        block_node.prev = previous_node
        previous_node.next = block_node

        free_node = Node(id='.',
                          num_blocks=0,
                          free_space=free_space)
        free_node.prev = block_node
        block_node.next = free_node

        previous_node = free_node

    # Remove placeholder root
    root_node = root_node.next

    # Link to the back
    root_node.prev = previous_node
    previous_node.next = root_node
    return root_node

disk_map = '12345'
disk_map = '2333133121414131402'

block_size = 1
free_space_size = 1
step_size = block_size + free_space_size

disk_map += '0'

root_node = build_disk(disk_map, block_size, free_space_size, step_size)
display_disk(root_node)

end_node = root_node
while not is_compressed(root_node):
    last_node = get_last_node(end_node)
    free_node = get_free_node(root_node, last_node.num_blocks)
    if free_node is None:
        continue

    free_node.free_space -= last_node.num_blocks

    end_node = last_node.prev
    last_node.prev.next = last_node.next
    last_node_prev = last_node.prev
    last_node.next.prev = last_node_prev

    free_node.prev.next = last_node
    free_node.prev = last_node
    last_node.next = free_node

    display_disk(root_node)