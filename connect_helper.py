import sys
import numpy as np
import math
import copy

ROWS = 0
COLS = 0

def initial_state(row,col):
    global ROWS
    global COLS
    ROWS = row
    COLS = col
    player = 1
    board = np.zeros((ROWS,COLS))
    return (player,board.astype(int))

def play_turn(col,board,piece):
    n_board = copy.deepcopy(board)
    row = valid_row(n_board,col)
    n_board[row][col] = piece
    n_player = 1 if piece == 2 else 2
    return (n_player,n_board)

def perform_action(action,state):
    player,board = state
    new_player, new_board = play_turn(action, board, player)
    return (new_player,new_board)

def valid_row(board,col):
    global ROWS
    global COLS
    for i in range(ROWS):
        if board[i][col] == 0:
            return i

def valid_action(board):
    global ROWS
    global COLS
    v_actions = []
    for i in range(COLS):
        for j in range(ROWS):
            if board[j][i] == 0:
                v_actions.append(i)
                break
    return v_actions

def display_board(state):
    print("\n")
    a = np.flip(state[1],0)
    for i in range(len(a[0])+2):
        print("__\t",end="")
    print("\n")
    for row in a:
        print("|\t",end="")
        for col in row:
            print("%d\t" %col,end ="")
        print("|\n")
    for i in range(len(a[0])+2):
        print("__\t",end="")
    print("\n")

def draw_state(state):
    return np.all(state[1])

def player_win(state,player):
    global ROWS
    global COLS
    player = player
    board = state[1]
    for c in range(COLS - 3):
        for r in range(ROWS):
            horizontal = np.array([])
            horizontal = np.append(horizontal,board[r][c])
            horizontal = np.append(horizontal,board[r][c+1])
            horizontal = np.append(horizontal,board[r][c+2])
            horizontal = np.append(horizontal,board[r][c+3])
            if np.all(horizontal == player):
                #print("Horizontal Win")
                return True

    for c in range(COLS):
        for r in range(ROWS-3):
            vertical = np.array([])
            vertical = np.append(vertical,board[r][c])
            vertical = np.append(vertical,board[r+1][c])
            vertical = np.append(vertical,board[r+2][c])
            vertical = np.append(vertical,board[r+3][c])
            if np.all(vertical == player):
                #print("Vertical Win")
                return True

    for c in range(COLS - 3):
        for r in range(ROWS-3):
            slope1 = np.array([])
            slope1 = np.append(slope1,board[r][c])
            slope1 = np.append(slope1,board[r+1][c+1])
            slope1 = np.append(slope1,board[r+2][c+2])
            slope1 = np.append(slope1,board[r+3][c+3])
            if np.all(slope1 == player):
                #print("Slope1 Win")
                return True

    for c in range(COLS - 3):
        for r in range(3, ROWS):
            slope2 = np.array([])
            slope2 = np.append(slope2,board[r][c])
            slope2 = np.append(slope2,board[r-1][c+1])
            slope2 = np.append(slope2,board[r-2][c+2])
            slope2 = np.append(slope2,board[r-3][c+3])
            if np.all(slope2 == player):
                #print("Slope2 Win")
                return True
