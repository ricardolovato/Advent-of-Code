from functools import cache

@cache
def blink(stone, blinks):
    # Base case
    if blinks == 0:
        return 1

    if stone == 0:
        return blink(1, blinks - 1)

    value_str = f'{stone}'
    if len(value_str) % 2 == 0:
        return blink(int(value_str[0:len(value_str)//2]), blinks - 1) + \
               blink(int(value_str[len(value_str)//2::]), blinks - 1)

    return blink(stone * 2024, blinks - 1)



stones = '125 17'
stones = '572556 22 0 528 4679021 1 10725 2790'
stones = [int(v) for v in stones.split(' ')]
num_stones = 0
for stone in stones:
    num_stones += blink(stone, 75)
print(num_stones)