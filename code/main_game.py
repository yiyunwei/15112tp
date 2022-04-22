from cmu_112_graphics import *
from enemy_class import *
from map import *
from a_star import *
import math, random

def appStarted(app):
    app.timerDelay = 100
    #map/window attributes
    app.rows = len(gameMap)
    app.cols = len(gameMap[0])
    app.startRow = 13
    app.startCol = 13
    app.cellsInView = 6
    #player attributes
    app.playerR = 20
    app.playerX = app.width/2
    app.playerY = app.height/2
    app.moving = False
    app.shooting = False
    app.destinationX = None
    app.destinationY = None
    app.eOnCooldown = False
    app.eCooldown = 5000
    #bullet attributes
    app.shotR = 10
    app.shotX = None
    app.shotY = None
    app.aimedX = None
    app.aimedY = None
    #mouse attributes
    app.mouseX = 0
    app.mouseY = 0
    #sprites (drawn by myself)
    app.sprites = app.loadImage('slime sprites.png')
    app.playerSprite = app.sprites.crop((60, 25, 140, 81))
    app.bulletSprite = app.sprites.crop((200, 25, 250, 70))
    app.enemySprite = app.sprites.crop((62, 105, 145, 180))
    #enemy attributes
    app.enemies = []
    for row in range(app.rows):
        for col in range(app.cols):
            if enemyMap[row][col] == 2:
                app.enemies += [Enemy(col, row)]
    for enem in app.enemies:
        (x0, y0, x1, y1) = getCellBounds(app, enem.enemyCellY-app.startRow,
                                        enem.enemyCellX-app.startCol)
        enem.enemyPosX = (x0 + x1)/2
        enem.enemyPosY = (y0 + y1)/2

#CITATION: function from 15-112 images mini-lecture
def getCachedPhotoImage(app, image):
    #stores a cached photo
    if ('cachedPhotoImage' not in image.__dict__):
        image.cachedPhotoImage = ImageTk.PhotoImage(image)
    return image.cachedPhotoImage

def pointInGrid(app, x, y):
    return ((0 <= x <= app.width) and (0 <= y <= app.height))

#CITATION: grid tkinter code from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def getCellBounds(app, row, col):
    gridWidth  = app.width
    gridHeight = app.height
    cellWidth = gridWidth / app.cellsInView
    cellHeight = gridHeight / app.cellsInView
    x0 = col * cellWidth
    x1 = (col+1) * cellWidth
    y0 = row * cellHeight
    y1 = (row+1) * cellHeight
    return (x0, y0, x1, y1)

def getCell(app, x, y):
    #if (not pointInGrid(app, x, y)):
    #    return (-1, -1)
    gridWidth  = app.width
    gridHeight = app.height
    cellWidth  = gridWidth / app.cellsInView
    cellHeight = gridHeight / app.cellsInView

    row = int(y / cellHeight) + app.startRow
    col = int(x / cellWidth) + app.startCol

    return (row, col)

def redrawAll(app, canvas):
    #draws game map
    for row in range(app.startRow, app.startRow + app.cellsInView):
        for col in range(app.startCol, app.startCol + app.cellsInView):
            (x0, y0, x1, y1) = getCellBounds(app, row-app.startRow, col-app.startCol)
            if (enemyMap[row][col] == 0):
                fill = "black"
            else:
                fill = "white"
            canvas.create_rectangle(x0, y0, x1, y1, fill=fill)

    #shows the bullet when it's being shot
    if (app.shooting == True):
        canvas.create_image(app.shotX, app.shotY,
                            image = getCachedPhotoImage(app, app.bulletSprite))
    #draws player
    playCellY, playCellX = getCell(app, app.playerX, app.playerY)
    if (playCellY in range(app.startRow, app.startRow + app.cellsInView) and
        playCellX in range(app.startCol, app.startCol + app.cellsInView)):
        canvas.create_image(app.playerX, app.playerY,
                            image = getCachedPhotoImage(app, app.playerSprite))
    #draws enemy
    for enem in app.enemies:
        if (enem.enemyAlive == True and 
            enem.enemyCellY in range(app.startRow, app.startRow + app.cellsInView) and
            enem.enemyCellX in range(app.startCol, app.startCol + app.cellsInView)):
            canvas.create_image(enem.enemyPosX, enem.enemyPosY,
                                image = getCachedPhotoImage(app, app.enemySprite))

    canvas.create_text(20, 20, text = getCell(app, app.playerX, app.playerY))
    canvas.create_text(20, 40, text = getCell(app, app.mouseX, app.mouseY))

def mousePressed(app, event):
    #moves the player towards where the mouse is pressed
    if (event.x != app.playerX or event.y != app.playerY):
        app.moving = True
        app.destinationX = event.x
        app.destinationY = event.y

def keyPressed(app, event):
    #CITATION: tkinter keys + other stuff from https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/index.html
    #shoots an attack when q is pressed
    if event.key == 'q':
        if(app.shotX == app.aimedX and app.shotY == app.aimedY):
            return
        if app.shooting == False:
            app.shooting = True
            app.aimedX = app.mouseX
            app.aimedY = app.mouseY
    
    #blink to mouse position when e is pressed
    elif event.key == 'e' and app.eOnCooldown == False:
        d = ((app.playerX - app.mouseX)**2 + (app.playerY - app.mouseY)**2)**0.5
        dY = (app.playerY - app.mouseY)/d
        dX = (app.playerX - app.mouseX)/d
        #limits blink distance to 300 pixels away
        if d > 300:
            app.playerY -= (dY*300)
            app.playerX -= (dX*300)
        else:
            app.playerX = app.mouseX
            app.playerY = app.mouseY
        #stops player movement after blink and puts it on cooldown
        app.moving = False
        app.eOnCooldown = True
    
    #elif event.key == 'x' and app.enemy.enemyAlive == False:
    #    app.enemy.setCoords(app.mouseX, app.mouseY)
    #    app.enemy.enemyAlive = True
    
    if event.key == 's':
        if app.startRow + app.cellsInView < app.rows:
            app.startRow += 1
            app.playerY -= app.height/app.cellsInView
            for enem in app.enemies:
                if (enem.enemyPosY != None):
                    enem.enemyPosY -= app.height/app.cellsInView
            if (app.destinationX != None):
                app.destinationY -= app.height/app.cellsInView
    elif event.key == 'w':
        if app.startRow - 1 >= 0:
            app.startRow -=1
            app.playerY += app.height/app.cellsInView
            for enem in app.enemies:
                if (enem.enemyPosY != None):
                    enem.enemyPosY += app.height/app.cellsInView
            if (app.destinationY != None):
                app.destinationY += app.height/app.cellsInView
    elif event.key == 'd':
        if app.startCol + app.cellsInView < app.cols:
            app.startCol += 1
            app.playerX -= app.width/app.cellsInView
            for enem in app.enemies:
                if (enem.enemyPosX != None):
                    enem.enemyPosX -= app.width/app.cellsInView
            if (app.destinationX != None):
                app.destinationX -= app.height/app.cellsInView
    elif event.key == 'a':
        if app.startCol - 1 >= 0:
            app.startCol -= 1
            app.playerX += app.width/app.cellsInView
            for enem in app.enemies:
                if (enem.enemyPosX != None):
                    enem.enemyPosX += app.width/app.cellsInView
            if (app.destinationX != None):
                app.destinationX += app.height/app.cellsInView

def mouseMoved(app, event):
    #gets mouse's current position
    app.mouseX = event.x
    app.mouseY = event.y

def timerFired(app):
    #controls player movement
    if(app.playerX == app.destinationX and app.playerY == app.destinationY):
        app.moving = False
    #has player move slowly towards where the mouse has clicked
    elif(app.moving == True):
        dist1 = ((app.playerX - app.destinationX)**2 +
                (app.playerY - app.destinationY)**2)**0.5
        dY1 = (app.playerY - app.destinationY)/dist1
        dX1 = (app.playerX - app.destinationX)/dist1
        if dist1 > 10:
            tempX = app.playerX
            tempY = app.playerY
            app.playerX -= 15*dX1
            app.playerY -= 15*dY1
            leftCellY, leftCellX = getCell(app, app.playerX-40, app.playerY)
            rightCellY, rightCellX = getCell(app, app.playerX+40, app.playerY)
            topCellY, topCellX = getCell(app, app.playerX, app.playerY-28)
            botCellY, botCellX = getCell(app, app.playerX, app.playerY+28)
            if (gameMap[leftCellY][leftCellX] == 0 or gameMap[rightCellY][rightCellX] == 0 or
                gameMap[topCellY][topCellX] == 0 or gameMap[botCellY][botCellX] == 0):
                app.playerX = tempX
                app.playerY = tempY
        else:
            app.playerX = app.destinationX
            app.playerY = app.destinationY

    #controls bullet movement
    #keeps bullet starting point where the player is
    if (app.shooting == False):
        app.shotX, app.shotY = app.playerX, app.playerY
    #resets the bullet after it has reached its destination
    elif(app.shotX == app.aimedX and app.shotY == app.aimedY):
        app.shooting = False
    elif (app.shooting == True):
        dist2 = ((app.shotX - app.aimedX)**2 + (app.shotY - app.aimedY)**2)**0.5
        dY2 = (app.shotY - app.aimedY)/dist2
        dX2 = (app.shotX - app.aimedX)/dist2
        #limits the range of the bullet to 300 pixels
        if dist2 > 300:
            app.aimedY = app.shotY - (dY2*300)
            app.aimedX = app.shotX - (dX2*300)
        #bullet gradually travels to destination
        if dist2 > 70:
            app.shotX -= 70*dX2
            app.shotY -= 70*dY2
        #snaps to destination if it is less than 70 pixels away
        else:
            app.shotX = app.aimedX
            app.shotY = app.aimedY
    for enem in app.enemies:
        #bullet hits enemy + causes it to respawn
        if(enem.enemyAlive == True and 
            app.shotX <= enem.enemyPosX + 50 and app.shotX >= enem.enemyPosX - 50 and
            app.shotY <= enem.enemyPosY + 50 and app.shotY >= enem.enemyPosY - 50):
            app.shooting = False
            enem.enemyAlive = False
            enem.enemyPosX = enem.enemyPosY = None
            #app.enemyX = random.randint(100, app.width-100)
            #app.enemyY = random.randint(100, app.height-100)
        
    #controls enemy movement through pathfinding
    for enem in app.enemies:
        if (enem.enemyAlive == True and 
            enem.enemyCellY in range(app.startRow, app.startRow + app.cellsInView) and
            enem.enemyCellX in range(app.startCol, app.startCol + app.cellsInView)):
            playCellY, playCellX = getCell(app, app.playerX, app.playerY)
            if (playCellY in range(app.startRow, app.startRow + app.cellsInView) and
                playCellX in range(app.startCol, app.startCol + app.cellsInView)):
                path = a_star(gameMap, app.startCol, app.startRow, app.cellsInView, enem.enemyCellX,
                            enem.enemyCellY, playCellX, playCellY)
                if((enem.enemyCellY != playCellY or enem.enemyCellX != playCellX) and path != None):
                    x0, y0, x1, y1 = getCellBounds(app, path[1][0]-app.startRow,
                                                    path[1][1]-app.startCol)
                    enem.move(app.playerX, app.playerY, app.width/(app.cellsInView*2),
                                    x0, y0, x1, y1)
                    enem.enemyCellY, enem.enemyCellX = getCell(app, enem.enemyPosX, enem.enemyPosY)
                    path.pop(0)

    #monitors blink cooldown
    if (app.eOnCooldown == True):
        app.eCooldown -= app.timerDelay
        if (app.eCooldown == 0):
            app.eCooldown = 5000
            app.eOnCooldown = False

def main():
    runApp(width=750, height=750)

if __name__ == '__main__':
    main()