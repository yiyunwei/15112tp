import copy

class Player:
    def __init__(self, x, y, radius):
        self.playerR = radius
        self.playerX = x
        self.playerY = y
        self.moving = False
        self.shooting = False
        self.destinationX = None
        self.destinationY = None
        self.eOnCooldown = False
        self.eCooldown = 5000
    
    def setDestination(self, x, y):
        self.moving = True
        self.destinationX = x
        self.destinationY = y
    
    def blink(self, x, y):
        d = ((self.playerX - x)**2 + (self.playerY - y)**2)**0.5
        dY = (self.playerY - y)/d
        dX = (self.playerX - x)/d
        #limits blink distance to 300 pixels away
        if d > 300:
            self.playerY -= (dY*300)
            self.playerX -= (dX*300)
        else:
            self.playerX = x
            self.playerY = y
        #stops player movement after blink and puts it on cooldown
        self.moving = False
        self.eOnCooldown = True
    
    def move(self):
        dist1 = ((self.playerX - self.destinationX)**2 +
                (self.playerY - self.destinationY)**2)**0.5
        dY1 = (self.playerY - self.destinationY)/dist1
        dX1 = (self.playerX - self.destinationX)/dist1
        if dist1 > 10:
            self.playerX -= 15*dX1
            self.playerY -= 15*dY1
        else:
            self.playerX = self.destinationX
            self.playerY = self.destinationY