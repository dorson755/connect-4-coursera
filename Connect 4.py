import numpy as np
import pygame
import math

image = pygame.image.load('pop.png')

##############################Colors##############################
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
GRAY = (128,128,128)

#############################Dimensions###########################
ROWS = 6
COLUMNS = 7
SLOT = 100
OFFSET = 100
width = COLUMNS * SLOT
height = (ROWS+1) * SLOT
size = (width, height)
RADIUS = int(SLOT/2 - 5)

game_over = False
turn = 0

##############################Functions########################### 
def is_valid_location(board, col):
       return board[ROWS-1][col] == 0

def drop_piece(board,col, piece):
       for r in range(ROWS):
              if board[r][col] == 0:
                     row = r
                     break
       board[row][col] = piece

def is_winning_move(board, piece):
       # Check horizontal locations for win
       for c in range(COLUMNS-3):
              for r in range(ROWS):
                     if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                            return True

       # Check vertical locations for win
       for c in range(COLUMNS):
              for r in range(ROWS-3):
                     if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                            return True

       # Check positively sloped diaganols
       for c in range(COLUMNS-3):
              for r in range(ROWS-3):
                     if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                            return True

       # Check negatively sloped diaganols
       for c in range(COLUMNS-3):
              for r in range(3, ROWS):
                     if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                            return True

def draw_board(board):
       pygame.draw.rect(window, GRAY, (0,0, width, SLOT))
       for c in range(COLUMNS):
              for r in range(ROWS):
                     rect = (c*SLOT, r*SLOT+OFFSET, SLOT, SLOT)
                     c1 = (int(c*SLOT+SLOT/2), int(r*SLOT+OFFSET+SLOT/2))
                     pygame.draw.rect(window, BLUE, rect)
                     pygame.draw.circle(window, GRAY, c1 , RADIUS)
       
       for c in range(COLUMNS):
              for r in range(ROWS):         
                     c2 = (int(c*SLOT+SLOT/2), height-int(r*SLOT+SLOT/2))
                     if board[r][c] == 1:
                            pygame.draw.circle(window, RED, c2, RADIUS)
                     elif board[r][c] == 2: 
                            pygame.draw.circle(window, GREEN, c2, RADIUS)
       pygame.display.update()

###########################Initializing Pygame##############################

board = np.zeros((ROWS,COLUMNS))
print(board)

pygame.init()
window = pygame.display.set_mode(size)
pygame.display.set_caption("Connect 4")

pygame.display.update()
font = pygame.font.SysFont("Comic Sans MS", 33, True)
draw_board(board)
######################### Main loop #########################################

while not game_over:

       for event in pygame.event.get():
              if event.type == pygame.QUIT:
                     pygame.quit()

              if event.type == pygame.MOUSEMOTION:
                     pygame.draw.rect(window, GRAY, (0,0, width, SLOT))
                     posx = event.pos[0]
                     if turn % 2 == 0:
                            pygame.draw.circle(window, RED, (posx, int(SLOT/2)), RADIUS)
                     else: 
                            pygame.draw.circle(window, GREEN, (posx, int(SLOT/2)), RADIUS)
              pygame.display.update()

              if event.type == pygame.MOUSEBUTTONDOWN:
                     #print(event.pos)
                     # Ask for Player 1 Input
                     if turn % 2 == 0:
                            posx = event.pos[0]
                            col = math.floor(posx/SLOT)

                            if is_valid_location(board, col):
                                   drop_piece(board,col,1)

                                   if is_winning_move(board, 1):
                                          label = font.render("PLAYER 1 WON!", True, RED)
                                          game_over = True
                            else:
                                   turn -= 1

                     # # Ask for Player 2 Input
                     else:                       
                            col = event.pos[0]
                            col = int(math.floor(col/SLOT))

                            if is_valid_location(board, col):
                                   drop_piece(board, col, 2)
                                   if is_winning_move(board, 2):
                                          label = font.render("PLAYER 2 WON!", True, GREEN)
                                          game_over = True
                            else:
                                   turn -= 1;
                     print(np.flip(board,0))
                     draw_board(board)
                     turn += 1
                     if game_over:
                            window.blit(image,(120,220))
                            window.blit(label,(170,350))
                            pygame.display.update()
                            pygame.time.wait(2000)
