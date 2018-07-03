from PIL import ImageGrab
from PIL import Image
import os
import time
import win32api, win32con
import numpy as np
import random
import itertools
import math
import constants
'''
Author: Devin B, dpb246

Provides an abstracted interface layer between solver and website: 0hh1.com
Returns a integer verion of board with:
    blue being 1
    red being 0
    empty being whatever it is set to in constants

Make sure to check that the pixel locations for the clicks are in the correct spots
'''
class Binary:
    '''
    8x8:
    #Location of each row on the website, in order top to bottom
    rows = [253, 330, 409, 494, 561, 642, 728, 809]
    #Location of each column on the website, in order left to right
    columns = [658, 747, 815, 894, 977, 1060, 1141, 1211]
    6x6:
    #Location of each row on the website, in order top to bottom
    rows = [263,370,475,570,676,800]
    #Location of each column on the website, in order left to right
    columns = [667,778,874,977,1101,1202]
    '''
    def __init__(self):
        #Location of each row on the website, in order top to bottom
        rows = [253, 330, 409, 494, 561, 642, 728, 809]
        #Location of each column on the website, in order left to right
        columns = [658, 747, 815, 894, 977, 1060, 1141, 1211]
        #Generate grid of each location to make it easier to access
        self.pos = list()
        for r in rows:
            temp = list()
            for c in columns:
                temp.append((c, r))
            self.pos.append(temp)
        #size of the board
        self.size = len(self.pos)
        #The colours the website uses for the tiles
        self.blue = np.array([53, 184, 213])
        self.red = np.array([213, 83, 54])
        self.blue2 = np.array([48, 167, 194])
        self.red2 = np.array([194, 75, 49])
        self.grey = np.array([42, 42, 42])
        #Dictionary to decode the colours, convert to string in order to hash list
        self.decodeColour = {
                np.array_str(self.blue): 1,
                np.array_str(self.red): 0,
                np.array_str(self.grey): constants.empty,
                np.array_str(self.blue2): 1,
                np.array_str(self.red2): 0
            }
    #Clicks screen at given point: (x,y) tuple
    def click(self, pos):
        win32api.SetCursorPos(pos)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    #Goes through 2d array and clicks to set each spot to 0/1 (red/blue)
    def output_board(self, board):
        for i in range(self.size):
            for j in range(self.size):
                #Add one since red is stored as 0 but needs one click etc.
                click_count = board[i][j]+1
                for k in range(click_count):
                    self.click(self.pos[i][j])
                    #Need to wait just a bit for website to update
                    time.sleep(0.001)
    #Function that clicks through board and then waits to check if game over
    def try_finish(self, board):
        self.output_board(board)
        time.sleep(1.5) #allow screen/website to update
        return self.is_finished()
    #Return int version of current board from screen
    def get_board(self):
        board = [[None for j in range(self.size)] for i in range(self.size)]
        im = np.array(ImageGrab.grab()) #gets screen shot
        for i in range(self.size):
            for j in range(self.size):
                tempPos = self.pos[i][j]
                #for each location, flip x,y; find pixel rgb values; convert to string; get value from dictionary
                board[i][j] = self.decodeColour[np.array_str(im[tempPos[1]][tempPos[0]])]
        return np.array(board)
    #Don't ask
    def is_finished(self):
        return self.checkForWin()
    #Functions that checks to see if puzzle has been solved
    def checkForWin(self):
        i = np.array(ImageGrab.grab())
        return not all(i[982][798] == np.array([255,255,255]))
    #Starts a new Game clicking through menus
    def new_episode(self):
        self.click((742, 979))
        time.sleep(0.1)
        '''
        8x8:
        (1052, 448)
        6x6:
        (923,448)
        '''
        self.click((1052, 448))
        time.sleep(1)
