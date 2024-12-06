import numpy as np
import re
import operator

def evaluate_part(workflow, part):
    for sequence in workflow:
        if type(sequence) is not tuple:
            return sequence 
        
        category, comparison, criteria, destination = sequence
        if comparison(part[category], criteria):
            return destination

with open('input.txt') as f_in:
    lines = [line.strip() for line in f_in.readlines()]

comparisons = {'<':operator.lt, '>':operator.gt}

workflows = {}
for line in lines[0:lines.index('')]:
    workflow = line[0:line.index('{')]
    workflows[workflow] = []
    rules = line[line.index('{')+1:-1].split(',')
    for rule in rules:
        if ':' in rule:
            condition, destination = rule.split(':')            
            category, comparison, criteria = re.findall('(x|m|a|s)(<|>)(\-*\d+)', condition)[0]
            criteria = int(criteria)
            comparison = comparisons[comparison]
            workflows[workflow].append((category, comparison, criteria, destination))
        else:
            destination = rule
            workflows[workflow].append(destination)

parts = {}
for line in lines[lines.index('') + 1:]:
    part = {p.split('=')[0]:int(p.split('=')[1]) for p in line[1:-1].split(',')}

    current_workflow = 'in'
    while current_workflow not in ['R', 'A']:
        print(f'{current_workflow} -> ', end = '')
        current_workflow = evaluate_part(workflows[current_workflow], part)
    print(f'{current_workflow}')

    # Record accept/reject
    parts[tuple(part[category] for category in ['x', 'm', 'a', 's'])] = current_workflow

accepted_sum = sum([sum(ratings) for ratings, evaluation in parts.items() if evaluation == 'A'])
print(f'Part 1: {accepted_sum}')


# This doesn't work but probably could if fixed 
def iterate_workflows(current_workflow, current_criteria, ):
    # current_workflow = 'in'
    print(f'workflow: {current_workflow}')
    accepted_criterias = []
    # while current_workflow != 'A':
    print(f'current criteria: {current_criteria} ')

    if current_workflow == 'A':
        print('returning A')
        yield current_criteria
        return 
    elif current_workflow == 'R':
        print('returning R')
        return 
    workflow = workflows[current_workflow]
    
    for rule in workflow:
        print(f'rule: {rule}')
        if type(rule) == tuple:
            category, comparison, criteria, destination = rule

            if comparison == operator.lt:
                current_criteria[category] = (1, criteria - 1)
                # print('Entering 1a: ')
                # c = iterate_workflows(current_workflow=destination, 
                #                     current_criteria=current_criteria,
                #                     )
                # accepted_criterias.append(c)
            else:
                current_criteria[category] = (criteria, 4000)
            print('Entering 1b: ')
            c = iterate_workflows(current_workflow=destination, 
                                current_criteria=current_criteria,
                                )
            for _c in c:
                accepted_criterias.append(_c)
            if destination == 'A':
                return accepted_criterias
        else:
            # if rule == 'R':
            #     print('returning R bottom')
            #     return 0
            # elif rule == 'A':
            #     print('returning A bottom')
            #     # accepted_criterias.append(current_criteria)
            #     return current_criteria
            # else:
            # print('no rule')
            print('Entering 2: ')
            c = iterate_workflows(rule, current_criteria, )
            accepted_criterias.append(c)
    # print('returning bottom')
    return accepted_criterias
    # print(f'{current_workflow}')
                
# current_criteria = {'x':(1, 4000), 'm':(1, 4000), 'a':(1, 4000), 's':(1, 4000)}
# v = iterate_workflows(current_workflow='in', 
#                   current_criteria=current_criteria)



accepted_criterias = []
criterias = [({'x':(1, 4000), 'm':(1, 4000), 'a':(1, 4000), 's':(1, 4000)}, 'in', 0)]
while criterias:
    current_criteria, current_workflow, rule_index = criterias.pop()

    if current_workflow == 'A':
        accepted_criterias.append(current_criteria)
    elif current_workflow == 'R':
        continue
    else:
        workflow = workflows[current_workflow]
        rule = workflow[rule_index]

        criteria_met = dict(current_criteria)
        criteria_unmet = dict(current_criteria)

        if type(rule) == tuple:
            category, comparison, criteria, destination = rule

            if comparison == operator.lt:
                criteria_met[category] = (criteria_met[category][0], criteria - 1 )
                criteria_unmet[category] = (criteria, criteria_unmet[category][1])
            else:
                criteria_met[category] = (criteria + 1, criteria_met[category][1])
                criteria_unmet[category] = (criteria_unmet[category][0], criteria)

            # Go to destination for met condition
            criterias.append((criteria_met, destination, 0))
            # Go back to current workflow and proceed to next rule for unmet condition
            criterias.append((criteria_unmet, current_workflow, rule_index + 1))
        else:
            # print('unhandled')
            # print(f'rule: {rule}')
            criterias.append((current_criteria, rule, 0))

import math
criteria_sum = 0
for c in accepted_criterias:
    print(c)
    p = math.prod([(v[1]-v[0] + 1) for _, v in c.items()])
    print(p)
    criteria_sum += p

print(criteria_sum)
















