import pygame
import random as rand
from GameOfLife import redrawCell

# Define ant class to make handling numerous ants easier
class Ant():
    # Initialize the ant with a direction and position
    def __init__(self,x,y,xVel,yVel):
        self.pos = (x,y)
        self.vel = (xVel,yVel)
    
    def getDirection(self): # Get the direction of the ant
        return self.vel
    
    def setDirection(self, xVel,yVel):
        self.vel = (xVel,yVel)
        
    def getPosition(self):
        return self.pos
    
    def setPosition(self,x,y):
        self.pos = (x,y)
        
    def moveForward(self):
        x,y = self.pos
        xVel,yVel=self.vel
        
        # Move by current vel
        x+=xVel
        y+=yVel
        
        # make edges of screen wrap around
        x%=80
        y%=80
            
        # Update ant pos
        self.pos = (x,y)
        
# Create the cell matrix
CellMatrix = [[False for a in range(80)] for b in range(80)]

win = pygame.display.set_mode((800,800))
pygame.display.set_caption("Langton's Ant")

def drawAnt(ant:Ant):
    # Draw the ant on the screen
    x,y=ant.getPosition()
    pygame.draw.rect(win, (255,0,0), ((x*10)+3,(y*10)+3, 4,4))
    
def redrawCell(x:int, y:int):
    # Default state of the cell is black
    col = (0,0,0)
    if CellMatrix[y][x] == True: # If true cell is white
        col = (255,255,255)
    
    # Draw cell
    pygame.draw.rect(win, col, (x*10,y*10,10,10))

# The state of activity for the simulation
active = False

# Keep track of all ants that are on the screen
Ants = []

# Main game loop
run = True
while(run):
    # Update display for next simulation tick
    #pygame.time.delay(100)
    pygame.display.update()
    
    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            x,y=int(x//10),int(y//10)
            
            NewAnt = Ant(x,y,0,1)
            Ants.append(NewAnt)
            drawAnt(NewAnt)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                active = not active
                print('Active set to: '+str(active))
                
            elif event.key == pygame.K_r:
                print("Random filling board space")
                CellMatrix = [[(rand.randint(0,2)==1 and True or False) for x in range(80)] for y in range(80)]
                [[redrawCell(x, y) for x in range(80)] for y in range(80)]
                
            elif event.key == pygame.K_c:
                print("Clearing board space")
                CellMatrix = [[False for x in range(80)] for y in range(80)]
                Ants.clear()
                win.fill((0,0,0))
    
    if active == True:
        # Simulation is active
        
        # Queue all cells to be inverted and redrawn after frame
        cellQueue = []
            
        for ant in Ants:
            # Loop through each ant on the screen
            x,y = ant.getPosition()
            xVel,yVel = ant.getDirection()
            
            # If white cell turn left if black turn right
            if CellMatrix[y][x] == True:
                xVel,yVel = yVel,-xVel
            else:
                xVel,yVel= -yVel,xVel
                
            # Update velocity and moveforwad
            ant.setDirection(xVel,yVel)
            ant.moveForward()
            # Queue cell update
            cellQueue.append([x,y])
            
        # Register all cell updates
        for x,y in cellQueue:
            CellMatrix[y][x] = not CellMatrix[y][x]
            redrawCell(x, y)
            
        # Redraw all ants in the new frame
        for ant in Ants:
            drawAnt(ant) # Call for each ant too be redrawn
            # Previous frame ants don't matter as the cell updates overlap them

