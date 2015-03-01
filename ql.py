import mazeastar

cell = mazeastar.cell 
width = mazeastar.width
height = mazeastar.height
coord = mazeastar.coord
walls = mazeastar.walls

def divideAll(fDict,divisor):
        """
        Divides all counts by divisor
        """
        divisor = float(divisor)
        for key in fDict:
            fDict[key] /= divisor

def closestFood(blitList, nextPos, currentCell):
    """
    closestFood -- this is similar to the function that we have
    worked on in the search project; here its all in one place
    """
    fringe = [(nextPos, 0)]
    expanded = set()
    while fringe:
        nextPos, dist = fringe.pop(0)
        if nextPos in expanded:
            continue
        expanded.add(nextPos)
        # if we find a food at this location then exit
        if nextPos in blitList:
            return dist
        # otherwise spread out from the location to its neighbours
        x = nextPos % mazeastar.coord
        y = nextPos / mazeastar.coord
        compass = [(-1,0),(0,1),(1,0),(0,-1),(0,0)]
        for i in xrange(5):
            nx = x + compass[i][0]
            ny = y + compass[i][1]
            if ((nx >= 0) and (ny >= 0) and (nx < mazeastar.width) and (ny < mazeastar.height)):
                if ny*mazeastar.coord + nx not in walls:
                    nidx = ny*mazeastar.coord + nx
                    fringe.append((nidx, dist+1))
    # no food found
    return None


def getFeatures(currentCell1, currentCell2, currentCell, nextPos, blitList):
    features = {}
    foo = []
    compass = [(-1,0),(0,1),(1,0),(0,-1),(0,0)]
#     features["bias"] = 1.0
    x1 = currentCell1 % mazeastar.coord
    y1 = currentCell1 / mazeastar.coord
    x2 = currentCell2 % mazeastar.coord
    y2 = currentCell2 / mazeastar.coord
    for i in xrange(5):
        nx1 = x1 + compass[i][0]
        ny1 = y1 + compass[i][1]
        nx2 = x2 + compass[i][0]
        ny2 = y2 + compass[i][1]
        nidx1 = ny1*mazeastar.coord + nx1
        nidx2 = ny2*mazeastar.coord + nx2
        if ((nx1 >= 0) and (ny1 >= 0) and (nx1 < mazeastar.width) and (ny1 < mazeastar.height)):
            if nidx1 not in walls:
                if nextPos == nidx1:
                    foo.append(1)
        if ((nx2 >= 0) and (ny2 >= 0) and (nx2 < mazeastar.width) and (ny2 < mazeastar.height)):
            if nidx2 not in walls:
                if nextPos == nidx2:
                    foo.append(1)
    if len(foo) == 1:
        features["#-of-ghosts-1-step-away"] = 1
    elif len(foo) == 2:
        features["#-of-ghosts-1-step-away"] = 2
    else:
        features["#-of-ghosts-1-step-away"] = 0 
    # if there is no danger of ghosts then add the food feature
    if features["#-of-ghosts-1-step-away"] == 0 and nextPos in blitList :
        features["eats-food"] = 1.0 
    
    dist = closestFood(blitList, nextPos, currentCell)
    if dist is not None:
        # make the distance a number less than one otherwise the update
        # will diverge wildly
        features["closest-food"] = float(dist) / mazeastar.width*mazeastar.height
    divideAll(features,10.0)
    return features
