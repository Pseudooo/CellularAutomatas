'''
@author Pseudo // Mitchell
@github https://github.com/Pseudooo
@gmail mitchell.wright877@gmail.com
'''

import pygame, random 

win = pygame.display.set_mode((800,800))
pygame.display.set_caption("Game Of Life")

'''
All of the cells that are going to be displayed on the screen will be represented
by an 80x80 matrix containing boolean values. True means the cell is living, false
means that the cell is dead.
'''

# Init matrix with all dead cells
CellMatrix = [[False for i in range(80)] for j in range(80)]

def redrawCell(x:int,y:int):
    # Helper function to redraw a given cell on the screen
    if CellMatrix[y][x] == False:
        col = (0,0,0) # Black squares are dead cells
    else:
        col = (255,255,255) # White squares are living cells
    # Draw rectangle
    pygame.draw.rect(win, col, (x*10,y*10,10,10))

# Helper function to count the neighbours of a given coordinate
def countNeighbours(x:int,y:int):
    count = 0
    
    # Check left cell
    if x != 0 and CellMatrix[y][x-1]==True:
        count+=1
    
    # Check upper left cell
    if x != 0 and y != 0 and CellMatrix[y-1][x-1]==True:
        count+=1
    
    # Check upper cell
    if y != 0 and CellMatrix[y-1][x]==True:
        count+=1
    
    # Check upper right cell
    if x != 79 and y != 0 and CellMatrix[y-1][x+1]==True:
        count+=1
        
    # Check right cell
    if x != 79 and CellMatrix[y][x+1]==True:
        count+=1
        
    # Check lower right cell
    if x != 79 and y != 79 and CellMatrix[y+1][x+1]==True:
        count+=1
        
    # Check lower cell
    if y != 79 and CellMatrix[y+1][x]==True:
        count+=1
    
    # Check lower left cell
    if x != 0 and y != 79 and CellMatrix[y+1][x-1]==True:
        count+=1
    
    return count

# Simulation will not be running by default
active = False

# Primary game loop
run = True
while(run):
    pygame.time.delay(100)
    pygame.display.update()
    
    # Check Events
    for event in pygame.event.get():
        # Quit event means that the program is going to close
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # User is allowed to click to toggle a cell's state 
            x,y = pygame.mouse.get_pos() # Translate coords to matrix positions
            x,y = int(x//10),int(y//10)
            
            CellMatrix[y][x] = not CellMatrix[y][x] # Toggle the state and redraw
            redrawCell(x, y)
            
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_SPACE:
                # Space bar is pressed, toggle active state
                active = not active
                print("Simulation State is now:",active)
                
            if event.key == pygame.K_r:
                # R key will fill the space with a random assortment of cells
                print("Randomizing screen")
                for y in range(80):
                    for x in range(80):
                        if random.randint(0,3) == 2:
                            CellMatrix[y][x] = True
                        else:
                            CellMatrix[y][x] = False
                        redrawCell(x, y)
                
    if active == True:
        # If the simulation is active then it should be simulated
        
        # Queue of cells that need to be updated for simulation tick
        ToggleQueue = []
        
        for y in range(80):
            for x in range(80):
                neighbourCount = countNeighbours(x, y)
                if CellMatrix[y][x] == True:
                    # Cell is living
                    
                    # Kill cell due to overpopulation or underpopulation
                    if neighbourCount < 2 or neighbourCount > 3:
                        ToggleQueue.append([x,y])
                    
                else:
                    
                    # Create a new living cell
                    if neighbourCount == 3:
                        ToggleQueue.append([x,y])
        
        for x,y in ToggleQueue:
            CellMatrix[y][x] = not CellMatrix[y][x]
            redrawCell(x, y)

# End of game loop, program to terminate
print("Program Terminated")
pygame.quit()