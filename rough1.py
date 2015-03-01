import mazeastar,math
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

def scf(sc,nidx,dup,currentCell1):           
        if nidx in dup:
            sc += 1
            dup.remove(nidx)
            if len(dup) == 0:
                sc = sc + 500 
        else:
            sc = sc - 1
        if nidx == currentCell1:
            sc = sc - 300
        print "sc",sc
        return sc
    
def score(currentCell1,blitList,compass,currentCell,oldPos,sc):
    print oldPos,currentCell1
    x = currentCell % 4
    x1 = currentCell1 % 4
    y = currentCell / 4
    y1 = currentCell1 / 4
    small = float("inf")
    small1 = -float("inf")
    valDict = {}
    dup = [i for i in blitList]
    
    for i in xrange(4):
        temp = 0
        nx = x + compass[i][0]
        ny = y + compass[i][1]
        if ((nx >= 0) and (ny >= 0) and (nx < 4) and (ny < 3)):
                nidx = ny*4 + nx
                abc = (nx-x1)**2 + (ny-y1)**2
                print abc,nx,x1,ny,y1,"****",nidx,currentCell1
                for food in blitList:
                    x2 = food % 4
                    y2 = food / 4
                    dist = math.sqrt((nx-x2)**2 + (ny-y2)**2)
                    if small > dist:
                        small = dist
                val = scf(sc,nidx,dup,currentCell1) #math.sqrt(abc) + 10/(1+dist)
                if oldPos != nidx:
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
    print valDict,currentCell,"--",currentCell1 
    if currentCell in blitList:
        blitList.remove(currentCell)
    print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@',currentCell
    return currentCell
    
    
                










