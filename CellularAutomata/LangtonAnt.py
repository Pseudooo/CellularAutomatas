import pygame

# Create a vector object to allow for directions to be handelled easier
class Vector():
    # Initialize the vector with i and j components
    def __init__(self, i:int, j:int): 
        self.i = i
        self.j = j
        
    def geti(self): # Get the i component
        return self.i
    
    def seti(self, i:int): # Set the i component
        self.i = i
        
    def getj(self): # Get the j component
        return self.j
    
    def setj(self, j:int): # Set the j component
        self.j = j
        
    def rotateCW(self): # Rotate the vector 90d clockwise
        self.i,self.j = self.j,-self.i
        
    def rotateCCW(self): # Rotate the vector 90d AntiClockwise
        self.i,self.j = -self.j,self.i
        
    def __str__(self): # Return a pretty string
        return "("+str(self.i)+"i + "+str(self.j)+"j)"
    
# Here we define an ant object to better handle the ant(s) on the screen
class Ant():
    # Initialize the ant with a direction and position
    def __init__(self, Direction:Vector, x:int, y:int):
        self.direction = Direction
        self.x = x
        self.y = y
        
    def getDirection(self): # Get the direction of the ant
        return self.direction
    
    def setDirection(self, Direction:Vector):
        self.direction = Direction
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def setX(self, x:int):
        self.x = x
        
    def setY(self, y:int):
        self.y = y
        
    def moveForward(self):
        self.x+=self.direction.geti()
        self.y+=self.direction.getj()
        
# Create the cell matrix
CellMatrix = [[False for a in range(80)] for b in range(80)]

win = pygame.display.set_mode((800,800))
pygame.display.set_caption("Langton's Ant")

def redrawCell(x:int, y:int):
    col = None
    if CellMatrix[y][x] == True:
        col = (255,255,255)
    else:
        col = (0,0,0)
    
    pygame.draw.rect(win, col, (x*10,y*10,10,10))

# The state of activity for the simulation
active = False

Ants = []

# Main game loop
run = True
while(run):
    # Update display for next simulation tick
    pygame.display.update()
    
    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            x,y=int(x//10),int(y//10)
            
            NewAnt = Ant(Vector(0, 1), x, y)
            Ants.append(NewAnt)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                active = not active
                print('Active set to: %d' % active)
    
    if active == True:
        # Simulation is active
        cellQueue = []
        
        for i in range(len(Ants)):
            ant = Ants[i]
            x,y = ant.getX(),ant.getY()
            
            if CellMatrix[y][x] == True:
                ant.getDirection().rotateCW()
            else:
                ant.getDirection().rotateCCW()
            ant.moveForward()
            
            cellQueue.append([x,y])
        
        for x,y in cellQueue:
            CellMatrix[y][x] = not CellMatrix[y][x]
            redrawCell(x, y)

