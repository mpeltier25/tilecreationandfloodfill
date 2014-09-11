import copy, pygame
from pygame.locals import *
class Node:#credit goes here
    def __init__(self, state, parent=None, action=None, path_cost=0):#credit goes here
        "Create a search tree Node, derived from a parent by an action."
        update(self, state=state, parent=parent, action=action,#credit goes here
               path_cost=path_cost, depth=0)#credit goes here
        if parent:#credit goes here
            self.depth = parent.depth + 1#credit goes here
    def __repr__(self):#credit goes here
        return "<Node %s>" % (self.state,)#credit goes here
    def path(self):#credit goes here
        "Create a list of nodes from the root to this node."
        x, result = self, [self]#credit goes here
        while x.parent:#credit goes here
            result.append(x.parent)#credit goes here
            x = x.parent#credit goes here
        return result#credit goes here
    def expand(self, problem):
        "Return a list of nodes reachable from this node. [Fig. 3.8]"
        return [Node(next, self, act,#credit goes here
                     problem.path_cost(self.path_cost, self.state, act, next))#credit goes here
                for (act, next) in problem.successor(self.state)]#credit goes here
    #end credit
def main():
    Frames = 30
    global Screen, Tiles, Orc
    pygame.init()
    #For the screen display which is big for the imac monitors we have in class
    Screen = pygame.display.set_mode((1024, 1024))
    #Tiles which are very important. These will convert simple letters into the tiles that will be displayed onto the screen I have three regular tiles, and
    #Cliff wall, which counts as impassable terrain and I purposely made it bigger to show this.
    Tiles = {'w': pygame.image.load('images/Cliff_wall.png'),
                   'r':pygame.image.load('images/rocky_terrain.png'),
                   's': pygame.image.load('images/Sandy_terrain.png'),
                   'g': pygame.image.load('images/Grass.png')
                   }
    #Decided to make a seperate Orc variable because unlike the other tiles, this one will be moving.
    Orc = [pygame.image.load('images\orc.png')]
    #This will read tilemapedit, which you can edit so that the map appears different.
    reading = readinfile('tilemapedit.txt')
    returning = worldstate(reading)
def creatingmap(worldmap, startorcposition):
    #This will make the flood fill where ever the orc is located.
    startxposition, startyposition = startorcposition
    #The floodfill is used twice because I have two different tiles that
    #I want to write over. I made it easy to see this effect by putting
    #walls around the tiles and removing a wall and replacing it with something else because it is 30 by 30
    #means that the flood fill will affect it and turn it all into Sandy terrain.
    floodFill(worldmap, startxposition, startyposition, 'g', 'r', Node)
    floodFill(worldmap, startxposition, startyposition, 'r', 's', Node)
    return worldmap    
def worldstate(reading):
    #The world is read like an array. For my 30 by 30 world, I made it at position 0 of the array.
    world = reading[0]
    worldmap = creatingmap(world['worldmap'], world['orcposition'])
    worldstate = copy.deepcopy(world['startPosition'])
    #refreshmap is important. Without refreshmap, whenever you make a move it refreshes the map so that you can see your move on the screen.
    refreshmap = True
    #Need a while loop because you need the movement to keep going and not just stop with just one key press.
    while True:
        orcpositionmove = None
        keyPressed = False
        #This for loop is in place whenever a user presses an arrow key that it will register as well as if someone presses escape to leave or hitting the
        #x button to close the program.
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            #Tried implementing a click event that you could get the
            #character to move to the place that was clicked (the goal) that
            #I would create later, when that didn't work, I made it so that you could
            #move with the keyboard instead
            #elif event.type == MOUSEBUTTONDOWN:
                #orcpositionmove = event.pos
            elif event.type == KEYDOWN:
                keyPressed = True
                if event.key == K_UP:
                    orcpositionmove = 'up'
                elif event.key == K_DOWN:
                    orcpositionmove = 'down'
                elif event.key == K_LEFT:
                    orcpositionmove = 'left'
                elif event.key == K_RIGHT:
                    orcpositionmove = 'right'
                elif event.key == K_ESCAPE:
                    pygame.quit()
        if orcpositionmove != None:
            #Need to use return move to make the orc actually utilize movement.
            mademove = returningmove(worldmap, worldstate, orcpositionmove)
            if mademove:
                #Need to refresh the map so the move actually registers on screen.
                refreshmap = True
        if refreshmap:
            centering = makemap(worldmap, worldstate)
            #don't want to keep refreshing until the next move, so make it false.
            refreshmap = False
        centermap = centering.get_rect()
        #centering the map so that despite length it will always be centered makes it easy for edits instead of always
        #starting at the very left of the map every time.
        centermap.center = (1024 / 2, 1024 / 2)
        Screen.blit(centering, centermap)
        pygame.display.update()
#Wallblocking is used for impassable terrain.
def wallblocking(worldmap, x, y):
    #It will return true if the player tries to move into a square occupied by a wall, otherwise the player is free to move through it.
    if worldmap[x][y] in ('w'):
        return True
    return False
def makemap(worldmap, world):
    centeringWidth = len(worldmap) * 50
    centeringHeight = (len(worldmap[0]) - 1) * 40 + 85
    centering = pygame.Surface((centeringWidth, centeringHeight))
    for x in range(len(worldmap)):
        for y in range(len(worldmap[x])):
            spaceRect = pygame.Rect((x * 50, y * 40, 50, 85))
            if worldmap[x][y] in Tiles:
                baseTile = Tiles[worldmap[x][y]]
            centering.blit(baseTile, spaceRect)
            if (x, y) == world['orcposition']:
                centering.blit(Orc[0], spaceRect)
    return centering
#This will read in the file in order to create the map.
def readinfile(filename):
    #Want to open the file that will be read.
    mapfile = open(filename)
    content = mapfile.readlines() + ['\r']
    #Arrays will be useful
    reading = []
    maptext = [] 
    worldmap = [] 
    for lineNum in range(len(content)):
        line = content[lineNum].rstrip('\r\n')
        #If the line is not blank we want to append the lines with whatever is into the array.
        if line != '':
            maptext.append(line)
        elif line == '' and len(maptext) > 0:
            maxWidth = -1
            for i in range(len(maptext)):
                if len(maptext[i]) > maxWidth:
                    maxWidth = len(maptext[i])
            for x in range(len(maptext[0])):
                worldmap.append([])
            for y in range(len(maptext)):
                for x in range(maxWidth):
                    worldmap[x].append(maptext[y][x])
            for x in range(maxWidth):
                for y in range(len(worldmap[x])):
                    #Getting the orc position for x and y coordinates.
                    if worldmap[x][y] in ('o'):
                        orcxposition = x
                        orcyposition = y
            worldstate = {'orcposition': (orcxposition, orcyposition)}
            world = {'worldmap': worldmap,
                        'startPosition': worldstate,
                        'orcposition': (orcxposition, orcyposition)}
            reading.append(world)
            maptext = []
    return reading
#Having a lot of trouble figuring out how nodes work in the flood fill. I think I managed to implement the Node class, but not sure how to utilize it for
#Pathfinding purposes.
""" Credit for floodfill go to:
http://inventwithpython.com/blog/2011/08/11/recursion-explained-with-the-flood-fill-algorithm-and-zombies-and-cats/"""
def floodFill(worldmap, x, y, oldCharacter, newCharacter, Node):#credit here
    #Recursive flood fill
    if worldmap[x][y] == oldCharacter: #credit here
        worldmap[x][y] = newCharacter #credit here
    if x < len(worldmap) - 1 and worldmap[x+1][y] == oldCharacter: #credit here
        floodFill(worldmap, x+1, y, oldCharacter, newCharacter, Node)#credit here
    if x > 0 and worldmap[x-1][y] == oldCharacter:#credit here
        floodFill(worldmap, x-1, y, oldCharacter, newCharacter,Node)#credit here
    if y < len(worldmap[x]) - 1 and worldmap[x][y+1] == oldCharacter:#credit here
        floodFill(worldmap, x, y+1, oldCharacter, newCharacter,Node)#credit here
    if y > 0 and worldmap[x][y-1] == oldCharacter:#credit here
        floodFill(worldmap, x, y-1, oldCharacter, newCharacter,Node)#credit here
        #end credit
#This will return whatever move that you make for the orc on the map
def returningmove(worldmap, world, orcpositionmove):
    orcpositionx, orcpositiony = world['orcposition']
    #simple up down left and right commands
    if orcpositionmove == 'up':
        xOffset = 0
        yOffset = -1
    elif orcpositionmove == 'down':
        xOffset = 0
        yOffset = 1
    elif orcpositionmove == 'left':
        xOffset = -1
        yOffset = 0
    elif orcpositionmove == 'right':
        xOffset = 1
        yOffset = 0
    #checking if orc runs into a wall and he won't be able to pass
    if wallblocking(worldmap, orcpositionx + xOffset, orcpositiony + yOffset):
        #If it is true, he won't be able to move into that space, which makes the movement false.
        return False
    else:
        #otherwise, he is able to move just about anywhere he wants!
        world['orcposition'] = (orcpositionx + xOffset, orcpositiony + yOffset)
        return True
if __name__ == '__main__':
    main()
