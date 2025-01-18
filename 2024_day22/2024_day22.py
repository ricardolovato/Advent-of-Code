from functools import cache

@cache
def mix(n1, n2):
    return n1 ^ n2

@cache
def prune(n):
    return n % 16777216

@cache
def generate_secret(secret_num):
    # Calculate the result of multiplying the secret number by 64. Then, mix this result
    # into the secret number. Finally, prune the secret number.
    secret_num = prune(mix(secret_num, secret_num * 64))

    secret_num = prune(mix(secret_num, (secret_num // 32)))

    secret_num = prune(mix(secret_num, (secret_num * 2048)))

    return secret_num


# secret_nums = [1, 10, 100, 2024]
# with open('2024_day22/input.txt') as f_in:
#     lines = f_in.readlines()
# secret_nums = [int(line.strip()) for line in lines]

secret_nums = [1, 2, 3, 2024]

secret_sum = 0
for secret_num in secret_nums:
    # print(f'{secret_num}: ', end='')
    for i in range(2000):
        secret_num = generate_secret(secret_num)
    secret_sum += secret_num
    # print(f'{secret_num}')

print(f'sum: {secret_sum}')


import numpy as np
secret_num = 1
prices = [1 % 10]
for i in range(2000):
    secret_num = generate_secret(secret_num)
    prices.append(secret_num % 10)

num_diff = np.diff(prices)

for idx in range(len(num_diff)):
    if prices[idx] == 7:
        print(num_diff[idx - 4:idx + 1])

for idx in range(4, len(num_diff)):
    if all(n1 == n2 for n1, n2 in zip(num_diff[idx-4:idx], np.array([-2, 1, -1, 3]))):
        print(idx)