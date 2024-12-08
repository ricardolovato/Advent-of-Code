import numpy as np

class Round:
              # R  P  S
    scoring = [[3, 0, 6], # Rock
               [6, 3, 0], # Paper
               [0, 6, 3]] # Scissors
    
    shape_scores = {'ROCK':1, 'PAPER':2, 'SCISSORS':3}
    win_loss = {'X':6, 'Y':3, 'Z':0}

    def __init__(self, player1, player2):
        player1 = Action(player1)
        # player2 = Action(player2)

        player2_idx = self.win_loss[player2]
        player2_idx = self.scoring[player1.score_idx].index(player2_idx)
        player2 = Action({0:'A', 1:'B', 2:'C'}[player2_idx])

        print(f'{player1.player_action} : {player2.player_action}')

        self.scores = [self.shape_scores[p1.player_action] + self.scoring[p1.score_idx][p2.score_idx] for p1, p2 in zip([player1, player2], [player2, player1])]
        
        print(f'scores {self.scores}')

class Action:
    # Rock, paper, scissors
    score_indices = ['ROCK', 'PAPER', 'SCISSORS'] 
    
    def __init__(self, player_action):
        # self.score = self.scores[self.player_action]
        if player_action in ['X', 'A']:
            self.player_action = 'ROCK'
        elif player_action in ['Y', 'B']:
            self.player_action = 'PAPER'
        elif player_action in ['Z', 'C']:
            self.player_action = 'SCISSORS'

        self.score_idx = self.score_indices.index(self.player_action)


with open('input.txt') as f_in:
    lines = [line.strip() for line in f_in.readlines()]

score_sum = []
for round in lines:
    player1, player2 = round.split(' ')
    print(f'{player1}, {player2}')

    current_round = Round(player1, player2)
    score_sum.append(current_round.scores[1])
    # break

print(f'Scores: {np.sum(score_sum)}')







































