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
    
    col = (0,0,0) # Default colour is dead cell (Black)
    if CellMatrix[y][x] == True:
        col = (255,255,255) # If the state of the given cell is living then change to white

    # Draw the cell as a rectangle
    pygame.draw.rect(win, col, (x*10,y*10,10,10))

# Helper function to count the (living) neighbours of a given coordinate
def countNeighbours(x:int,y:int):
    
    count = 0
    for xShift in [-1,0,1]:
        for yShift in [-1,0,1]:
            
            # Skip check on self
            if xShift == 0 and yShift == 0:
                continue
            
            CheckX = x+xShift
            CheckY = y+yShift
            
            # Skip any checks that are outside of our CellMatrix range
            if CheckX == -1 or CheckX == 80 or CheckY == -1 or CheckY == 80:
                continue
            
            # Increase neighbour count if living cell found
            if CellMatrix[CheckY][CheckX]:
                count+=1
                
    return count

# Boolean to determine active state of simulation
active = False

# Primary game loop
run = True
while(run):
    pygame.time.delay(100) # Max 10fps
    pygame.display.update() 
    
    # Check Events
    for event in pygame.event.get():
        
        # Quit event means that the program is going to close
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # User is allowed to click to toggle a cell's state 
            x,y = pygame.mouse.get_pos() # Translate coords to matrix positions
            x,y = x//10,y//10
            
            CellMatrix[y][x] = not CellMatrix[y][x] # Invert the cell's state and call for a redraw
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
                        if random.randint(0,3) == 2: # one in 3 chance of being alive
                            CellMatrix[y][x] = True
                        else:
                            CellMatrix[y][x] = False
                        redrawCell(x, y)
                        
            if event.key == pygame.K_c:
                # C key will clear the board
                
                # Set CellMatrix to full false values
                CellMatrix = [[False]*80 for b in range(80)]
                win.fill((0,0,0))
                
    if active == True:
        # If the simulation is active then it should be simulated
        
        # Queue of cells that need to be updated for simulation tick
        ToggleQueue = []
        
        # Iterate through all cells in matrix
        for y in range(80):
            for x in range(80):
                neighbourCount = countNeighbours(x, y)
                if CellMatrix[y][x] == True:
                    # Cell is living
                    
                    # Act on rules 1 and 3
                    # Kill cell due to overpopulation or underpopulation
                    if neighbourCount < 2 or neighbourCount > 3:
                        # Queue cell to be toggeled
                        ToggleQueue.append((x,y))
                    
                    # Cell remains living if 2 or 3 neighbours so do nothing
                else:
                    # Cell is dead
                    
                    # Act of rule 3
                    # Birth cell with 3 neighbours
                    if neighbourCount == 3:
                        ToggleQueue.append((x,y))
        
        # Process all actions queued
        for x,y in ToggleQueue:
            # Invert and redraw queued cell
            CellMatrix[y][x] = not CellMatrix[y][x]
            redrawCell(x, y)

# End of game loop, program to terminate
print("Program Terminated")
pygame.quit()