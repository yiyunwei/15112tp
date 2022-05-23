from cmu_112_graphics import *
from enemy_class import *
from map import *
from a_star import *
from treasure_class import *
from music import *

import math, random

##########################################
# Splash Screen Mode
##########################################

def splashScreenMode_redrawAll(app, canvas):
    canvas.create_text(app.width/2, app.height/4, text='Welcome to',
                       font='Rockwell 70', fill='purple')
    canvas.create_text(app.width/2, app.height/4 + 90, text='Dungeon Explorer!',
                       font='Rockwell 70', fill='purple')
    canvas.create_text(app.width/2, app.height * 3/5, text='Press any key to enter the game!',
                       font='Rockwell 30', fill='black')

def splashScreenMode_keyPressed(app, event):
    app.music.unpause()
    app.mode = 'gameMode'

##########################################
# Game Mode
##########################################

def gameMode_redrawAll(app, canvas):
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

    #draws treasure
    for treas in app.treasure:
        if (treas.treasureUp == True and 
            treas.treasCellY in range(app.startRow, app.startRow + app.cellsInView) and
            treas.treasCellX in range(app.startCol, app.startCol + app.cellsInView)):
            canvas.create_image(treas.treasPosX, treas.treasPosY,
                                image = getCachedPhotoImage(app, app.treasureSprite))

    #draws enemy
    for enem in app.enemies:
        if (enem.enemyAlive == True and 
            enem.enemyCellY in range(app.startRow, app.startRow + app.cellsInView) and
            enem.enemyCellX in range(app.startCol, app.startCol + app.cellsInView)):
            canvas.create_image(enem.enemyPosX, enem.enemyPosY,
                                image = getCachedPhotoImage(app, app.enemySprite))
    #displays how much treasure + lives are left
    canvas.create_text(15, 25, text = f"Treasure Collected: {app.treasureFound}",
                            fill = '#ff0037', anchor = W, font = ('Rockwell', '20'))
    if app.treasureHintsOn == True:
        canvas.create_text(233, 25, text = f"/{app.totalTreasure}",
                            fill = '#ff0037', anchor = W, font = ('Rockwell', '20'))   
    canvas.create_text(15, 50, text = f"Lives: {app.hp}",
                        fill = '#ff0037', anchor = W, font = ('Rockwell', '20'))
    
    #game over screen
    if app.gameOver == True:
        canvas.create_rectangle((app.width/2)-150, (app.height/2)-80,
                                (app.width/2)+150, (app.height/2)+10, fill = "white",
                                width = 5)
        canvas.create_rectangle((app.width/2)-140, (app.height/2)+30,
                                (app.width/2)+140, (app.height/2)+70, fill = "white",
                                width = 5)
        canvas.create_text(app.width/2, (app.height/2)-30, text = "You Win!",
                            font = ('Rockwell', '40'), anchor = "center")
        canvas.create_text(app.width/2, (app.height/2)+50,
                            text = "Press 'R' to play again!", font = ('Rockwell', '20'))
    #pause menu
    elif app.paused == True:
        font = 'Rockwell 20'
        canvas.create_rectangle((app.width/2)-150, (app.height/4)-60,
                                (app.width/2)+150, (app.height/4)+40, fill = "white",
                                width = 5)
        canvas.create_rectangle((app.width/2)-300, (app.height/2)-100,
                                (app.width/2)+300, (app.height/2)+200, fill = "white",
                                width = 5)
        canvas.create_rectangle(210, 305, 235, 330, fill = "white",
                                width = 5)
        canvas.create_rectangle(335, 345, 360, 370, fill = "white",
                                width = 5)
        if app.music.isPlaying():
            canvas.create_rectangle(218, 313, 227, 322, fill = "black",
                                    width = 5)
        if app.treasureHintsOn == True:
            canvas.create_rectangle(343, 353, 352, 362, fill = "black",
                                    width = 5)
        canvas.create_text(app.width/2, (app.height/4)-10, text = "Game Paused",
                            font = ('Rockwell 30'))
        canvas.create_text((app.width/2)-270, (app.height/2)-55, text = "Music",
                            font = ('Rockwell 30'), anchor = W)
        canvas.create_text((app.width/2)-270, (app.height/2)-15, text = "Treasure Hints",
                            font = ('Rockwell 30'), anchor = W)
        canvas.create_text((app.width/2)-270, (app.height/2)+25, text = "Instructions:",
                            font = ('Rockwell 30'), anchor = W)
        canvas.create_text((app.width/2)-270, (app.height/2)+60,
                            text = "Left click to move", font = font, anchor = W)
        canvas.create_text((app.width/2)-270, (app.height/2)+90,
                            text = "Press Q to shoot enemies", font = font, anchor = W)
        canvas.create_text((app.width/2)-270, (app.height/2)+120,
                            text = "Press E to blink to cursor position",
                            font = font, anchor = W)
        canvas.create_text((app.width/2)-270, (app.height/2)+150,
                            text = "Use WASD to adjust window", font = font, anchor = W)
        canvas.create_text((app.width/2)-270, (app.height/2)+180,
                            text = "Avoid getting hit and collect all the treasure to win!",
                            font = font, anchor = W)

def gameMode_mousePressed(app, event):
    if app.paused == True and app.gameOver == False:
        #button for turning music on/off
        if (210 < event.x < 235 and 305 < event.y < 330):
            if (app.music.isPlaying()):
                app.music.pause()
            else:
                app.music.unpause()
        #button for turning hints on/off
        elif (335 < event.x < 360 and 345 < event.y < 370):
            if (app.treasureHintsOn == True):
                app.treasureHintsOn = False
            else:
                app.treasureHintsOn = True
    #moves the player towards where the mouse is pressed
    elif (event.x != app.playerX or event.y != app.playerY):
        app.moving = True
        app.destinationX = event.x
        app.destinationY = event.y

def gameMode_keyPressed(app, event):
    #CITATION: tkinter keys + other syntax from https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/index.html
    #pauses game when p is pressed + unpauses when pressed again
    if app.gameOver == True:
        if event.key == 'r':
            appStarted(app, 'gameMode')
        else:
            return
    
    #to pause game
    if event.key == 'p':
        if app.paused == False:
            app.paused = True
        else:
            app.paused = False
    if app.paused == True:
        return
    
    #shoots an attack when q is pressed
    if event.key == 'q':
        if(app.shotX == app.aimedX and app.shotY == app.aimedY):
            return
        if app.shooting == False:
            app.shooting = True
            app.aimedX = app.mouseX
            app.aimedY = app.mouseY
    
    #blink to mouse position when e is pressed
    elif (event.key == 'e' and app.eOnCooldown == False):
        leftCellY, leftCellX = getCell(app, app.mouseX-40, app.mouseY)
        rightCellY, rightCellX = getCell(app, app.mouseX+40, app.mouseY)
        topCellY, topCellX = getCell(app, app.mouseX, app.mouseY-28)
        botCellY, botCellX = getCell(app, app.mouseX, app.mouseY+28)
        if (gameMap[leftCellY][leftCellX] == 1 and gameMap[rightCellY][rightCellX] == 1 and
            gameMap[topCellY][topCellX] == 1 and gameMap[botCellY][botCellX] == 1):
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
    
    #adjusts the view window using wasd keys
    if event.key == 's':
        if app.startRow + app.cellsInView < app.rows:
            app.startRow += 1
            app.playerY -= app.height/app.cellsInView
            for enem in app.enemies:
                if (enem.enemyPosY != None):
                    enem.enemyPosY -= app.height/app.cellsInView
            for treas in app.treasure:
                treas.treasPosY -= app.height/app.cellsInView
            if (app.destinationX != None):
                app.destinationY -= app.height/app.cellsInView
    elif event.key == 'w':
        if app.startRow - 1 >= 0:
            app.startRow -=1
            app.playerY += app.height/app.cellsInView
            for enem in app.enemies:
                if (enem.enemyPosY != None):
                    enem.enemyPosY += app.height/app.cellsInView
            for treas in app.treasure:
                treas.treasPosY += app.height/app.cellsInView
            if (app.destinationY != None):
                app.destinationY += app.height/app.cellsInView
    elif event.key == 'd':
        if app.startCol + app.cellsInView < app.cols:
            app.startCol += 1
            app.playerX -= app.width/app.cellsInView
            for enem in app.enemies:
                if (enem.enemyPosX != None):
                    enem.enemyPosX -= app.width/app.cellsInView
            for treas in app.treasure:
                treas.treasPosX -= app.width/app.cellsInView
            if (app.destinationX != None):
                app.destinationX -= app.height/app.cellsInView
    elif event.key == 'a':
        if app.startCol - 1 >= 0:
            app.startCol -= 1
            app.playerX += app.width/app.cellsInView
            for enem in app.enemies:
                if (enem.enemyPosX != None):
                    enem.enemyPosX += app.width/app.cellsInView
            for treas in app.treasure:
                treas.treasPosX += app.width/app.cellsInView
            if (app.destinationX != None):
                app.destinationX += app.height/app.cellsInView

def gameMode_mouseMoved(app, event):
    #gets mouse's current position
    app.mouseX = event.x
    app.mouseY = event.y

def gameMode_timerFired(app):
    #pauses game
    if app.paused == True:
        return

    #restarts the game when your hp reaches 0
    if app.hp == 0:
        appStarted(app, 'gameMode')

    #game is over when you have found all the treasure
    if app.treasureFound == app.totalTreasure:
        app.gameOver = True
        app.paused = True

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

    #treasure collecting
    for treas in app.treasure:
        if(treas.treasureUp == True and 
            treas.treasPosX - 50 <= app.playerX <= treas.treasPosX + 50 and
            treas.treasPosY - 50 <= app.playerY <= treas.treasPosY + 50):
            treas.treasureUp = False
            app.treasureFound += 1

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
        if(enem.enemyAlive == True):
            #if enemy hits player player loses 1 hp
            if(enem.enemyPosX - 70 <= app.playerX <= enem.enemyPosX + 70 and
                enem.enemyPosY - 70 <= app.playerY <= enem.enemyPosY + 70):
                enem.enemyAlive = False
                enem.enemyPosX = enem.enemyPosY = None
                app.hp -= 1
            #if bullet hits enemy, the enemy dies
            elif(enem.enemyPosX - 40 <= app.shotX <= enem.enemyPosX + 40 and
                enem.enemyPosY - 40 <= app.shotY <= enem.enemyPosY + 40):
                app.shooting = False
                enem.enemyAlive = False
                enem.enemyPosX = enem.enemyPosY = None
        
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
                #makes it so that enemies keep chasing even if they're in the same cell as the player
                elif((enem.enemyPosY != playCellY or enem.enemyPosX != playCellX) and path != None):
                    enem.move(app.playerX, app.playerY, app.width, None, None, None, None)

    #monitors blink cooldown
    if (app.eOnCooldown == True):
        app.eCooldown -= app.timerDelay
        if (app.eCooldown == 0):
            app.eCooldown = 5000
            app.eOnCooldown = False

    #respawns enemy at their original location after being dead for a certain 
    #amount of time
    for enem in app.enemies:
        if enem.enemyAlive == False:
            enem.respawnTime -= app.timerDelay
            if (enem.respawnTime == 0):
                enem.respawnTime = 10000
                enem.enemyAlive = True
                enem.enemyCellX, enem.enemyCellY = enem.originX, enem.originY
                (x0, y0, x1, y1) = getCellBounds(app, enem.enemyCellY-app.startRow,
                                        enem.enemyCellX-app.startCol)
                enem.enemyPosX = (x0 + x1)/2
                enem.enemyPosY = (y0 + y1)/2

##########################################
# Main App
##########################################

def appStarted(app, mode = 'splashScreenMode'):
    app.mode = mode
    app.timerDelay = 100
    app.paused = False
    app.gameOver = False
    app.treasureHintsOn = False
    #CITATION: music from the game Helltaker (link: https://www.youtube.com/watch?v=GzeBHIto4Ps)
    pygame.mixer.init()
    app.music = Music("Helltaker OST.mp3")
    app.music.start()
    if app.mode == 'splashScreenMode':
        app.music.pause()
    #map/window attributes
    app.rows = len(gameMap)
    app.cols = len(gameMap[0])
    app.startRow = 12
    app.startCol = 12
    app.cellsInView = 7
    #player attributes
    app.playerX = 440
    app.playerY = 440
    app.moving = False
    app.shooting = False
    app.destinationX = None
    app.destinationY = None
    app.eOnCooldown = False
    app.eCooldown = 5000
    app.treasureFound = 0
    app.totalTreasure = 10
    app.hp = 5
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
    app.treasureSprite = app.sprites.crop((180, 90, 260, 170))
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
    #treasure attributes
    app.treasure = []
    for row in range(app.rows):
        for col in range(app.cols):
            if treasMap[row][col] == 3:
                app.treasure += [Treasure(col, row)]
    for treas in app.treasure:
        (x0, y0, x1, y1) = getCellBounds(app, treas.treasCellY-app.startRow,
                                        treas.treasCellX-app.startCol)
        treas.treasPosX = (x0 + x1)/2
        treas.treasPosY = (y0 + y1)/2

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

def main():
    runApp(width=750, height=750)

if __name__ == '__main__':
    main()