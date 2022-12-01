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

def showScore(data):
    plt.figure(figsize=(32,6))
    plt.suptitle("Winning Score")
    plt.style.use('ggplot')
    for i in range(len(data.keys())):
        key = list(data.keys())[i]
        stat = ['Base', 'Tree AI', 'Draw']
        plt.subplot(1,5,i+1)
        plt.title("Size: "+str(key))
        plt.bar(stat, data[key])
        plt.xlabel("AI")
        plt.ylabel("Win Frequency")
    plt.show()
    return

def compete(state):
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

        if player_win(state,old_player):    
                game_stat = OVER
                winner = old_player
                #print("Player %d Wins" %(old_player))
            
        if draw_state(state):
            game_stat = DRAW
            #print("Game Draw")
    return winner

if __name__ == "__main__":
    problem_size = [(5,5),(5,6),(6,6),(6,7),(7,7)]
    result = {}
    scores = {} 
    for size in problem_size:
        player1_score = 0
        player2_score = 0
        draw_score = 0
        print("Size:",size)
        result[size] = []
        for i in tqdm(range(100)):
            ROW, COL = size
            state = initial_state(ROW, COL)
            winner = compete(state)
            if winner == 1:
                player1_score = player1_score + 1
            elif winner == 2:
                player2_score = player2_score + 1
            else:
                draw_score = draw_score + 1
            result[size].append(getNodeCount())
        scores[size] = (player1_score,player2_score,draw_score)

    showHistogram(result)
    showScore(scores)
