import copy
#from main_game import *
from a_star import *

class Enemy:
    def __init__(self, x, y):
        self.enemyAlive = True
        #cell is relative to entire game map
        self.originX = x
        self.originY = y
        self.enemyCellX = x
        self.enemyCellY = y
        #position is relative to entire game map
        self.enemyPosX = None
        self.enemyPosY = None
        self.respawnTime = 10000

    def setCoords(self, x, y):
        self.enemyPosX = x
        self.enemyPosY = y
    
    def move(self, destX, destY, limit, x0, y0, x1, y1):
        d = ((self.enemyPosX - destX)**2 + (self.enemyPosY - destY)**2)**0.5
        if (d > limit):
            self.enemyPosX -= (self.enemyPosX-(x0+x1)/2)*0.2
            self.enemyPosY -= (self.enemyPosY-(y0+y1)/2)*0.2
        else:
            self.enemyPosX -= (self.enemyPosX-destX)*0.2
            self.enemyPosY -= (self.enemyPosY-destY)*0.2