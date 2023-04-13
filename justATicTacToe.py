import pygame
import sys
from pygame import font

pygame.init()

FONT = font.SysFont('calibri', 50, bold=True)

WINDOW_SIZE = (500, 500)
screen = pygame.display.set_mode(WINDOW_SIZE)

pygame.display.set_caption("justA Tic Tac Toe (Level Impossible)")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

FONT = pygame.font.Font(None, 50)

GRID_SIZE = 3
CELL_SIZE = WINDOW_SIZE[0] // GRID_SIZE

PLAYER_MARKER = 'X'
COMPUTER_MARKER = 'O'

board = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def draw_board():
    screen.fill(WHITE)
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_SIZE[1]))
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WINDOW_SIZE[0], i * CELL_SIZE))
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == PLAYER_MARKER:
                pygame.draw.line(screen, RED, (col * CELL_SIZE + 20, row * CELL_SIZE + 20), (col * CELL_SIZE + CELL_SIZE - 20, row * CELL_SIZE + CELL_SIZE - 20), 5)
                pygame.draw.line(screen, RED, (col * CELL_SIZE + CELL_SIZE - 20, row * CELL_SIZE + 20), (col * CELL_SIZE + 20, row * CELL_SIZE + CELL_SIZE - 20), 5)
            elif board[row][col] == COMPUTER_MARKER:
                pygame.draw.circle(screen, BLUE, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 20, 5)

def check_winner():
    for row in range(GRID_SIZE):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] != ' ':
            return board[row][0]
    for col in range(GRID_SIZE):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != ' ':
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return board[0][2]
    if all(board[row][col] != ' ' for row in range(GRID_SIZE) for col in range(GRID_SIZE)):
        return 'Tie'
    return None



def check_game_over():
    winner = check_winner()
    if winner is not None:
        return True
    if all(board[row][col] != ' ' for row in range(GRID_SIZE) for col in range(GRID_SIZE)):
        return True
    return False

def computer_turn():
    
    def evaluate():
        if check_winner() == COMPUTER_MARKER:
            return 1
        elif check_winner() == PLAYER_MARKER:
            return -1
        else:
            return 0

    def minimax(depth, is_maximizing):
        if check_game_over():
            return evaluate()
        if is_maximizing:
            best_score = -float('inf')
            for row in range(GRID_SIZE):
                for col in range(GRID_SIZE):
                    if board[row][col] == ' ':
                        board[row][col] = COMPUTER_MARKER
                        score = minimax(depth + 1, False)
                        board[row][col] = ' '
                        best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for row in range(GRID_SIZE):
                for col in range(GRID_SIZE):
                    
                    if board[row][col] == ' ':
                        board[row][col] = PLAYER_MARKER
                        score = minimax(depth + 1, True)
                        board[row][col] = ' '
                        best_score = min(best_score, score)
            return best_score
    best_score = -float('inf')
    best_move = None
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == ' ':
                board[row][col] = COMPUTER_MARKER
                score = minimax(0, False)
                board[row][col] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    board[best_move[0]][best_move[1]] = COMPUTER_MARKER

draw_board()

def reset_game():
    global board, turn
    board = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    turn = 0
    draw_board()

play_again_text = FONT.render("Play Again", True, BLACK)
play_again_rect = play_again_text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] - 50))

game_over = False
turn = 0

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            row = mouse_pos[1] // CELL_SIZE
            col = mouse_pos[0] // CELL_SIZE
            if board[row][col] == ' ':
                board[row][col] = PLAYER_MARKER
                turn += 1    
    draw_board()
    if check_game_over():
        winner = check_winner()
        if winner == PLAYER_MARKER:
            text = FONT.render('You win!', True, RED)
        elif winner == COMPUTER_MARKER:
            text = FONT.render('Computer wins!', True, BLUE)
        else:
            text = FONT.render('Tie!', True, BLACK)
        screen.fill(WHITE)
        text_rect = text.get_rect(center=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2))
        screen.blit(text, text_rect)
        text_surface = FONT.render('Shall we play again?', True, (0,0,0))
        gradient_surface = font.Font(None, 50).render('Shall we play again?', True, (0,0,0))
        gradient_surface.blit(text_surface, (2,2))
        play_again_text = gradient_surface
        play_again_rect = play_again_text.get_rect(center=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 + 50))
        pygame.draw.rect(screen, WHITE, play_again_rect)
        pygame.draw.rect(screen, BLACK, play_again_rect, 2)
        screen.blit(play_again_text, play_again_rect)
        if event.type == pygame.MOUSEBUTTONDOWN and play_again_rect.collidepoint(event.pos):
            board = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
            turn = 0
            draw_board()
            continue
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and play_again_rect.collidepoint(event.pos):
                    
                    board = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
                    turn = 0
                    
                    
                    draw_board()
                    game_over = False
                    break
            else:
                continue
            break
    if turn % 2 == 1:
        computer_turn()
        turn += 1
    
    pygame.display.update()
