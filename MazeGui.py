import pygame
from pygame.locals import *
import WilsonsAlgorithm
from time import sleep

width = 120
height = 80

N, S, E, W = 1, 2, 4, 8 #Flags for encoding connection
DX =       {E:1, W:-1, N:0, S:0}
DY =       {E:0, W:0, N:-1, S:1}
OPPOSITE = {E:W, W:E, N:S, S:N}

screen = pygame.display.set_mode((width*10, height*10))
#screen = pygame.display.set_mode((300, 100))
clock = pygame.time.Clock()
BACKGROUND = (0,0,0)

def checkExit(events):
    for event in events:
        if event.type == pygame.QUIT:
            return True
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            return True
    return False

def loadTiles():
	tiles = []
	for i in range(16):
		tile = pygame.transform.scale(pygame.image.load("./maze-tiles/" + str(i) + ".png"), (10,10))
		tiles.append(tile)
	return tiles

def loadLines():
	lines = [1, 2, 4, 5, 8, 9, 3, 6, 10, 12]
	linepics = {}
	for i in lines:
		linepics[i] = pygame.transform.scale(pygame.image.load("./maze-tiles/line" + str(i) + ".png"), (10,10))
	return linepics

def mainLoop():
	maze = WilsonsAlgorithm.generate_maze(width, height)
	exiting = False
	tiles = loadTiles()
	lines = loadLines()
	path = []
	for i in range(len(maze)):
			for j in range(len(maze[i])):
				screen.blit(tiles[maze[i][j]], pygame.Rect(i*10, j*10, 10, 10))
	while not exiting:
		#screen.fill(BACKGROUND)
		events = pygame.event.get()
		path = get_key_input(path, events)
		display_path(path, lines)
		pygame.display.flip()
		exiting = checkExit(events)

def get_key_input(path, events):
	''' Takes in 'path' as a list of values: each one of which
		is 1,2,4, or 8, corresponding to Up, Down, Right, Left
	'''
	for event in events:
		if event.type == pygame.KEYDOWN:
			print "Key_pressed"
			if event.key == pygame.K_LEFT:
				path.append(W)
				print "Left"
			elif event.key == pygame.K_RIGHT:
				path.append(E)
				print "Right"
			elif event.key == pygame.K_DOWN:
				path.append(S)
				print "Down"
			elif event.key == pygame.K_UP:
				path.append(N)
				print "Up"
	return path

def display_path(path, lines):
	x, y = 0, 0
	ball = pygame.transform.scale(pygame.image.load("./maze-tiles/current_pos.png"), (10,10))
	for i, move in enumerate(path):
		if i == 0:
			screen.blit(lines[move], (0,0))
			x, y = x + DX[move], y + DY[move]
		elif i == (len(path)):
			screen.blit(OPPOSITE[lines[move]], (x*10, y*10))
		else:
			if move == OPPOSITE[path[i-1]]:
				screen.blit(lines[move], (x*10, y*10))
			else:
				screen.blit(lines[move + OPPOSITE[path[i-1]]], (x*10,y*10))
			x, y = x + DX[move], y + DY[move]
	screen.blit(ball, (x*10,y*10))


	ball = pygame.transform.scale(pygame.image.load("./maze-tiles/Ball.png"), (10,10))
	screen.blit(ball, (0,0))
	screen.blit(ball, (width*10-10, height*10-10))

mainLoop()