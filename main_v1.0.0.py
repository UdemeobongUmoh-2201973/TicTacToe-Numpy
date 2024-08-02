import pygame
pygame.init()

import numpy as np
from random import choice

#Pygame Variables

Size = (800,600)

Screen = pygame.display.set_mode(Size)
pygame.display.set_caption("Tic Tac Toe: Numpy")

Clock = pygame.time.Clock()
fps = 30

MousePos = pygame.mouse.get_pos()

app = True

#Path for Resources

player_pieces = "res/images/player_pieces"
player_logopath = "res/images/icons/player_logo.png"
AI_logopath = "res/images/icons/AI_logo.png"

icon_path = pygame.display.set_icon(pygame.image.load("res/images/icons/icon.png").convert())

#Functions

def empty_board():
    board = np.array([
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ])
    return(board)

def empty_places(board):
    l = []

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0:
                l.append((i,j))
    return(l)

def row_winner(board, player):
    # Checks whether the player has three of their marks in a horizontal row

    for x in range(len(board)):
        win = True

        for y in range(len(board)):
            if board[x, y] != player:
                win = False
                continue

        if win == True:
            return(win)
    return(win)

def col_winner(board, player):
# Checks whether the player has three of their marks in a vertical row
  
    for x in range(len(board)):
        win = True

        for y in range(len(board)):
            if board[y][x] != player:
                win = False
                continue

        if win == True:
            return(win)
    return(win)

def diag_winner(board, player):
    # Check the diagnal rows for a winner

    win = True
    y = 0
    for x in range(len(board)):
        if board[x, x] != player:
                        win = False

    if win:
        return win

    win = True
    if win:
        for x in range(len(board)):
            y = len(board) - 1 - x
            if board[x, y] != player:
                win = False
    return win

def evaluate_game(board,players):
    # Evaluates Whether there is a winner or a Tie
    # Winner [0 = indecisive; 1 = Player 1; 2 = Player 2; -1 = Tie]
    winner = 0
    for player in players:
        if (row_winner(board, player) or
            col_winner(board, player) or
            diag_winner(board, player)):
            winner = player

    if np.all(board != 0) and winner == 0:
        winner = -1
    
    return winner

#Classes

class TicTacToe(object):
    def __init__(self,board_pos,size) -> None:
        self.board = empty_board()
        self.board_pos = board_pos
        self.size = size
        self.user_num = 1
        self.AI_num = 2

        self.user_score = 0
        self.AI_score = 0

    def place_piece(self,pos,player_number):
        if self.board[pos[0],pos[1]] == 0:
            self.board[pos[0],pos[1]] = player_number
            
    def user_input(self):
       
        for i in range(3):
            for j in range(3):
                rectX = self.board_pos[0]-(self.size/2)+(self.size*3*j/10)+(self.size*(j-0)/20)
                rectY = self.board_pos[1]-(self.size/2)+(self.size*3*i/10)+(self.size*(i-0)/20)

                if rectX < MousePos[0] < rectX + (self.size*3/10):
                    if rectY < MousePos[1] < rectY + (self.size*3/10):
                        self.place_piece([i,j],self.user_num)
                    
    def ai_input(self):
        if len(empty_places(self.board)) > 0:
            random_choice = choice(empty_places(self.board))
            self.board[random_choice] = self.AI_num

    def check_winner(self):
        winner = evaluate_game(self.board,[self.AI_num,self.user_num])
        if winner==self.user_num:
            self.user_score += 1
            self.reset_board()

        elif winner == self.AI_num:
            self.AI_score += 1
            self.reset_board()

        elif winner == -1:
            self.reset_board()

    def get_playerpiece(self,player_num):
        if player_num == self.user_num:
            return "X"
        elif player_num == self.AI_num:
            return "O"

    def draw_board(self):
        
        size = self.size
        board_pos = self.board_pos

        for i in range(3-1):
            rectY = board_pos[1] - (size/2)
            for j in range(3-1):
                rectX = board_pos[0]-(size/2)+(size*3*(i+1)/10)+(size*(i)/20)
                
                pygame.draw.rect(Screen,(255,255,255),[int(rectX),int(rectY),int(size/20),int(size)])

        for j in range(3-1):
            rectX = board_pos[0] - (size/2)
            for i in range(3-1):
                rectY = board_pos[1]-(size/2)+(size*3*(j+1)/10)+(size*(j)/20)
                
                pygame.draw.rect(Screen,(255,255,255),[rectX,rectY,size,size/20])

        for i in range(3):
            for j in range(3):
                imgPos =[board_pos[0]-(size/2)+(size*3*j/10)+(size*(j-0)/20),board_pos[1]-(size/2)+(size*3*i/10)+(size*(i-0)/20)]
                if self.board[i,j] != 0:
                    Screen.blit(pygame.transform.scale(pygame.image.load(f"{player_pieces}/white/{self.get_playerpiece(self.board[i,j])}.png").convert(),(size*3/10,size*3/10)),imgPos)

    def show_scoreboard(self,y_pos,x_dist,height):
        Screen.blit(pygame.transform.scale(pygame.image.load(player_logopath),(height,height)),(self.board_pos[0]-x_dist/2,y_pos-height/2))
        Screen.blit(pygame.transform.scale(pygame.image.load(AI_logopath),(height,height)),(self.board_pos[0]+x_dist/2-height,y_pos-height/2))

        font = "Courier New"

        self.PlayerScoreText = pygame.font.SysFont(font,height).render(str(self.user_score),True,(255,255,255))
        self.AIScoreText = pygame.font.SysFont(font,height).render(str(self.AI_score),True,(255,255,255))

        self.PlayerScoreTextPos = [int(self.board_pos[0]+height*6/5-x_dist/2),int(y_pos-height/2)]
        self.AIScoreTextPos = [int(self.board_pos[0]-height*6/5+x_dist/2-self.AIScoreText.get_width()),int(y_pos-height/2)]

        Screen.blit(self.PlayerScoreText,self.PlayerScoreTextPos)
        Screen.blit(self.AIScoreText,self.AIScoreTextPos)

    def draw(self):
        self.draw_board()
        self.show_scoreboard(int(Size[0]/24),int(Size[0]*39/40),int(Size[1]/12))

    def reset_board(self):
        self.board = empty_board()

        pygame.draw.rect(Screen,(0,0,0),(self.board_pos[0]-(self.size/2),self.board_pos[1]-(self.size/2),self.size,self.size))
        pygame.draw.rect(Screen,(0,0,0),(self.PlayerScoreTextPos[0],self.PlayerScoreTextPos[1],self.PlayerScoreText.get_width(),self.PlayerScoreText.get_height()))
        pygame.draw.rect(Screen,(0,0,0),(self.AIScoreTextPos[0],self.AIScoreTextPos[1],self.AIScoreText.get_width(),self.AIScoreText.get_height()))


Game1 = TicTacToe((Size[0]/2,Size[1]*7/12),Size[1]*7/12)

while app:

    MousePos = pygame.mouse.get_pos()
    Game1.draw()


    pygame.display.update()
    Clock.tick(fps)

    for event in pygame.event.get():  
        if event.type == pygame.QUIT:
            app = False
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN: 
            Game1.user_input()
            Game1.ai_input()
            Game1.check_winner()


    if app == False:
        pygame.quit()
        quit()
