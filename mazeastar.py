import pygame, random, astar, minimax
from pygame.locals import *
import math
import random

sp = 0
count = 0
walls = [4,13,19,20,22,24,25,26,27,28,29,31,33,34,37,52,55,57,58,60,65,67,68,70,78,83,91,93,94,96,97,98,99,100,101,103,104,106,109,124,127,128,130,132,133,134,135,136,137,139,141,142,148,157]#[5,22,33,9,31,44,28]
coord = 18
width = 18
height = 9
cell = 80
class Maze:
    def __init__(self, mazeLayer=0, solveLayer=0):
        self.featuresCounter = {'closest-food': -0.5, '#-of-ghosts-1-step-away': -10, 'eats-food': 0.3 }
        self.agent = 'p'
        self.score = 0
        self.randList = []
        for i in xrange(1):
            self.randList.append(i)
#         self.blitListR = [11,10,6,8,1,4,7,23,24,21,40,39,30]
        self.blitListR = []
        for i in xrange(161):
            self.blitListR.append(i)
        for i in walls :
            self.blitListR.remove(i)
        self.blitList = []
#         for i in xrange(8):
#             foo = random.choice(self.randList)
#             if foo not in self.blitList:
#                 self.blitList.append(foo) 
        
        self.currentState = 0
        self.spath = []
        self.mazeArray = []
        self.mazeArrayb = [] 
        self.state = 's'        # c = creating, s = solving, r = reset
        self.mLayer = mazeLayer # surface
        self.sLayer = solveLayer# surface
        self.sLayer.fill((0, 0, 0, 0))
        for y in xrange(height): # 80 wide + 60 tall
#             pygame.draw.line(self.mLayer, (0,0,0,255), (0, y*80), (320, y*80))
            for x in xrange(width):
                self.mazeArray.append(0)
                self.mazeArrayb.append(0)
#                 if ( y == 0 ):
#                     pygame.draw.line(self.mLayer, (0,0,0,255), (x*80,0), (x*80,240))
#         pygame.draw.rect(self.sLayer, (0,0,255,255), Rect(0,0,80,80))
#         pygame.draw.rect(self.sLayer, (255,0,255,255), Rect((240),(160),80,80))
        pellet = pygame.image.load("pacman.png").convert() 
        for i in xrange(len(self.blitList)):
            self.sLayer.blit(pellet,Rect((self.blitList[i]%coord)*cell,(self.blitList[i]/coord)*cell,cell,cell))
        self.totalCells = height*width # 80 * 60
        self.currentCell = 15#random.randint(0, self.totalCells-1)
        self.visitedCells = 1
#         self.currentCell1 = random.randint(0, self.totalCells-1)
#         if self.currentCell1 == 5:
        self.currentCell1 = 19
        self.currentCell2 = 19
        self.cellStack = []
        self.compass = [(-1,0),(0,1),(1,0),(0,-1),(0,0)]
        astar.drawMaze(walls,self.mLayer)
        
    def update(self):
        global sp
        if self.state == 'c':
            if self.visitedCells >= self.totalCells:
                self.currentCell = 0 # set current to top-left
                self.cellStack = []
                self.state = 's'
                return
            moved = False
            while(self.visitedCells < self.totalCells):#moved == False):
                x = self.currentCell % 4
                y = self.currentCell / 4
                neighbors = []
                for i in xrange(4):
                    nx = x + self.compass[i][0]
                    ny = y + self.compass[i][1]
                    if ((nx >= 0) and (ny >= 0) and (nx < width) and (ny < height)):
                        if (self.mazeArray[(ny*4+nx)] & 0x000F) == 0:
                            nidx = ny*4+nx
                            neighbors.append((nidx,1<<i))
                if len(neighbors) > 0:
                    idx = random.randint(0,len(neighbors)-1)
                    nidx,direction = neighbors[idx]
                    dx = x*80
                    dy = y*80
                    if direction & 1:
                        self.mazeArray[nidx] |= (4)
                        self.mazeArrayb[nidx] = (4)
                        pygame.draw.line(self.mLayer, (0,0,0,0), (dx,dy+1),(dx,dy+79))
                    elif direction & 2:
                        self.mazeArray[nidx] |= (8)
                        self.mazeArrayb[nidx] = (8)
                        pygame.draw.line(self.mLayer, (0,0,0,0), (dx+1,dy+80),(dx+79,dy+80))
                    elif direction & 4:
                        self.mazeArray[nidx] |= (1)
                        self.mazeArrayb[nidx] = (1)
                        pygame.draw.line(self.mLayer, (0,0,0,0), (dx+80,dy+1),(dx+80,dy+79))
                    elif direction & 8:
                        self.mazeArray[nidx] |= (2)
                        self.mazeArrayb[nidx] = (2)
                        pygame.draw.line(self.mLayer, (0,0,0,0), (dx+1,dy),(dx+79,dy))
                    self.mazeArray[self.currentCell] |= direction
                    self.cellStack.append(self.currentCell)
                    self.currentCell = nidx
                    self.visitedCells = self.visitedCells + 1
                    moved = True
                else:
                    self.currentCell = self.cellStack.pop()

        elif self.state == 's':
#             if len(self.spath) == 0:
#                 self.spath = astar.aStar(self.mazeArrayb,self.currentState,self.compass)
#             while len(self.path) == 0:
#                 x = self.currentState % 8
#                 y = self.currentState / 8
#                 dir = [4,8,1,2]
#                 for i in xrange(4):
#                     nx = x + self.compass[i][0]
#                     ny = y + self.compass[i][1]
#                     if ((nx >= 0) and (ny >= 0) and (nx < 8) and (ny < 6)):
#                         if ((self.mazeArrayb[ny*8+nx] == dir[i]) or (self.mazeArrayb[self.currentState] & 1<<i > 0)):
#                             nidx = ny*8 + nx
#                             if self.closelist[nidx] == 0:
#                                 self.g[nidx] = self.g[self.currentState] + 10
#                                 self.f.append((self.g[nidx] + self.h[nidx],nidx))
#                                 if self.openlist[nidx] == 1:
#                                     if self.g[nidx] > (self.g[self.currentState] + 10):
#                                         self.parent[nidx] = self.currentState
#                                 else:
#                                     self.parent[nidx] = self.currentState
#                                 self.openlist[nidx] = 1
#                 self.f.sort()
#                 self.fval,self.currentState = self.f.pop(0)
#                 self.closelist[self.currentState] = 1
#                 if  len(self.path) == 0 and self.currentState == 47:
#                     while True:
#                         self.path.append(self.currentState)
#                         if self.currentState == 0:
#                             break
#                         self.currentState = self.parent[self.currentState]
#                     self.spath = self.path    
#             print self.spath
#             if self.currentCell <> (self.totalCells-1):
#                 self.currentCell = self.spath.pop()
                moved = False
                if moved == False:
                    oldCurrentCell = self.currentCell
                    oldCurrentCell1 = self.currentCell1
                    oldCurrentCell2 = self.currentCell2
                    self.blitList = [i for i in self.blitListR]
                    oldBlitList = self.blitList
                    ghost1 = []
                    ghost2 = []
                    if self.agent == 'g':
                        x1 = self.currentCell1 % coord
                        y1 = self.currentCell1 / coord
                        x2 = self.currentCell2 % coord
                        y2 = self.currentCell2 / coord
                        for i in xrange(4):
                            nx1 = x1 + self.compass[i][0]
                            ny1 = y1 + self.compass[i][1]
                            nidx1 = ny1*coord+nx1
                            if ((nx1 >= 0) and (ny1 >= 0) and (nx1 < width) and (ny1 < height)):
                                if nidx1 not in walls:
                                    ghost1.append(nidx1)
                        for i in xrange(4):
                            nx2 = x2 + self.compass[i][0]
                            ny2 = y2 + self.compass[i][1]
                            nidx2 = ny2*coord+nx2
                            if ((nx2 >= 0) and (ny2 >= 0) and (nx2 < width) and (ny2 < height)):
                                if nidx2 not in walls:
                                    ghost2.append(nidx2)
                        
                        self.currentCell1 = astar.ghostPos(self.currentCell1, self.blitList,self.compass, self.currentCell,self.score)
                        self.currentCell2 = random.choice(ghost2)#astar.ghostPos(self.currentCell2, self.blitList,self.compass, self.currentCell,self.score)
                        x = self.currentCell % coord
                        y = self.currentCell / coord
                        dx = x*cell
                        dy = y*cell
                        x1 = self.currentCell1 % coord
                        y1 = self.currentCell1 / coord
                        x2 = self.currentCell2 % coord
                        y2 = self.currentCell2 / coord
                        dx1 = x1*cell
                        dy1 = y1*cell
                        dx2 = x2*cell
                        dy2 = y2*cell
                        pm1 = pygame.image.load("ball (1).gif").convert()
                        pm2 = pygame.image.load("ghost.png").convert() 
                        self.sLayer.blit(pm1,Rect(dx1,dy1,cell,cell))
                        self.sLayer.blit(pm2,Rect(dx2,dy2,cell,cell))
                        pm = pygame.image.load("pacman.001.png").convert()
                        self.sLayer.blit(pm,Rect(dx,dy,cell,cell))
                    if self.agent == 'p':
                        self.currentCell = minimax.value(self.currentCell1,self.currentCell2,self.blitList,self.compass,self.currentCell,0,0,self.score)
                        #astar.nextCell(self.currentCell1, self.currentCell2, self.currentCell, self.blitList, self.featuresCounter)
                        x = self.currentCell % coord
                        y = self.currentCell / coord
                        dx = x*cell
                        dy = y*cell
                        x1 = self.currentCell1 % coord
                        y1 = self.currentCell1 / coord
                        dx1 = x1*cell
                        dy1 = y1*cell
                        x2 = self.currentCell2 % coord
                        y2 = self.currentCell2 / coord
                        dx2 = x2*cell
                        dy2 = y2*cell
                        pm = pygame.image.load("pacman.001.png").convert()
                        self.sLayer.blit(pm,Rect(dx,dy,cell,cell))
                        pm1 = pygame.image.load("ball (1).gif").convert()
                        pm2 = pygame.image.load("ghost.png").convert() 
                        self.sLayer.blit(pm1,Rect(dx1,dy1,cell,cell))
                        self.sLayer.blit(pm2,Rect(dx2,dy2,cell,cell))
                        if self.currentCell in self.blitListR:
                            self.score = minimax.scoreEval(self.currentCell1, self.currentCell2, self.blitListR, self.currentCell, self.score, 0)
                            self.blitListR.remove(self.currentCell)
                        else:
                            self.score = minimax.scoreEval(self.currentCell1, self.currentCell2, self.blitListR, self.currentCell, self.score, 0)
                        self.blitList = self.blitListR
#                         print "old %s",oldCurrentCell,"new",self.currentCell
#                         self.featuresCounter = astar.update(oldCurrentCell1, oldCurrentCell2, oldCurrentCell, oldBlitList, self.currentCell1, self.currentCell2, self.currentCell, self.blitList, self.featuresCounter, self.score)
#                         print "featurescounter",self.featuresCounter
                        
                    if self.agent == 'p':
                        self.agent = 'g'
                    else:
                        self.agent = 'p'
                    pellet = pygame.image.load("pacman.png").convert() 
                    for i in self.blitList:
                        self.sLayer.blit(pellet,Rect((i%coord)*cell,(i/coord)*cell,cell,cell))
#                     pygame.draw.rect(self.sLayer, p, Rect(dx,dy,80,80))
#                     if self.currentCell == self.currentCell1 or self.currentCell == self.currentCell2 or len(self.blitListR) == 0:
#                             print "NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN"
#                             print "NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN"
#                             self.currentCell = 0
#                             self.currentCell1 = 2
#                             self.currentCell2 = 3
#                             self.blitListR = [11,10,6,8,1,4,7,23,24,21,40,39,30]
#                             self.blitList = []
#                             self.score = 0
#                             self.agent = 'p'
                    moved = True
    def draw(self, screen):
        screen.blit(self.sLayer, (0,0))
        screen.blit(self.mLayer, (0,0))
    def resetSlayer(self):
        self.sLayer.fill((0, 0, 0, 0))
#         pygame.draw.rect(self.sLayer, (0,0,255,255), Rect(0,0,80,80))
#         pygame.draw.rect(self.sLayer, (255,0,255,255), Rect((240),(160),80,80))

def main():  
    """Maze Main Function - Luke Arntson, Jan '09
        Written using - http://www.mazeworks.com/mazegen/mazetut/index.htm
    """
    pygame.init()
    screen = pygame.display.set_mode((1440, 720))
    pygame.display.set_caption("druuu's game")
    pygame.mouse.set_visible(0)
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))
    mazeLayer = pygame.Surface(screen.get_size())
    mazeLayer = mazeLayer.convert_alpha()
    mazeLayer.fill((0, 0, 0, 0))
    solveLayer = pygame.Surface(screen.get_size())
    solveLayer = solveLayer.convert_alpha()
    solveLayer.fill((0, 0, 0, 0))
    newMaze = Maze(mazeLayer,solveLayer)
    screen.blit(background, (0, 0))
    pygame.display.flip()
    clock = pygame.time.Clock()
    t = 20
    while 1:
        clock.tick(5)
#         if sp == 50 :
#             t =2 
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
        newMaze.update()
        screen.blit(background, (0, 0))
        newMaze.draw(screen)
        pygame.display.flip()
        newMaze.resetSlayer()
    print newMaze.score 
if __name__ == '__main__': main()