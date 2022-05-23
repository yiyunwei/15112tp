import copy

class Treasure:
    def __init__(self, x, y):
        self.treasureUp = True
        #cell is relative to entire game map
        self.treasCellX = x
        self.treasCellY = y
        #position is relative to entire game map
        self.treasPosX = None
        self.treasPosY = None