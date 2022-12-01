from connect_helper import *
import random
import numpy as np
from connect_helper import *
import copy

DRAW = True
OVER = True
DEPTH = 4
PLAYER = 1
AI = 2
ROW = 0
COL = 0
NODE_COUNT = 0

def user_action(player,board):   
    valid_moves = valid_action(board)
    prompt = "Player %d, choose an action: " % (player)
    print("Valid Actions:")
    print(valid_moves)
    while True:
        action = int(input(prompt))
        if action in valid_moves:
            return action
        else:
            print("Action invalid, please try again")

def baseline_ai(board,verbose):
    valid_moves = valid_action(board)
    action = random.choice(valid_moves)
    if verbose:
        print("Baseline AI chooses action : %d" %action)
    return action

def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER
	if piece == PLAYER:
		opp_piece = AI

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(0) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(0) == 2:
		score += 2
	if window.count(opp_piece) == 3 and window.count(0) == 1:
		score -= 4
	return score

def evaluate(state):
    global ROW
    global COL
    player,new_board = state
    score = 0
    center_array = [int(i) for i in list(new_board[:, COL//2])]
    center_count = center_array.count(player_win)
    score += center_count * 3

    for r in range(ROW):
        row_array = [int(i) for i in list(new_board[r,:])]
        for c in range(COL-3):
            window = row_array[c:c+4]
            score = score + evaluate_window(window, player)    

    for c in range(COL):
        col_array = [int(i) for i in list(new_board[:,c])]
        for r in range(ROW-3):
            window = col_array[r:r+4]
            score += evaluate_window(window, player)

    for r in range(ROW-3):
        for c in range(COL-3):
            window = [new_board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, player)

    for r in range(ROW-3):
        for c in range(COL-3):
            window = [new_board[r+3-i][c+i] for i in range(4)]
            score += evaluate_window(window, player)

    return score
       
def better_ai(state, max_depth, evaluate):
    global NODE_COUNT
    NODE_COUNT = NODE_COUNT + 1
    if draw_state(state): 
        return (None, 5)
    elif player_win(state,state[0]):
        return (None, 1000)
    if max_depth == 0: 
        return (None, evaluate(state))
    
    children = [perform_action(action,state) for action in valid_action(state[1])]
    results = [better_ai(child, max_depth-1, evaluate) for child in children]

    _, utilities = zip(*results)

    player, board = state
    if player == 2: action = np.argmax(utilities)
    if player == 1: action = np.argmin(utilities)
    return children[action], utilities[action]

def getNodeCount():
    global NODE_COUNT
    temp = copy.deepcopy(NODE_COUNT)
    NODE_COUNT = 0
    return temp 

if __name__ == "__main__":
    prompt1 = ("\nChoose Problem Instance, here board size is the problem instance (Rows x Columns):\n"
                "\t1 >> 5 x 5\n"
                "\t2 >> 5 x 6\n"
                "\t3 >> 6 x 6\n"
                "\t4 >> 6 x 7 - Original Size\n"
                "\t5 >> 7 x 7\n"
                "Option ---->" )
    board_size = int(input(prompt1))

    player1_score = 0
    player2_score = 0

    problem_size = [(5,5),(5,6),(6,6),(6,7),(7,7)]

    ROW,COL = problem_size[board_size-1]

    prompt2 = ("\nChoose any option for selecting the opponent:\n" 
                "\t1 >> Human Opponent\n"
                "\t2 >> Baseline AI Opponent\n" 
                "\t3 >> Tree Search AI\n"
                "Option ---->" )

    opponent = int(input(prompt2))
    state = initial_state(ROW, COL)
    player = 1
    game_stat = False

    # Implementation of the tweak in the rule
    player, board = state
    action = baseline_ai(board,False)
    state = perform_action(action,state)

    player, board = state
    action = baseline_ai(board,False)
    state = perform_action(action,state)
    print("Game Begins, with 1 piece of each player dropped at random place :")
    display_board(state)

    while not game_stat: 
        player, board = state
        old_player = player
        if player == 1:
            print("Player 1 >>")
            action = user_action(player,board)
            state = perform_action(action,state)
            player1_score = player1_score + evaluate(state)
        else:
            print("Player 2 >>")
            if opponent == 1:
                action = user_action(player,board)
                state = perform_action(action,state)
            elif opponent == 2:
                action = baseline_ai(board,True)
                state = perform_action(action,state)
            elif opponent == 3:
                state, utility = better_ai(state, DEPTH, evaluate)
                print(utility)
            player2_score = player2_score + evaluate(state)
        
        display_board(state)
        
        if player_win(state,old_player):    
            game_stat = OVER
            print("Player %d Wins" %(old_player))
        
        if draw_state(state):
            game_stat = DRAW
            print("Game Draw")

    print("Node Count : %d" %NODE_COUNT)
    print("Player 1 Score : %d" %player1_score)
    print("Player 2 Score : %d" %player2_score)