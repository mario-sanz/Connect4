import numpy as np
import pygame
import sys
import math

ROW_COUNT = 6
COLUMN_COUNT = 7
BLUE = (0,0,255) # blue color for the screen
BLACK = (0,0,0) # black color for the screen
RED = (255,0,0) # red color for the tiles of player 1
YELLOW = (255,255,0) # yellow color for the tiles of player 2

def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT)) # creo una matriz 6x7 rellena de ceros
    return board;


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0 # está la columna vacía?


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r # la funcion nos devuelve la primera fila que esté vacía


def print_board(board):
    print(np.flip(board, 0)) # revierte el board desde el eje 0


def winning_move(board, piece):
    # Comprobar posibilidades HORIZONTALES
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

    # Comprobar posibilidades VERTICALES
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

    # Comprobar posibilidades DIAGONALES CON PENDIENTE POSITIVA
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Comprobar posibilidades DIAGONALES CON PENDIENTE NEGATIVA
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True



def draw_board(board):
    # dibujo del tablero y agujeros vacios
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
            

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1: # dibujar fichas 1
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2: # dibujar fichas 2
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)

    pygame.display.update()


board = create_board()
print_board(board)
game_over = False
turn = 0

# GRAPHICAL INTERFACE
pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size) # creates the window
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # dibuja la ficha arriba moviendose antes de caer
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE)) # borra la anterior ficha moviendose
            posx = event.pos[0]
            if turn == 0: # jugador 1
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else: # jugador 2
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE)) # borra la anterior ficha moviendose
            #print(event.pos) # esto nos imprime en consola las coordenadas de donde pinchamos
            # Input del PRIMER jugador
            if turn == 0:
                posx = event.pos[0] # pos[0] indica el eje x de las coordenadas
                col = int(math.floor(posx/SQUARESIZE)) # esto nos da el numero de la columna que pulsamos
                
                if is_valid_location(board, col):
                    row = get_next_open_row(board,col)
                    drop_piece(board, row, col, 1) # las fichas del jugador 1 siempre son 1

                    if winning_move(board, 1):
                        label = myfont.render("JUGADOR 1 GANA", 1, RED)
                        screen.blit(label, (40,10))
                        game_over = True

            # Input del SEGUNDO jugador
            else:
                posx = event.pos[0] # pos[0] indica el eje x de las coordenadas
                col = int(math.floor(posx/SQUARESIZE)) # esto nos da el numero de la columna que pulsamos

                if is_valid_location(board, col):
                    row = get_next_open_row(board,col)
                    drop_piece(board, row, col, 2) # las fichas del jugador 2 siempre son 2

                    if winning_move(board, 2):
                        label = myfont.render("JUGADOR 2 GANA", 1, YELLOW)
                        screen.blit(label, (40,10))
                        game_over = True

            # TABLERO
            print_board(board)
            draw_board(board)

            # ALTERNANCIA DE TURNOS
            turn += 1
            turn = turn % 2 # el turno va a alternar entre 0 y 1

            if game_over:
                pygame.time.wait(3000) # espera 3 segundos antes de cerrarse la ventana

