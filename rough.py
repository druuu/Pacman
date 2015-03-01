import pygame, random, astar
from pygame.locals import *
import math
import random

class Maze:
    def __init__(self, mazeLayer, solveLayer):
        self.score = 0
        self.randList = []
        for i in xrange(12):
            self.randList.append(i)
        self.blitList = []
        for i in xrange(8):
            foo = random.choice(self.randList)
            if foo not in self.blitList:
                self.blitList.append(foo) 
        
        self.currentState = 0
        self.spath = []
        self.mazeArray = []
        self.mazeArrayb = [] 
        self.state = 'c'        # c = creating, s = solving, r = reset
        self.mLayer = mazeLayer # surface
        self.sLayer = solveLayer# surface
        self.sLayer.fill((0, 0, 0, 0))
        for y in xrange(3): # 80 wide + 60 tall
#             pygame.draw.line(self.mLayer, (0,0,0,255), (0, y*80), (640, y*80))
            for x in xrange(4):
                self.mazeArray.append(0)
                self.mazeArrayb.append(0)
#                 if ( y == 0 ):
#                     pygame.draw.line(self.mLayer, (0,0,0,255), (x*80,0), (x*80,480))
        pygame.draw.rect(self.sLayer, (0,0,255,255), Rect(0,0,80,80))
        pygame.draw.rect(self.sLayer, (255,0,255,255), Rect((240),(160),80,80))
        pellet = pygame.image.load("pacman.png").convert() 
        for i in xrange(len(self.blitList)):
            self.sLayer.blit(pellet,Rect((self.blitList[i]%4)*80,(self.blitList[i]/4444)*80,80,80))
        self.totalCells = 12 # 80 * 60
        self.currentCell = random.randint(0, self.totalCells-1)
        self.visitedCells = 1
        self.currentCell1 = random.randint(0, self.totalCells-1)
        self.cellStack = []
        self.compass = [(-1,0),(0,1),(1,0),(0,-1)]
    def update(self):
        if self.state == 'c':
            if self.visitedCells >= self.totalCells:
                self.currentCell = 0 # set current to top-left
                self.cellStack = []
                self.state = 's'
                return
            moved = False
            while(self.visitedCells < self.totalCells):#moved == False):
                x = self.currentCell % 8
                y = self.currentCell / 8
                neighbors = []
                for i in xrange(4):
                    nx = x + self.compass[i][0]
                    ny = y + self.compass[i][1]
                    if ((nx >= 0) and (ny >= 0) and (nx < 8) and (ny < 6)):
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
                while(moved == False):
                    x = self.currentCell % 4
                    y = self.currentCell / 4
                    dx = x*80
                    dy = y*80
                    x1 = self.currentCell1 % 4
                    y1 = self.currentCell1 / 4 
                    dir = [4,8,1,2]
                    oldPos = self.currentCell1
                    surr = [self.currentCell1]
                    small = None
                    for i in xrange(4):
                        nx1 = x1 + self.compass[i][0]
                        ny1 = y1 + self.compass[i][1]
                        if ((nx1 >= 0) and (ny1 >= 0) and (nx1 < 4) and (ny1 < 3)):
#                             if ((self.mazeArrayb[ny1*8+nx1] == dir[i]) or (self.mazeArrayb[self.currentCell1] & 1<<i > 0)):
                                nidx1 = ny1*4 + nx1
                                surr.append(nidx1)
                    for s in surr:
                        x2 = s%4
                        y2 = s/4
                        temp = math.sqrt((x-x2)**2 + (y-y2)**2) 
                        if small > temp or small == None:
                            small = temp
                            self.currentCell1 = s
                    self.currentCell = astar.score(self.currentCell1, self.blitList, self.compass, self.currentCell,oldPos,self.score)
                    x = self.currentCell % 4
                    y = self.currentCell / 4
                    dx = x*80
                    dy = y*80
                    pm1 = pygame.image.load("ball (1).gif").convert() 
                    p1 = pm1.get_rect()
                    x1 = self.currentCell1 % 4
                    y1 = self.currentCell1 / 4
                    dx1 = x1*80
                    dy1 = y1*80
                    self.sLayer.blit(pm1,Rect(dx1,dy1,80,80))
                    pm = pygame.image.load("pacman.001.png").convert() 
                    pellet = pygame.image.load("pacman.png").convert() 
                    p = pm.get_rect()
                    self.sLayer.blit(pm,Rect(dx,dy,80,80))
                    for i in xrange(len(self.blitList)):
                        self.sLayer.blit(pellet,Rect((self.blitList[i]%4)*80,(self.blitList[i]/4)*80,80,80))
#                     pygame.draw.rect(self.sLayer, p, Rect(dx,dy,80,80))
#                     self.score -= 1
#                     if self.currentCell in self.blitList:
# 
#                         self.score += 1
                    self.cellStack.append(self.currentCell)
                    moved = True
    def draw(self, screen):
        screen.blit(self.sLayer, (0,0))
        screen.blit(self.mLayer, (0,0))
    def resetSlayer(self):
        self.sLayer.fill((0, 0, 0, 0))
        pygame.draw.rect(self.sLayer, (0,0,255,255), Rect(0,0,80,80))
        pygame.draw.rect(self.sLayer, (255,0,255,255), Rect((240),(160),80,80))

def main():  
    """Maze Main Function - Luke Arntson, Jan '09
        Written using - http://www.mazeworks.com/mazegen/mazetut/index.htm
    """
    pygame.init()
    screen = pygame.display.set_mode((320,240))
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
    while 1:
        clock.tick(2)
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