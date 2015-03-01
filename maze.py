import pygame, random
from pygame.locals import *

class Maze:
    def __init__(self, mazeLayer, solveLayer):
        self.h = []
        self.f = []
        self.g = []
        self.currentState = 0
        self.parent = []
        self.closelist = []
        self.openlist = []
        self.path = []
        self.mazeArray = []
        self.mazeArrayb = []
        self.state = 'c'        # c = creating, s = solving, r = reset
        self.mLayer = mazeLayer # surface
        self.sLayer = solveLayer# surface
        #self.mLayer.fill((0, 0, 0, 0))
        self.sLayer.fill((0, 0, 0, 0))
        for y in xrange(6): # 80 wide + 60 tall
            pygame.draw.line(self.mLayer, (0,0,0,255), (0, y*80), (640, y*80))
            for x in xrange(8):
                self.mazeArrayb.append(0)
                self.mazeArray.append(0)
                self.h.append(0)
                #self.f.append(0)
                self.g.append(0)
                self.parent.append(0)
                self.openlist.append(0)
                self.closelist.append(0)
                #self.path.append(0)
                if ( y == 0 ):
                    pygame.draw.line(self.mLayer, (0,0,0,255), (x*80,0), (x*80,480))
        pygame.draw.rect(self.sLayer, (0,0,255,255), Rect(0,0,80,80))
        pygame.draw.rect(self.sLayer, (255,0,255,255), Rect((560),(400),80,80))
        # Maze Section
        self.totalCells = 48 # 80 * 60
        self.currentCell = random.randint(0, self.totalCells-1)
        self.visitedCells = 1
        self.cellStack = []
        self.compass = [(-1,0),(0,1),(1,0),(0,-1)]
        for i in xrange(48):
            self.h[i] = (7-(i%8)) + (5-(i/8))

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
                        if (self.mazeArray[(ny*8+nx)] & 0x000F) == 0:
                            nidx = ny*8+nx
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
                    #print(nidx)
                    self.visitedCells = self.visitedCells + 1
                    moved = True
                else:
                    self.currentCell = self.cellStack.pop()
            print("**********creation**********")            
        elif self.state == 's':
            if self.currentCell == (self.totalCells-1): # have we reached the exit?            
                self.state = 'r'
                return
            #self.openlist[0] = 1
            #self.closelist[0] = 1
            while self.currentState <> 47: #self.closelist[47] != 1:
                self.closelist[self.currentState] = 1
                print(self.currentState,"closelst")
                x = self.currentState % 8
                y = self.currentState / 8
                dir = [4,8,1,2]
                for i in xrange(4):
                    nx = x + self.compass[i][0]
                    ny = y + self.compass[i][1]
                    if ((nx >= 0) and (ny >= 0) and (nx < 8) and (ny < 6)):
                        if ((self.mazeArrayb[ny*8+nx] == dir[i]) or (self.mazeArrayb[self.currentState] & 1<<i > 0)):
                            #print(nx,ny)
                            nidx = ny*8 + nx
                            print(nidx,"nowall")
                            if self.closelist[nidx] == 0:
                                self.g[nidx] = self.g[self.currentState] + 10
                                print(self.g[nidx],nidx,"g")
                                self.f.append((self.g[nidx] + self.h[nidx],nidx))
                                print(self.f,"f")
                                if self.openlist[nidx] == 1:
                                    print(nidx,"ospcial")
                                    if self.g[nidx] > (self.g[self.currentState] + 10):
                                        self.parent[nidx] = self.currentState
                                        print(nidx,"ospecltstd")
                                else:
                                    self.parent[nidx] = self.currentState
                                    print(nidx,"opn")
                                self.openlist[nidx] = 1
                        else:
                            print(ny*8+nx,self.mazeArrayb[ny*8+nx],self.mazeArrayb[self.currentState],"wall")
                self.f.sort()
                print(self.f,"fs")
                #print(self.f[0])
                self.fval,self.currentState = self.f.pop(0)
                print(self.currentState,"curs")
                #self.closelist[self.currentState] = 1
            while self.currentState <> 0:
                self.path.append(self.currentState)
                self.curretState = self.parent[self.currentState]
            self.path.reverse()    
            moved = False
            while(moved == False):
                #x = self.currentCell % 8
                #y = self.currentCell / 8
                #neighbors = []
                #directions = self.mazeArray[self.currentCell] & 0xF
                #for i in xrange(4):
                #    if (directions & (1<<i)) > 0:
                #        nx = x + self.compass[i][0]
                #        ny = y + self.compass[i][1]
                #        if ((nx >= 0) and (ny >= 0) and (nx < 8) and (ny < 6)):              
                #            nidx = ny*8+nx
                #            if ((self.mazeArray[nidx] & 0xFF00) == 0): # make sure there's no backtrack
                #                neighbors.append((nidx,1<<i))
                #if len(neighbors) > 0:
                #    idx = random.randint(0,len(neighbors)-1)
                #    nidx,direction = neighbors[idx]
                self.ans = self.path.pop(0)
                x = self.ans % 8
                y = self.ans / 8 
                dx = x*80
                dy = y*80
                if direction & 1:
                    self.mazeArray[nidx] |= (4 << 12)
                elif direction & 2:
                    self.mazeArray[nidx] |= (8 << 12)
                elif direction & 4:
                    self.mazeArray[nidx] |= (1 << 12)
                elif direction & 8:
                    self.mazeArray[nidx] |= (2 << 12)
                pygame.draw.rect(self.sLayer, (0,255,0,255), Rect(dx,dy,80,80))
                self.mazeArray[self.currentCell] |= direction << 8
                self.cellStack.append(self.currentCell)
                self.currentCell = nidx
                moved = True
            #else:
            #    pygame.draw.rect(self.sLayer, (255,0,0,255), Rect((x*80),(y*80),80,80))
            #    self.mazeArray[self.currentCell] &= 0xF0FF # not a solution
            #    self.currentCell = self.cellStack.pop()
        elif self.state == 'r':
            self.__init__(self.mLayer,self.sLayer)

    def draw(self, screen):
        screen.blit(self.sLayer, (0,0))
        screen.blit(self.mLayer, (0,0))

def main():
    """Maze Main Function - Luke Arntson, Jan '09
        Written using - http://www.mazeworks.com/mazegen/mazetut/index.htm
    """
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Labyrinth')
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
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
        newMaze.update()
        screen.blit(background, (0, 0))
        newMaze.draw(screen)
        pygame.display.flip()

if __name__ == '__main__': main()