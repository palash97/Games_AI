import pygame
import sys
import numpy as np 
import random 
from time import sleep 
pygame.init()
pygame.font.init()


width = 900
height = 900

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
black = (0,0,0)

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Tic Tac Toe")
clock = pygame.time.Clock()

game_over = False 

thickness = 60

myfont = pygame.font.SysFont('Comic Sans MS', 300)
myfont2 = pygame.font.SysFont('Comic Sans MS', 100)
textsurfacex = myfont.render('X', False, blue)
posx = myfont.size('X')

textsurfaceo = myfont.render('O', False, blue)
poso = myfont.size('O')

player = 2 
opponent = 1

def drawlines():
	pygame.draw.line(screen,red,(0,height/3),(width,height/3),thickness)
	pygame.draw.line(screen,red,(0,height*2/3),(width,height*2/3),thickness)
	pygame.draw.line(screen,red,(width/3,0),(width/3,height),thickness)
	pygame.draw.line(screen,red,(width*2/3,0),(width*2/3,height),thickness)

def create_board(): 
    return(np.array([[0, 0, 0], 
                     [0, 0, 0], 
                     [0, 0, 0]]))

def map_mouse_to_board(x, y):
    if x < width / 3- thickness/2:
        column = 0
    elif width / 3 + thickness/2 <= x < (width / 3) * 2 - thickness/2:
        column = 1
    else:
        column = 2
    if y < height / 3 - thickness/2:
        row = 0
    elif height / 3  + thickness/2<= y < (height / 3) * 2 -thickness/2:
        row = 1
    else:
        row = 2
    return column, row

def drawX(x,y):
	screen.blit(textsurfacex,((2*x+1)*width/6 -posx[0]/2,(2*y+1)*height/6-posx[1]/2))

def drawO(x,y):
	screen.blit(textsurfaceo,((2*x+1)*width/6 -poso[0]/2,(2*y+1)*height/6-poso[1]/2))

def evaluate(board):
    for row in range(0,3):
        if(board[row][0]==board[row][1] and board[row][1]==board[row][2]):
            if(board[row][0]==player):
                return 10
            elif(board[row][0]==opponent):
                return -10
  
    for col in range(0,3): 
        if(board[0][col]==board[1][col] and  board[1][col]==board[2][col]):
            if (board[0][col]==player):
                return +10
  
            elif (board[0][col]==opponent):
            	return -10
  
    if(board[0][0]==board[1][1] and board[1][1]==board[2][2]):
        if(board[0][0]==player):
            return +10
        elif(board[0][0]==opponent):
            return -10
  
    if(board[0][2]==board[1][1] and board[1][1]==board[2][0]):
        if (board[0][2]==player):
            return +10
        elif (board[0][2]==opponent):
            return -10 

    return 0

def checkgameover(board):
	for i in range(0,3):
		for j in range(0,3):
			if(board[i][j]==0):
				return False
	return True

def minimaxValue(board , ismaximizing):
	value = evaluate(board)
	if(value == 10):
		return 10
	if(value == -10):
		return -10
	if(checkgameover(board)==True):
		return 0


	if(ismaximizing):
		maxvalue = -1000
		currmaxvalue = -1000
		for i in range(0,3):
			for j in range(0,3):
				if(board[i][j]==0):
					board[i][j]=2
					currmaxvalue = minimaxValue(board,False)
					if(currmaxvalue > maxvalue):
						maxvalue = currmaxvalue
					board[i][j]=0
		return maxvalue
	else:
		minvalue = 1000
		currminvalue = 1000
		for i in range(0,3):
			for j in range(0,3):
				if(board[i][j]==0):
					board[i][j]=1
					currminvalue = minimaxValue(board,True)
					if(currminvalue < minvalue):
						minvalue = currminvalue
					board[i][j]=0
		return minvalue


def best_move(board):
    value = -1000
    currentvalue = -1000
    bestmove = (-1,-1)
    for i in range(0,3):
    	for j in range(0,3):
    		if(board[i][j]==0):
    			board[i][j] = 2
    			currentvalue = minimaxValue(board , False)
    			if(currentvalue > value):
    				value = currentvalue
    				bestmove = (i,j)
    			board[i][j] = 0
    board[bestmove[0]][bestmove[1]] = 2
    return board 
	



board = create_board()

chance = 'human'
winner = 'nothing'
l = 1
while True:
	for event in pygame.event.get():

		if event.type == pygame.QUIT:
		    sys.exit() 

		if(not game_over):
			drawlines()

			if(chance == 'human' and not game_over):
				if event.type is pygame.MOUSEBUTTONDOWN :
					(mouseX, mouseY) = pygame.mouse.get_pos()
					(row, column) = map_mouse_to_board(mouseX, mouseY)
					board[row][column] = 1
					score = evaluate(board)
					if(score==-10):
						game_over = True
						winner = 'User'
					chance = 'computer'

		

			for x in range(0,3):
				for y in range(0,3):
					if(board[x][y]==1):
						drawX(x,y)
					if(board[x][y]==2):
						drawO(x,y)
			
			if(checkgameover(board)):
				game_over = True
				if(winner == 'nothing'):
					winner = 'Draw'
			
			if(chance == 'computer' and not game_over):
				best_move(board)
				chance = 'human'

			score = evaluate(board)
			if(score==10):
				winner = 'Palash\'s AI'
				game_over=True

			if(checkgameover(board)):
				game_over = True
				if(winner == 'nothing'):
					winner = 'Draw'
		    
			for x in range(0,3):
				for y in range(0,3):
					if(board[x][y]==1):
						drawX(x,y)
					if(board[x][y]==2):
						drawO(x,y)

		pygame.display.update()
		
		if(game_over and l==1):
			sleep(5)
			l = 2
		
		screen.fill(black)
		
		if(game_over):
			if(winner == 'Draw'):
				textsurface = myfont2.render('It\'s a ' + winner, False, blue)
				posw = myfont2.size('It\'s a ' + winner)
			else:
				textsurface = myfont2.render('Winner is ' + winner, False, blue)
				posw = myfont2.size('Winner is ' + winner)
			screen.blit(textsurface,(width/2-posw[0]/2,height/2-posw[1]/2))




