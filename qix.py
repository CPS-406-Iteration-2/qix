from pygame.constants import K_x, VIDEOEXPOSE, VIDEORESIZE
import pygame.display;
import time;
import pygame.color;
from pygame.locals import *
import pygame.event;
import sys

from board import Board
from boardObjects import Marker, Qix, Sparx

pygame.display.init()
fps = 30
fpsclock=pygame.time.Clock()

# Surface drawn on is 160 by 100 pixels, scaled to 1280 by 800 pixels
mysurface = pygame.display.set_mode((1280, 800), pygame.RESIZABLE)
resized = pygame.transform.scale(mysurface, (160, 100))

pygame.display.update()

# level = int(input("Enter the you the Level you wish to play [1-3]: "))
# print("Entering Level {}...".format(level))

print("Creating Board...")

board = Board(80,94,1,1,False)
board.gameStart()
board.createEntities(1)

print("Start!")

# player = pygame.Rect(320,439,25,25)
playerRect = board.getMarker().theRect
board.getMarker().updateLocation(playerRect.x, playerRect.y)

running = True
while running:

    fpsclock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        if event == VIDEORESIZE:
            mysurface = pygame.display.set_mode((event.w,event.h), pygame.RESIZABLE)


    keys = pygame.key.get_pressed()
    # TODO: This vector should be either: (1,0), (0,1), or (0,0)
    moveVector = (playerRect.x + (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]), playerRect.y + (keys[pygame.K_DOWN] - keys[pygame.K_UP]))
    
    # Check if it can move on a valid edge
    if moveVector in board.playableEdge:
        playerRect.x = moveVector[0]
        playerRect.y = moveVector[1]

        board.getMarker().setIsPushing(False)
        # Add all pixels that appear in that buffer and add it to captured space

    if not board.getMarker().isPushing() and board.edgesBuffer:
        board.updateEdges()
        board.updatePlayable()

    # Press Spacebar in order start an incursion
    if moveVector in board.uncaptured and (keys[pygame.K_SPACE] or board.getMarker().isPushing()):
        playerRect.x = moveVector[0]
        playerRect.y = moveVector[1]

        board.edgesBuffer.append((playerRect.x, playerRect.y))
        board.uncaptured.remove((playerRect.x, playerRect.y))

        board.getMarker().setIsPushing(True)

    board.getMarker().updateLocation(playerRect.x, playerRect.y)
    board.draw()

