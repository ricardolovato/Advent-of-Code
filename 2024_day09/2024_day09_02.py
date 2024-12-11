import time

class Node:
    def __init__(self, id, num_blocks, free_space):
        self.id = id
        self.num_blocks = int(num_blocks)
        self.free_space = int(free_space)

        self.next = None
        self.prev = None
        self.checked = False

def display_disk(root_node, mark_node=None):

    current_node = root_node
    count = 0
    while current_node.next is not root_node:
        # if count > 100:
        #     print('loop in forward direction')
        #     break
        count += 1
        id_str = ''.join([str(current_node.id)] * current_node.num_blocks)
        free_str = ''.join(['.'] * current_node.free_space)
        print(f'{id_str}{free_str}', end='')
        current_node = current_node.next

    id_str = ''.join([str(current_node.id)] * current_node.num_blocks)
    free_str = ''.join(['.'] * current_node.free_space)
    print(f'{id_str}{free_str}')

    if mark_node is not None:
        current_node = root_node
        count = 0
        while current_node is not mark_node:
            if count > 100:
                print('loop in marker')
                break
            count += 1
            id_str = ''.join([' '] * current_node.num_blocks)
            free_str = ''.join([' '] * current_node.free_space)
            print(f'{id_str}{free_str}', end='')
            current_node = current_node.next

        id_str = ''.join([str('^')] * current_node.num_blocks)
        free_str = ''.join(['^'] * current_node.free_space)
        print(f'{id_str}{free_str}')

    # current_node = root_node.prev
    # count = 0
    # while current_node is not root_node:
    #     if count > 100:
    #         print('loop in backward direction')
    #         break
    #     count += 1
    #     id_str = ''.join([str(current_node.id)] * current_node.num_blocks)
    #     free_str = ''.join(['.'] * current_node.free_space)
    #     print(f'{id_str}{free_str}', end='')
    #     current_node = current_node.prev
    #
    # id_str = ''.join([str(current_node.id)] * current_node.num_blocks)
    # free_str = ''.join(['.'] * current_node.free_space)
    # print(f'{id_str}{free_str}')


def is_compressed(root_node):
    current_node = root_node
    b_filled = True
    while current_node.next is not root_node:
        if current_node.free_space != 0:
            return False
        current_node = current_node.next
    return b_filled

def get_free_node(root_node, end_node, num_free_space):
    node = root_node
    while node.next is not end_node:
        if node.free_space >= num_free_space:
            return node
        node = node.next

    return None

def get_last_node(node):
    node = node.prev
    while node.id == '.' and not node.checked:
        node = node.prev
    return node


def build_disk(disk_map, block_size, free_space_size, step_size):
    root_node = Node(-1, 0, 0)
    # root_node = Node(0, disk_map[0:block_size], disk_map[block_size:block_size + free_space_size])
    previous_node = root_node
    for idx in range(0, len(disk_map), step_size):
        num_blocks = disk_map[idx:idx + block_size]
        free_space = disk_map[idx + block_size:idx + block_size + free_space_size]

        # print(f'{num_blocks} blocks, {free_space} free space')
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


start_time = time.time()
with open('2024_day09/input.txt') as f_in:
    disk_map = f_in.readlines()[0].strip()

block_size = 1
free_space_size = 1
step_size = block_size + free_space_size

disk_map += '0'

root_node = build_disk(disk_map, block_size, free_space_size, step_size)
# display_disk(root_node)

def get_node_num(node):
    position_idx = 0
    current_node = root_node
    while current_node is not node:
        position_idx += 1
        current_node = current_node.next
    return position_idx

end_node = root_node
while not is_compressed(root_node):
    last_node = get_last_node(end_node)

    node_idx = get_node_num(last_node)
    # print(node_idx)

    free_node = get_free_node(root_node, end_node, last_node.num_blocks)
    if free_node is None:
        # continue
        # print(f'cant move {last_node.id}')
        last_node.checked = True
        end_node = last_node
        # display_disk(root_node, end_node)

        if end_node == root_node:
            break
        continue
    # display_disk(root_node, free_node)

    free_node.free_space -= last_node.num_blocks

    # Move free space blocks to the end
    end_node = last_node.prev
    prev_node = end_node
    for i in range(last_node.num_blocks):
        new_free_node = Node(id='.',
                          num_blocks=0,
                          free_space=1)
        new_free_node.prev = prev_node
        prev_node.next = new_free_node
        prev_node = new_free_node
    prev_node.next = last_node.next
    last_node.next.prev = prev_node
    end_node = prev_node
    # display_disk(root_node)

    # Insert the last node where the free space was (before the free_node)
    free_node_prev = free_node.prev
    free_node.prev = last_node
    last_node.next = free_node

    free_node_prev.next = last_node
    last_node.prev = free_node_prev

    # display_disk(root_node)
display_disk(root_node)

# def calc_checksum(root_node):
checksum = 0
current_node = root_node
position_idx = 0
while current_node.next is not root_node:
    if current_node.id == '.':
        for i in range(current_node.free_space):
            position_idx += 1
    else:
        for i in range(current_node.num_blocks):
            checksum += position_idx * current_node.id
            position_idx += 1
    current_node = current_node.next
print(checksum)
# return checksum

# 6421724836639 too high
# 6421724645083

end_time = time.time()  # Record end time

elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")