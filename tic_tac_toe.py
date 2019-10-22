import pygame
import sys
import numpy as np 
import random 
from time import sleep 
pygame.init()
pygame.font.init()


width = 900
height = 900

red = (200,0,0)
dark_red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
black = (0,0,0)
white = (255,255,255)

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Tic Tac Toe")
clock = pygame.time.Clock()

 

thickness = 60

myfont = pygame.font.SysFont('Comic Sans MS', 300)
myfont2 = pygame.font.SysFont('Comic Sans MS', 100)
textsurfacex = myfont.render('X', True, blue)
posx = myfont.size('X')

textsurfaceo = myfont.render('O', True, blue)
poso = myfont.size('O')

player = 2 
opponent = 1

def create_board(): 
    return(np.array([[0, 0, 0], 
                     [0, 0, 0], 
                     [0, 0, 0]]))

def display_text(text,location_x,location_y,font,color,fontsize):
	font = pygame.font.SysFont(font,fontsize)
	textsurface = font.render(text,True,color)
	textrect = textsurface.get_rect()
	textrect.center = (location_x,location_y)
	screen.blit(textsurface,textrect)

def draw_button(text,location_x,location_y,b_width,b_height,font,color1,color2,text_color,fontsize,action):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if mouse[0]>location_x and mouse[0]<location_x + b_width and mouse[1]>location_y and mouse[1]<location_y+b_height:
		pygame.draw.rect(screen,color1,(location_x,location_y,b_width,b_height))
		if click[0]==1:
			if(action=='quit'):
				sys.exit()
			if(action=='start'):
				game_play()
			
	else:
		pygame.draw.rect(screen,color2,(location_x,location_y,b_width,b_height))
	font = pygame.font.SysFont(font,fontsize)
	textsurface = font.render(text,True,text_color)
	textrect = textsurface.get_rect()
	textrect.center = (location_x+b_width/2,location_y+b_height/2)
	screen.blit(textsurface,textrect)




def drawlines():
	pygame.draw.line(screen,red,(0,height/3),(width,height/3),thickness)
	pygame.draw.line(screen,red,(0,height*2/3),(width,height*2/3),thickness)
	pygame.draw.line(screen,red,(width/3,0),(width/3,height),thickness)
	pygame.draw.line(screen,red,(width*2/3,0),(width*2/3,height),thickness)



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
	

def game_play():
	board = create_board()
	game_over = False
	chance = 'human'
	winner = 'nothing'
	l = 1
	while True:
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
			    sys.exit() 

			if(not game_over):
				screen.fill(white)
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
				sleep(2)
				l = 2
			
			
			
			if(game_over):
				screen.fill(white)
				if(winner == 'Draw'):
					display_text('It\'s a ' + winner,width/2,height/2-50,'purisa',dark_red,75)
				else:
					display_text('Winner is ' + winner,width/2,height/2-50,'purisa',dark_red,75)
				draw_button('Start Game',width/2-225,height/2+25,200,50,'purisa',red,dark_red,white,25,'start')
				draw_button('Quit Game',width/2+25,height/2+25,200,50,'purisa',red,dark_red,white,25,'quit')

def game_intro_display():
	display_text('Tic-Tac-Toe',width/2,height/2-50,'purisa',dark_red,75)
	draw_button('Start Game',width/2-225,height/2+25,200,50,'purisa',red,dark_red,white,25,'start')
	draw_button('Quit Game',width/2+25,height/2+25,200,50,'purisa',red,dark_red,white,25,'quit')

def game_intro():
	gameintro = True
	while gameintro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
			    sys.exit()
		
		screen.fill(white)
		game_intro_display()
		pygame.display.update()
		clock.tick(10)

game_intro()
sys.exit()




