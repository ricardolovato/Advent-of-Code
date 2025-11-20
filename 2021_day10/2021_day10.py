filename = '2021_day10/test_input.txt'
filename = '2021_day10/input.txt'
with open(filename) as f_in:
    lines = f_in.readlines()

p1_points = {')':3,
          ']':57,
          '}':1197,
          '>':25137}
p2_points = {'(':1,
          '[':2,
          '{':3,
          '<':4}


p1_score = 0
p2_scores = []
for line in lines:
    stack = []
    b_stop = False
    for char in line.strip():
        if char in ['[', '(', '{', '<']:
            stack.append(char)
        else:
            c = stack.pop()
            if c == '[' and char == ']':
                continue 
            elif c == '{' and char == '}':
                continue
            elif c == '(' and char == ')':
                continue
            elif c == '<' and char == '>':
                continue
            else:
                # print(f'{line.strip()}: {c} // {char}')
                p1_score += p1_points[char]
                b_stop = True
                break
    if b_stop:
        continue

    if len(stack) == 0:
        continue
    
    p2_score = 0
    while stack != []:
        c = stack.pop()
        p2_score *= 5
        p2_score += p2_points[c]
    # print(f'{line.strip()}: {p2_score}')
    p2_scores.append(p2_score)
print(p1_score)

p2_scores = sorted(p2_scores)
print(f'{p2_scores[int(len(p2_scores)/2)]}')
