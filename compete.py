from connect_helper import *
import random
import numpy as np
from connect_helper import *
import copy
from play import *
from tqdm import tqdm
import matplotlib.pyplot as plt

DRAW = True
OVER = True
DEPTH = 3


def showHistogram(data):
    n_bins = 10
    plt.style.use('ggplot')
    plt.figure(figsize=(32,6))
    plt.suptitle("Node Count")
    for i in range(len(data.keys())):
        key = list(data.keys())[i]
        plt.subplot(1,5,i+1)
        plt.title("Size: "+str(key))
        plt.xlabel("Node Count")
        plt.ylabel("Frequency")
        plt.hist(data[key], bins = n_bins)
    plt.show()
    return

def showScore(data,type):
    plt.figure(figsize=(32,6))
    plt.suptitle("Winning Score")
    plt.style.use('ggplot')
    for i in range(len(data.keys())):
        key = list(data.keys())[i]
        if type == 1:
            stat = ['Base', 'Tree AI', 'Draw']
        else:
            stat = ['Base', 'Neural Net', 'Draw']
        plt.subplot(1,5,i+1)
        plt.title("Size: "+str(key))
        plt.bar(stat, data[key])
        plt.xlabel("AI")
        plt.ylabel("Win Frequency")
    plt.show()
    return

def compete1(state):
    player2_score = 0
    player = 1
    winner = 0
    game_stat = False
    while not game_stat:
        player, board = state
        old_player = player

        if player == 1:
            action = baseline_ai(board,verbose=False)
            state = perform_action(action,state)
        else:
            state, utility = better_ai(state, DEPTH, evaluate)
            player2_score = player2_score + utility

        if player_win(state,old_player):    
                game_stat = OVER
                winner = old_player
                #print("Player %d Wins" %(old_player))
            
        if draw_state(state):
            game_stat = DRAW
            #print("Game Draw")
    return winner,player2_score

def compete2(state,net):
    player2_score = 0
    player = 1
    winner = 0
    game_stat = False
    while not game_stat:
        player, board = state
        old_player = player

        if player == 1:
            action = baseline_ai(board,verbose=False)
            state = perform_action(action,state)

        else:
            state, utility = nn_ai(state, DEPTH, evaluate,net)
            player2_score = player2_score + evaluate(state)

        if player_win(state,old_player):    
                game_stat = OVER
                winner = old_player
                #print("Player %d Wins" %(old_player))
            
        if draw_state(state):
            game_stat = DRAW
            #print("Game Draw")
    return winner,player2_score

if __name__ == "__main__":
    player1_score = 0
    player2_score = 0
    draw_score = 0

    prompt1 = ("Select the opponents:\n "
             "\t 1 >> Baseline vs TreeBased AI\n"
             "\t 2 >> Baseline vs Neural Network\n")

    prompt2 = ("\nChoose Problem Instance, here board size is the problem instance (Rows x Columns):\n"
                "\t1 >> 5 x 5\n"
                "\t2 >> 6 x 6\n"
                "\t3 >> 7 x 7\n"
                "Option ---->" )
    
    opp_type = int(input(prompt1))
    problem_size = [(5,5),(5,6),(6,6),(6,7),(7,7)]
    problem_size2 = [(5,5),(6,6),(7,7)]
    result = {}
    scores = {}    
    if opp_type == 1:
        for size in problem_size:
            print("Size:",size)
            result[size] = []
            for i in tqdm(range(100)):
                ROW, COL = size
                state = initial_state(ROW, COL)
                winner,sc2 = compete1(state)
                if winner == 1:
                    player1_score = player1_score + 1
                elif winner == 2:
                    player2_score = player2_score + 1
                else:
                    draw_score = draw_score + 1
                result[size].append(getNodeCount())
            scores[size] = (player1_score,player2_score,draw_score)

    elif opp_type == 2:
        size_index = int(input(prompt2))
        ROW,COL = problem_size2[size_index-1] 
        size = problem_size2[size_index-1]
        print("Generating Data:")
        training_examples = generate_data(ROW,COL, num_examples = 500, max_depth=3)
        testing_examples = generate_data(ROW,COL, num_examples = 500, max_depth=3)
        print("Training and Testing data created")
        print("Training examples:%d" %len(training_examples[0]))
        print("Training examples:%d" %len(testing_examples[0]))
        ag_train  = augment(training_examples)
        ag_test = augment(testing_examples)
        print("\nAfter Augmentation")
        print("Training examples:%d" %len(ag_train))
        print("Training examples:%d" %len(ag_test))
        net = train_model(ag_train,ag_test)
        result[size] = []
        for i in tqdm(range(100)):
            state = initial_state(ROW, COL)
            winner,sc2 = compete2(state,net)
            if winner == 1:
                player1_score = player1_score + 1
            elif winner == 2:
                player2_score = player2_score + 1
            else:
                draw_score = draw_score + 1
            result[size].append(getNodeCount())
        scores[size] = (player1_score,player2_score,draw_score)       
    
    showHistogram(result)
    showScore(scores,opp_type)
