# importing the required libraries
import pygame, sys, time

pygame.init()
red = pygame.Color(255,0,0)
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
pygame.display.set_caption('Tic Tac Toe AI')
width, height = 400,400
game_window = pygame.display.set_mode((width, height))

player = "X"
board = [0]*16

x_img = pygame.image.load("X_img.png")
y_img = pygame.image.load("O_img.png")
x_img = pygame.transform.scale(x_img, (86, 86))
o_img = pygame.transform.scale(y_img, (86, 86))

fps_controller = pygame.time.Clock()

game_window.fill(white)

pygame.draw.line(game_window, black, (width/4, 0), (width/4, height), 7)
pygame.draw.line(game_window, black, (width/4 * 2, 0), (width/4 * 2, height), 7)
pygame.draw.line(game_window, black, (width/4 * 3, 0), (width/4 * 3, height), 7)

pygame.draw.line(game_window, black, (0, height/4), (width, height/4), 7)
pygame.draw.line(game_window, black, (0, height/4 * 2), (width, height/4 * 2), 7)
pygame.draw.line(game_window, black, (0, height/4 * 3), (width, height/4 * 3), 7)

pygame.display.update()

# 3 in a row
#[0,1,2],[1,2,3],[4,5,6],[5,6,7],[8,9,10],[9,10,11],[12,13,14],[13,14,15],[0,4,8],[4,8,12],[1,5,9],[5,9,13],[2,6,10],[6,10,14],[3,7,11],[7,11,15],[2,5,8],[3,6,9],[6,9,12],[7,10,13],[1,6,11],[0,5,10],[5,10,15],[4,9,14]

def evaluate(board, turn):
    for pos in ([0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15],[0,4,8,12],[1,5,9,13],[2,6,10,14],[3,7,11,15],[0,5,10,15],[3,6,9,12]):
        if board[pos[0]] == board[pos[1]] == board[pos[2]] == board[pos[3]] == turn: 
            return True
        
# AI
TRANSPOSITION_TABLE = {}

def store(table, board, alpha, beta, best, depth):
    if best[1] <= alpha:
        flag = 'UPPERCASE'
    elif best[1] >= beta:
        flag = 'LOWERCASE'
    else:
        flag = 'EXACT'

    table[str(board)] = [best, flag, depth]

def negamax(board, depth, turn, alpha, beta):
    alpha_org = alpha
    # Transposition tabel look up
    if str(board) in TRANSPOSITION_TABLE:
        tt_entry = TRANSPOSITION_TABLE[str(board)]
        if tt_entry[2] >= depth:
            if tt_entry[1] == 'EXACT':
                return tt_entry[0]
            elif tt_entry[1] == 'LOWERCASE':
                alpha = max(alpha, tt_entry[0][1])
            elif tt_entry[1] == 'UPPERCASE':
                beta = min(beta, tt_entry[0][1])

        if alpha >= beta:
            return tt_entry[0]
    
    if evaluate(board, turn): return 0, (16+depth)  # Return positive score if maximizing player
    if evaluate(board, -turn): return 0, -(16+depth)  # Return negative score if minimizing player wins
    if 0 not in board: return 0, 0  # Drawn game, return 0
    
    best_score = -2000
    
    for move in [i for i in range(16) if not board[i]]:  # Go through all empty squares on board
        board[move] = turn  # Make move
        score = -negamax(board, depth - 1, -turn, -beta, -alpha)[1]  # Recursive call to go through all child nodes
        board[move] = 0  # Unmake the move
        alpha = max(alpha,score)
        if score > best_score:
            best_score, best_move = score, move  # If score is larger than previous best, update score
        if alpha >= beta:
            break
    
    store(TRANSPOSITION_TABLE, board, alpha_org, beta, [best_move,best_score], depth)
    
    return best_move, best_score  # Return the best move and its corresponding score
       
def game_over(player):
    game_window.fill(black)
    my_font = pygame.font.SysFont('times new roman', 40)
    game_over_surface = my_font.render(f'{player} WINS', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (width/2, height/4)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    sys.exit()
    
def game_over_draw():
    game_window.fill(black)
    my_font = pygame.font.SysFont('times new roman', 40)
    game_over_surface = my_font.render(f'Draw', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (width/2, height/4)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    sys.exit()

def make_move(player,move,posx,posy):
    global board
    
    if player == "X":
        game_window.blit(x_img, (posy,posx))
        pygame.display.update()
        board[move] = 1
        if evaluate(board,1):
            time.sleep(0.1)
            print("Game Over, X wins.")
            game_over("X")
    else:
        game_window.blit(o_img, (posy,posx))
        pygame.display.update()
        board[move] = -1
        if evaluate(board,-1):
            time.sleep(0.1)
            print("Game Over, O wins.")
            game_over("O")
    
    if 0 not in board:
        game_over_draw()
        

current_player = 1
while True:
    for event in pygame.event.get():

      # if user types QUIT then the screen will close
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN and current_player == 1:
            
            mouseX, mouseY = pygame.mouse.get_pos()
            column, row = 0, 0
            
            # Human Move
            if mouseY > 100:
                column = 1
                if mouseY > 200:
                    column = 2
                    if mouseY > 300:
                        column = 3
                    
            if mouseX > 100:
                row = 1
                if mouseX > 200:
                    row = 2
                    if mouseX > 300:
                        row = 3
            
            posy = row*100 + 7
            posx = column*100 + 7
            
            move = row + column*4
            
            if board[move] ==  0:
                make_move("X",move,posx,posy)
                current_player = -1
                            
        # AI Move
        if current_player == -1:
            starttime = time.time()
            ai_move = negamax(board, 16, -1, -10000, 10000)[0]
            print("Time taken to generate move:",time.time()-starttime)
                
            if ai_move == 0:
                ai_row, ai_column = 0, 0
            if ai_move == 1:
                ai_row, ai_column = 1, 0
            if ai_move == 2:
                ai_row, ai_column = 2, 0
            if ai_move == 3:
                ai_row, ai_column = 3, 0
            if ai_move == 4:
                ai_row, ai_column = 0, 1
            if ai_move == 5:
                ai_row, ai_column = 1, 1
            if ai_move == 6:
                ai_row, ai_column = 2, 1
            if ai_move == 7:
                ai_row, ai_column = 3, 1
            if ai_move == 8:
                ai_row, ai_column = 0, 2
            if ai_move == 9:
                ai_row, ai_column = 1, 2
            if ai_move == 10:
                ai_row, ai_column = 2, 2
            if ai_move == 11:
                ai_row, ai_column = 3, 2
            if ai_move == 12:
                ai_row, ai_column = 0, 3
            if ai_move == 13:
                ai_row, ai_column = 1, 3
            if ai_move == 14:
                ai_row, ai_column = 2, 3
            if ai_move == 15:
                ai_row, ai_column = 3, 3

            ai_posy = ai_row*100 + 7
            ai_posx = ai_column*100 + 7

            make_move("O",ai_move,ai_posx,ai_posy)
            current_player = 1
                
    pygame.display.update()
    fps_controller.tick(30)
