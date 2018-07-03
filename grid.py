import location as p
import numpy as np
from copy import deepcopy
"""
Author: Devin B, dpb246

2d array but this provides safe checking and fancy printing
Also tracks the count of the pieces in each column/row as it updates so it doesn't have to be calculated each time
"""
class grid:
    def __init__(self, default, board_size=8):
        self.board_size = board_size
        self.default = default
        self.grid = np.array([[default for i in range(self.board_size)] for j in range(self.board_size)])
        #Hard coded for binary sudoko because not sure how else to do this right now allows instant piece counts in each row/column
        self.row_count = [{self.default:self.board_size, 0:0, 1:0} for i in range(self.board_size)]
        self.column_count = [{self.default:self.board_size, 0:0, 1:0} for i in range(self.board_size)]
    def reset(self, default):
        self.grid = np.array([[default for i in range(self.board_size)] for j in range(self.board_size)])
    def get(self, location):
        if not location.valid():
            return None
        return self.grid[location.row()][location.column()]
    def getRow(self, index):
        return self.grid[index]
    def getGrid(self):
        return self.grid
    def getSize(self):
        return self.board_size
    def __len__(self):
        return self.board_size
    def set(self, location, value):
        if not location.valid():
            return False
        self.grid[location.row()][location.column()] = value
        return True
    #Doesn't allow change if the value isn't the default returns True if succesful in setting
    def safe_set(self, location, value):
        if not location.valid():
            return False
        if self.grid[location.row()][location.column()] != self.default:
            return False
        self.grid[location.row()][location.column()] = value
        self.row_count[location.row()][value] += 1
        self.row_count[location.row()][self.default] -= 1
        self.column_count[location.column()][value] += 1
        self.column_count[location.column()][self.default] -= 1
        return True
    def __iter__(self):
        for row in self.grid:
            yield row
    #Sets the grid from a 2d array of the exact same size
    def massSet(self, values):
        for r in range(self.board_size):
            for c in range(self.board_size):
                self.grid[r][c] = values[r][c]
                self.row_count[r][values[r][c]] += 1
                self.row_count[r][self.default] -= 1
                self.column_count[c][values[r][c]] += 1
                self.column_count[c][self.default] -= 1
    def __repr__(self):
        return str(self.grid)
