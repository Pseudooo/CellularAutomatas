import pygame
import random as r

'''
In order to represent empty cells, predators and prey items on the screen a matrix will be used
containing integer values
0 = Empty Cell
1 = Prey
2 = Predator
'''


# Populate CellMatrix with empty cells for init
CellMatrix = [[0 for a in range(80)] for b in range(80)]

win = pygame.display.set_mode((800,800))
pygame.display.set_caption("Predator and Prey")

'''
Setup some helper function
'''

PreyCells = set([])
PredatorCells = set([])

def getNeighbours(x:int, y:int, CellType:int):
    
    neighbours = []
    
    for xShift in [-1,0,1]:
        for yShift in [-1,0,1]:
            # Skip checking the parent cell
            if xShift == 0 and yShift == 0:
                continue
            
            CheckX,CheckY=x+xShift,y+yShift
            
            # Make check ignore window bounds and loop around
            if CheckX == -1:
                CheckX = 79
            elif CheckX == 80:
                CheckX = 0
            if CheckY == -1:
                CheckY = 79
            elif CheckY == 80:
                CheckY = 0
            
            if CellMatrix[CheckY][CheckX] == CellType:
                # If the cell is empty coord pair appended to list
                neighbours.append([CheckX,CheckY]) 
            
    # Return the list of coorindate pairs
    return neighbours

def redrawCell(x:int, y:int):
    
    col = (0,0,0)
    if CellMatrix[y][x] == 1:
        col = (0,0,255)
    elif CellMatrix[y][x] == 2:
        col = (255,0,0)
    
    pygame.draw.rect(win, col, (x*10,y*10,10,10))
    

simulating = False
run = True
while(run):
    pygame.display.update()
    #pygame.time.delay(100)
    
    for event in pygame.event.get():
        
        # Quit event break loop
        if event.type == pygame.QUIT:
            run = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Mouse button pushed
            x,y = pygame.mouse.get_pos()
            x,y = int(x//10),int(y//10)
            if CellMatrix[y][x] == 0:
                # Cell is becoming a prey cell
                PreyCells.add((x,y))
            elif CellMatrix[y][x] == 1:
                # Cell is becoming predator
                PreyCells.remove((x,y))
                PredatorCells.add((x,y))
            else:
                # Cell is becoming empty
                PredatorCells.remove((x,y))
            
            # Increase value of cell
            CellMatrix[y][x]+=1
            if CellMatrix[y][x] == 3:
                # Reset to 0 at end of possible values
                CellMatrix[y][x] = 0
                
            # Call for cell to be redrawn with new state
            redrawCell(x, y)
            
            print("Prey Cells:",PreyCells)
            print("Predator Cells:",PredatorCells)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                simulating = not simulating
                print("Simulation State:",simulating)
                
    if simulating == True:
        # Simulation is active
        
        actionQueue = set([])
        
        for PreyX,PreyY in PreyCells:
            
            # 30% chance of prey cell randomly dying
            if r.randint(0,10) > 3:
                actionQueue.add((PreyX,PreyY,0))
                continue
            
            # Get all empty cell neighbours
            neighbours = getNeighbours(PreyX, PreyY, 0)
            
            # Loop through each empty neighbour
            for neighbourX,neighbourY in neighbours:
                action = (neighbourX,neighbourY,1)
                
                # If action isn't already queued, queue it
                if not action in actionQueue:
                    actionQueue.add(action)
                    #print("Appended")
    
        for PredX,PredY in PredatorCells:
            
            # 10% chance of predator randomly dying
            if r.randint(0,10) == 3:
                actionQueue.add((PredX,PredY,0))
            
            # Get all prey neighbours
            neighbours = getNeighbours(PredX, PredY, 1)
            
            # If a predator has not eaten it dies
            eaten = False
            
            for neighbourX,neighbourY in neighbours:
                action = (neighbourX,neighbourY,2)
                
                if not action in actionQueue:
                    # Predator has now eaten and queue the action
                    actionQueue.add(action)
                    eaten = True
            
            if eaten == False:
                # Kill the predator if it hasn't eaten
                actionQueue.add((PredX,PredY,0))
        
        for x,y,val in actionQueue:
            
            # perform all queued actions
            
            # Unlist any prior predator/prey cels
            if CellMatrix[y][x] == 1:
                PreyCells.remove((x,y))
            elif CellMatrix[y][x] == 2:
                PredatorCells.remove((x,y))
                
            # List any new predator/prey cells
            if val == 1:
                PreyCells.add((x,y))
            elif val == 2:
                PredatorCells.add((x,y))
            
            CellMatrix[y][x] = val
            redrawCell(x, y)
              
        
pygame.quit()
print("Simulation Terminated")
