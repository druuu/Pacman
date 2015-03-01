import astar,math,mazeastar

# cell = mazeastar.cell 
# width = mazeastar.width
# height = mazeastar.height
# coord = mazeastar.coord
# walls = mazeastar.walls
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
                if ny*mazeastar.coord + nx not in mazeastar.walls:
                    nidx = ny*mazeastar.coord + nx
                    fringe.append((nidx, dist+1))
    # no food found
    return 0
def scoreEval(currentCell1, currentCell2, blitList,currentCell,sc, depth):
#     print "eval sc",sc
    dup = [i for i in blitList]
    x = currentCell % mazeastar.coord
    y = currentCell / mazeastar.coord
    x1 = currentCell1 % mazeastar.coord
    y1 = currentCell1 / mazeastar.coord
    compass = [(-1,0),(0,1),(1,0),(0,-1),(0,0)]
    dist = closestFood(blitList, currentCell, 0)
    sc = sc - 50 - 0.01*dist
    if currentCell == currentCell1 or currentCell == currentCell2:
        sc = sc - 5000
    elif currentCell in dup:
        dup.remove(currentCell)
        if len(dup) == 0:
            sc = sc + 5100
        sc = sc + 1000*1/(1+depth)
    return sc
        
     
 
def value(currentCell1,currentCell2,blitList,compass,currentCell,index,depth,sc):
    if index > 2:
        index = 0
    if depth >= 3 :
        return sc         
    elif index != 0:
        return min_value(currentCell1,currentCell2,blitList,compass,currentCell,index,depth,sc)
    elif index == 0:
        return max_value(currentCell1,currentCell2,blitList,compass,currentCell,index,depth,sc)    
          
def max_value(currentCell1,currentCell2,blitList,compass,currentCell,index,depth,sc):
    v = -float("inf")
    x = currentCell % mazeastar.coord
    y = currentCell / mazeastar.coord
    
    for i in xrange(5):
        nx = x + compass[i][0]
        ny = y + compass[i][1]
        if ((nx >= 0) and (ny >= 0) and (nx < mazeastar.width) and (ny < mazeastar.height)):
            if ny*mazeastar.coord + nx not in mazeastar.walls:
                nidx = ny*mazeastar.coord + nx
                dupBl = [food for food in blitList]
                dupSc = scoreEval(currentCell1,currentCell2, dupBl, nidx, sc, depth)
                if nidx in dupBl:
                    dupBl.remove(nidx)
                pSuccValue = value(currentCell1,currentCell2,dupBl,compass,nidx,index+1,depth,dupSc)
                if depth == 0 :
                    print "neighbour",nidx,"parent",currentCell
                    print "food=",blitList
                    print "value=",pSuccValue
                if v < pSuccValue:
                    v = pSuccValue
                    bar = nidx
    if depth == 0:
        print "#################################################################################################################################################"
        print "max selected value ",v,"i,e node",bar
        print "#################################################################################################################################################"
        return bar
    else:
        return v
  
def min_value(currentCell1,currentCell2,blitList,compass,currentCell,index,depth,sc):
#     print "MIN MIN pacman,g1,g2,atdepth,score",currentCell,currentCell1,currentCell2,depth,sc
    v = float("inf")
    if index == 1:
        x = currentCell1 % mazeastar.coord
        y = currentCell1 / mazeastar.coord
    elif index == 2: 
        x = currentCell2 % mazeastar.coord
        y = currentCell2 / mazeastar.coord
    if index != 0:
        if index >= 2:
            depth += 1
        for i in xrange(4):
            nx = x + compass[i][0]
            ny = y + compass[i][1]
            if ((nx >= 0) and (ny >= 0) and (nx < mazeastar.width) and (ny < mazeastar.height)):
                if ny*mazeastar.coord + nx not in mazeastar.walls:
                    nidx = ny*mazeastar.coord + nx
                    if index == 1:
                        currentCell1 = nidx
                    elif index == 2:
                        currentCell2 = nidx
                    dupBl = [i for i in blitList]
                    dupSc = scoreEval(currentCell1,currentCell2, dupBl,currentCell, sc, depth)
                    if nidx in dupBl:
                        dupBl.remove(nidx)
                    gSuccValue = value(currentCell1,currentCell2,dupBl,compass,currentCell,index+1,depth,dupSc)
                    v = min(v,gSuccValue)
    return v
