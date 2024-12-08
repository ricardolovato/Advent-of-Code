# filename = '2024_day05/test_input1.txt'
filename = '2024_day05/input.txt'

with open(filename) as f_in:
    lines = f_in.readlines()

rules = []
all_pages = []
for idx in range(lines.index('\n')):
    rules.append([int(v) for v in lines[idx].strip().split('|')])
rules = {r_b:[rule[1] for rule in rules if r_b == rule[0]] for r_b in set([r[0] for r in rules])}

for idx in range(lines.index('\n')+1, len(lines)):
    all_pages.append([int(v) for v in lines[idx].strip().split(',')])

incorrect_indices = []
correct_pages = []
count = 0
for pages_idx in range(len(all_pages)):
    pages = all_pages[pages_idx]
    print(pages)
    b_pass = True
    # for iPage in range(len(pages)):#, page in enumerate(pages):
    iPage = 0
    while iPage < len(pages):
        page = pages[iPage]
        # print(f'\t{page}')
        b_restart = False
        if page in rules:
            for bad_page in rules[page]:
                # if any(bad_page == p for p in pages[0:iPage]):
                for current_page_idx in range(0,iPage):
                    if bad_page == pages[current_page_idx]:
                        print(f'\t{bad_page} found before {page}')
                        b_pass = False
                        if pages_idx not in incorrect_indices:
                            incorrect_indices.append(pages_idx)

                        # Swap and reset
                        pages[current_page_idx], pages[iPage] = pages[iPage], pages[current_page_idx]
                        print(f'\tAfter swap: {pages}')
                        iPage = current_page_idx - 1
                        print(f'\tResetting index to {iPage}')
                        b_restart = True
                        break
                if b_restart:
                    break
        iPage += 1
    if b_pass:
        middle_element = pages[len(pages) // 2]
        correct_pages.append(middle_element)
        print(f'\tCorrectly ordered: {middle_element}')
        count += 1

print(count)
print(sum(correct_pages))

part2_sum = sum([all_pages[idx][len(all_pages[idx])//2] for idx in incorrect_indices])
print(f'part 2: {part2_sum}')