# CellularAutomatas
I've decided to start working on a few cellular automatas

# Game Of Life
Conway's Game Of Life is most likely one of the most popular and well known cellular automatas (CA), the rules of this CA are:
1. Any live cell with fewer than two live neighbors dies, as if by underpopulation.
2. Any live cell with two or three live neighbors lives on to the next generation.
3. Any live cell with more than three live neighbors dies, as if by overpopulation.
4. Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.

So I've designed this in python using pygame to handle the GUI of the effect
Controls:
Clicking on a spot on the window will toggle it between dead or alive
Pressing R will fill the screen with a random arrangement of dead and living cells
Pressing Space will pause/unpause the simulation

# Langton's Ant
Langton's Ant (LA) is one of my personal favourites for cellular automatas. The rules for LA are:
1. If the ant is on a white space it will turn right, move forward by 1 space and then toggle the previous cell
2. If the ant is on a blank cell, it will turn left, move forward by 1 space and then toggle the previous cell.

Controls:
Clicking on the window will place an ant at the click
Pressing space will pause/unpause the simulation
