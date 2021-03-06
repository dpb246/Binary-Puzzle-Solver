from copy import deepcopy
import numpy as np
from Game import *
import grid
import location as p
import constants
'''
Author: Devin B, dpb246

Uses a rule based approach to solve without needing to use guesses or recursion
This is the more readable version although the exact same logic structure
'''
opposite = { #Used to get the opposite of the current piece
    0: 1,
    1: 0
}
def Main(in_board):
    board = grid.grid(constants.empty, len(in_board))
    board.massSet(in_board)#Need to set the grid object to the starting board
    keep_going = True
    while keep_going:#Loop functions until it doesn't change anything in the grid
        keep_going = solve_rules(board)
        keep_going = keep_going or fill_master(board)
        keep_going = keep_going or logic(board)
    return board.getGrid()
#Finds and solves all the 00_ or 11_
def pairs(board, pos, current, opposite_current, change):
    if current == board.get(pos+(0,1)):
        change = change or board.safe_set(pos+(0,-1), opposite_current) or board.safe_set(pos+(0, 2), opposite_current)
    if current == board.get(pos+(1,0)):
        change = change or board.safe_set(pos+(-1,0), opposite_current) or board.safe_set(pos+(2,0), opposite_current)
    return change
#Find and solves all the 0_0 or 1_1
def triplets(board, pos, current, opposite_current, change):
    if current == board.get(pos+(0,2)):
        change = change or board.safe_set(pos+(0,1), opposite_current)
    if current == board.get(pos+(2,0)):
        change = change or board.safe_set(pos+(1,0), opposite_current)
    return change
#Calls pairs and triplets functions
def solve_rules(board):
    change = False
    for i in range(len(board)):
        for j in range(len(board)):
            pos = p.location(i, j)
            current = board.get(pos)
            if current != constants.empty: #Only need to check if the square isn't empty
                opposite_current = opposite[current]
                change = change or pairs(board, pos, current, opposite_current, change)
                change = change or triplets(board, pos, current, opposite_current, change)
    return change
#Fills the row with the given piece
def fill_row(board, i, to_fill_with):
    for j in range(len(board)):
        board.safe_set(p.location(i, j), to_fill_with)
#Fills the column with the given piece
def fill_column(board, i, to_fill_with):
    for j in range(len(board)):
        board.safe_set(p.location(j, i), to_fill_with)
#Calls all the fill functions
def fill_master(board):
    size = len(board)
    change = False
    for i in range(size):
        if (board.row_count[i][0] == size/2) and (board.row_count[i][1] != size/2):#Need more blue in row i
            change = True
            fill_row(board, i, 1)
        elif (board.row_count[i][0] != size/2) and (board.row_count[i][1] == size/2):#Need more red in row i
            change = True
            fill_row(board, i, 0)
        if (board.column_count[i][0] == size/2) and (board.column_count[i][1] != size/2):#Need more blue in row i
            change = True
            fill_column(board, i, 1)
        elif (board.column_count[i][0] != size/2) and (board.column_count[i][1] == size/2):#Need more red in row i
            change = True
            fill_column(board, i, 0)
    return change
#Returns the piece with the lowest count in the dictionary for that row/column
def least(dict):
    if dict[0] > dict[1]:
        return 1
    elif dict[1] > dict[0]:
        return 0
    else:
        return None
#Does the more advanced rules based logic
def logic(board):
    #If 3 empty in row, and edged by piece with less count, put that peice type on opposite side of empties
    change = False
    for i in range(len(board)):
        if (board.row_count[i][constants.empty] == 3):
            in_row = 0
            for j in range(len(board)):
                pos = p.location(i, j)
                if board.get(pos) == constants.empty:
                    last_pos = pos #Stores the position of the last empty element in row
                    in_row += 1
                else:
                    in_row = 0
                if in_row == 3:
                    piece_looking_for = least(board.row_count[i])
                    if board.get(last_pos+(0,1)) == piece_looking_for:
                        board.safe_set(last_pos+(0,-2), piece_looking_for)
                        change = True
                    if board.get(last_pos+(0,-3)) == piece_looking_for:
                        board.safe_set(last_pos, piece_looking_for)
                        change = True
                    break
        if (board.column_count[i][constants.empty] == 3):
            in_row = 0
            for j in range(len(board)):
                pos = p.location(j, i)
                if board.get(pos) == constants.empty:
                    last_pos = pos #Stores the position of the last empty element in column
                    in_row += 1
                else:
                    in_row = 0
                if in_row == 3:
                    piece_looking_for = least(board.column_count[i])
                    if board.get(last_pos+(1,0)) == piece_looking_for:
                        board.safe_set(last_pos+(-2,0), piece_looking_for)
                        change = True
                    if board.get(last_pos+(-3,0)) == piece_looking_for:
                        board.safe_set(last_pos, piece_looking_for)
                        change = True
                    break
        #Compares rows/columns to see if it can solve on by ensuring no 2 are identical
        if (board.row_count[i][constants.empty] == 2):
            for j in range(len(board)):
                if j==i: continue
                if board.row_count[j][constants.empty] != 0: continue
                empties = list()
                for k in range(len(board)):
                    pos1 = p.location(i, k)
                    pos2 = p.location(j, k)
                    if board.get(pos1) == constants.empty:
                        empties.append([pos1, pos2])
                        continue
                    if board.get(pos1) != board.get(pos2):
                        break
                else:#Success
                    for pos in empties:
                        change = change or board.safe_set(pos[0], opposite[board.get(pos[1])])
        if (board.column_count[i][constants.empty] == 2):
            for j in range(len(board)):
                if j==i: continue
                if board.column_count[j][constants.empty] != 0: continue
                empties = list()
                for k in range(len(board)):
                    pos1 = p.location(k, i)
                    pos2 = p.location(k, j)
                    if board.get(pos1) == constants.empty:
                        empties.append([pos1, pos2])
                        continue
                    if board.get(pos1) != board.get(pos2):
                        break
                else:#Success
                    for pos in empties:
                        change = change or board.safe_set(pos[0], opposite[board.get(pos[1])])
    return change
