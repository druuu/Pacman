import mazeastar,math,minimax,ql,pygame,random
from pygame.locals import *
from time import sleep

cell = mazeastar.cell 
width = mazeastar.width
height = mazeastar.height
coord = mazeastar.coord
walls = mazeastar.walls


def aStar(mazeArrayb,currentState,compass):
    print mazeArrayb,currentState,compass
    h = []
    f = []
    g = [] 
    parent = []
    closelist = []
    openlist = []
    path = []
    spath = []
    for y in xrange(3): # 80 wide + 60 tall
            for x in xrange(4):
                h.append(0)
                g.append(0)
                parent.append(0)
                openlist.append(0)
                closelist.append(0)
    closelist[0] == 1
    while len(path) == 0:
        x = currentState % 4
        y = currentState / 4
        dir = [4,8,1,2]
        for i in xrange(4):
            nx = x + compass[i][0]
            ny = y + compass[i][1]
            if ((nx >= 0) and (ny >= 0) and (nx < 4) and (ny < 3)):
                if ((mazeArrayb[ny*4+nx] == dir[i]) or (mazeArrayb[currentState] & 1<<i > 0)):
                    nidx = ny*4 + nx
                    if closelist[nidx] == 0:
                        g[nidx] = g[currentState] + 10
                        f.append((g[nidx] + h[nidx],nidx))
                        if openlist[nidx] == 1:
                            if g[nidx] > (g[currentState] + 10):
                                parent[nidx] = currentState
                        else:
                            parent[nidx] = currentState
                        openlist[nidx] = 1
        f.sort()
        fval,currentState = f.pop(0)
        closelist[currentState] = 1
        if  len(path) == 0 and currentState == 47:
            while True:
                path.append(currentState)
                if currentState == 0:
                    break
                currentState = parent[currentState]
            spath = path
    print spath
    return spath

def argMax(d):
        """
        Returns the key with the highest value.
        """
        if len(d.keys()) == 0: return None
        all = d.items()
        values = [x[1] for x in all]
        maxIndex = values.index(max(values))
        return all[maxIndex][0]

def drawMaze(walls,mLayer):
    for wall in walls:
        dx = (wall%coord)*cell
        dy = (wall/coord)*cell
        pygame.draw.line(mLayer, (0,0,0,255), (dx,dy+1),(dx,dy+cell-1))
        pygame.draw.line(mLayer, (0,0,0,255), (dx+1,dy+cell),(dx+cell-1,dy+cell))
        pygame.draw.line(mLayer, (0,0,0,255), (dx+cell,dy+1),(dx+cell,dy+cell-1))
        pygame.draw.line(mLayer, (0,0,0,255), (dx+1,dy),(dx+cell-1,dy))
def ghostPos(currentCell1,blitList,compass,currentCell,sc):
    surr = []    
    small = None
    x = currentCell % mazeastar.coord
    y = currentCell / mazeastar.coord
    x1 = currentCell1 % mazeastar.coord
    y1 = currentCell1 / mazeastar.coord
    valDict1 = {}
    for i in xrange(5):
        nx1 = x1 + compass[i][0]
        ny1 = y1 + compass[i][1]
        if ((nx1 >= 0) and (ny1 >= 0) and (nx1 < mazeastar.width) and (ny1 < mazeastar.height)):
            if ny1*mazeastar.coord + nx1 not in walls:
                nidx1 = ny1*mazeastar.coord + nx1
                dist = math.sqrt(((nx1-x)**2 + (ny1-y)**2))
                valDict1[nidx1] = 10/(1+dist)
    currentCell1 = argMax(valDict1) 
    return currentCell1
def userGhost(ghost):
    compass = [(-1,0),(0,1),(1,0),(0,-1),(0,0)]
    keyDict = {1:ghost,0:ghost,2:ghost,3:ghost}
    x1 = ghost % mazeastar.coord
    y1 = ghost / mazeastar.coord
    for i in xrange(5):
        nx1 = x1 + compass[i][0]
        ny1 = y1 + compass[i][1]
        if ((nx1 >= 0) and (ny1 >= 0) and (nx1 < mazeastar.width) and (ny1 < mazeastar.height)):
            if ny1*mazeastar.coord + nx1 not in walls:
                nidx1 = ny1*mazeastar.coord + nx1
                keyDict[i] = nidx1
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return 
                if event.key == K_LEFT:
                    return keyDict[0]
                elif event.key == K_DOWN:
                    return keyDict[1]
                elif event.key == K_RIGHT:
                    return keyDict[2]
                elif event.key == K_UP:
                    return keyDict[3]
    
    pygame.event.clear()
#     keys=pygame.key.get_pressed()
#     if keys[K_LEFT]:
#         return keyDict[0]
#     elif keys[K_DOWN]:
#         return keyDict[1]
#     elif keys[K_RIGHT]:
#         return keyDict[2]
#     elif keys[K_UP]:
#         return keyDict[3]
           

def score(currentCell1,blitList,compass,currentCell):
    dup = [i for i in blitList]
    x = currentCell % 4
    x1 = currentCell1 % 4
    y = currentCell / 4
    y1 = currentCell1 / 4
    valDict = {}
    dir = [4,8,1,2]
    for i in xrange(5):
        small = 0
        nx = x + compass[i][0]
        ny = y + compass[i][1]
        if ((nx >= 0) and (ny >= 0) and (nx < 4) and (ny < 3)):
#             if ((mazeArrayb[ny*4+nx] == dir[i]) or (mazeArrayb[currentCell] & 1<<i > 0)):
            if ny*4 + nx not in walls:
                nidx = ny*4 + nx
#                 abc = math.sqrt((nx-x1)**2 + (ny-y1)**2)
#                 for food in dup:
#                     x2 = food % 4
#                     y2 = food / 4
#                     print x2,y2
#                     small = small + math.sqrt((nx-x2)**2 + (ny-y2)**2)
                val = minimax.scoreEval(currentCell1, blitList, nidx)
#                 if oldPos != nidx and currentCell1 != nidx:
                valDict[nidx] = val
    currentCell = argMax(valDict) 
#                 for food in blitList:
#                     x2 = food % 4
#                     y2 = food / 4
#                     dist = math.sqrt((nx-x2)**2 + (ny-y2)**2)
#                     temp1 = dist
#                     temp = temp + dist
#                     if val < 1.5:
#                         if small1 < val:
#                             print "val:",val,nidx
#                             small1 = val
#                             currentCell = nidx
#                     else:
#                         val1 = 1/(1+temp) + 1/(1+temp1)
#                         if small <= val1: 
#                             print "val1",val1,nidx
#                             small = val1 
#                             if nidx != oldPos:
#                                 currentCell = nidx
                        
    if currentCell in dup:
        dup.remove(currentCell)
    return currentCell,dup
                
def getValue(currentCell1, currentCell2, currentCell, blitList, featuresCounter):
    x = currentCell % mazeastar.coord
    y = currentCell / mazeastar.coord
    legalActions = []
    compass = [(-1,0),(0,1),(1,0),(0,-1),(0,0)]
    for i in xrange(5):
        nx = x + compass[i][0]
        ny = y + compass[i][1]
        if ((nx >= 0) and (ny >= 0) and (nx < mazeastar.width) and (ny < mazeastar.height)):
            if ny*mazeastar.coord + nx not in walls:
                nidx = ny*mazeastar.coord + nx
                legalActions.append(nidx)
    if legalActions:
        return max(getQValue(currentCell1, currentCell2, currentCell, blitList, nidx, featuresCounter) for nidx in legalActions)
    return 0.0

def getQValue(currentCell1, currentCell2, currentCell, blitList, nidx, featuresCounter):
    features = ql.getFeatures(currentCell1, currentCell2, currentCell, nidx, blitList)
    fSum = sum(featuresCounter[feature] * features[feature] for feature in features)
    
#     print "for neighbr of pacman %s is "% currentCell,"%s"% nidx,"total sum is %s"% fSum
#     print "features are:",features
    return fSum

def update(oldCurrentCell1, oldCurrentCell2, oldCurrentCell, oldBlitList, currentCell1, currentCell2, currentCell, blitList, featuresCounter, reward):
    
    features = ql.getFeatures(oldCurrentCell1, oldCurrentCell2, oldCurrentCell, currentCell, oldBlitList)
    
    correction = (reward + 0.8 * getValue(currentCell1, currentCell2, currentCell, blitList, featuresCounter)) - getQValue(oldCurrentCell1, oldCurrentCell2, oldCurrentCell, oldBlitList, currentCell, featuresCounter)
#     print correction
#     print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
    for feature in features.keys():
        featuresCounter[feature] = featuresCounter[feature] + 0.2 * correction *features[feature]
#         print "correction is:",correction,"feature is:",feature,"featurecounter of feature is:",featuresCounter[feature]
#         print "features are",features
#     print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"    
#     print featuresCounter
#     print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
    return featuresCounter

def nextCell(currentCell1, currentCell2, currentCell, blitList, featuresCounter):
    randomList = [1,2,3,4]
    randomMemo = []
    x = currentCell % mazeastar.coord
    x1 = currentCell1 % mazeastar.coord
    y = currentCell / mazeastar.coord
    y1 = currentCell1 / mazeastar.coord
    final = float("inf")
    featureDict = {} 
    compass = [(-1,0),(0,1),(1,0),(0,-1),(0,0)]
#     print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
    for i in xrange(5):
        nx = x + compass[i][0]
        ny = y + compass[i][1]
        sum = 0
        if ((nx >= 0) and (ny >= 0) and (nx < mazeastar.width) and (ny < mazeastar.height)):
            if ny*mazeastar.coord + nx not in walls:
                nidx = ny*mazeastar.coord + nx
                randomMemo.append(nidx)
                featureDict[nidx] = getQValue(currentCell1, currentCell2, currentCell, blitList, nidx, featuresCounter)
#     print randomMemo,featureDict
    if mazeastar.count < 50:
        if random.choice(randomList) == 4:
            print "RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR"
            key = random.choice([i for i in randomMemo])
            randomMemo = []
            mazeastar.count += 1
            return key,mazeastar.count
        else:
            return argMax(featureDict),mazeastar.count
    
    return argMax(featureDict),50








