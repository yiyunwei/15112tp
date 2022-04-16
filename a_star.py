#CITATION: pathfinding info from:
#https://www.cs.cmu.edu/~112/notes/student-tp-guides/Pathfinding.pdf
#https://isaaccomputerscience.org/concepts/dsa_search_a_star
G_SCORE = 0
F_SCORE = 1
PREVIOUS = 2

#row = y, col = x

#CITATION: manhattan distance info from https://en.wikipedia.org/wiki/Taxicab_geometry
def manhattanDist(x1, y1, x2, y2):
    return abs(x1-x2) + abs(y1-y2)

def lowestFScore(d):
    lowest = 10**5
    lowestNode = (-1, -1)

    for key in d:
        if (d[key][F_SCORE] != None):
            if(d[key][F_SCORE] < lowest):
                lowest = d[key][F_SCORE]
                lowestNode = key
    
    return lowestNode

def getNeighbors(cellX, cellY, graph, cornerCellX, cornerCellY, cellsInView):
    result = []

    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if ((i == 0 and j == 0) or (i != 0 and j != 0)):
                continue
            elif (cornerCellY <= cellY + i < cornerCellY + cellsInView and
                cornerCellX <= cellX + j < cornerCellX + cellsInView):
                if graph[cellY + i][cellX + j] == 1:
                    result += [(cellY + i, cellX + j)]
    return result

def getPath(d, startX, startY, endX, endY):
    result = []
    result += [(endY, endX)]
    while (startY, startX) not in result:
        currStep = result[0]
        nextStep = d[currStep][PREVIOUS]
        result.insert(0, nextStep)

    return result

def a_star(graph, cornerCellX, cornerCellY, cellsInView, startCellX,
            startCellY, targetCellX, targetCellY):
    visited = dict()
    unvisited = dict()

    for i in range(cornerCellY, cornerCellY + cellsInView):
        for j in range(cornerCellX, cornerCellX + cellsInView):
            if graph[i][j] == 0:
                continue
            unvisited[(i, j)] = [None, None, None]

    h_score = manhattanDist(startCellX, startCellY, targetCellX, targetCellY)
    unvisited[(startCellY, startCellX)] = [0, h_score, None]

    finished = False
    while(finished == False):
        if len(unvisited) == 0:
            finished = True
        else:
            currNode = lowestFScore(unvisited)
            if currNode == (targetCellY, targetCellX):
                finished = True
                visited[currNode] = unvisited[currNode]
            else:
                neighbors = getNeighbors(currNode[1], currNode[0], graph,
                            cornerCellX, cornerCellY, cellsInView)
                for n in neighbors: 
                    if n not in visited:
                        newGScore = (unvisited[currNode][G_SCORE] +
                                    manhattanDist(n[1], n[0], currNode[1], currNode[0]))
                        if (unvisited[n][G_SCORE] == None or 
                            newGScore < unvisited[n][G_SCORE]):
                            unvisited[n][G_SCORE] = newGScore
                            unvisited[n][F_SCORE] = (newGScore +
                                manhattanDist(n[1], n[0], targetCellX, targetCellY))
                            unvisited[n][PREVIOUS] = currNode

                visited[currNode] = unvisited.pop(currNode)
    return getPath(visited, startCellX, startCellY, targetCellX, targetCellY)