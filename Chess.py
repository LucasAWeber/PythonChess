# Chess
# May, 2021
# ShockingRotom

# game of chess starting with white
# doesnt include advanced moves such as castling

# Importing
import pygame
import math
import numpy as np
from extra import draw_library

pygame.init()

# Colours
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# important variables
COLUMNCOUNT = 8
ROWCOUNT = 8
SQUARESIZE = 75

size = (COLUMNCOUNT * SQUARESIZE, ROWCOUNT * SQUARESIZE)
screen = pygame.display.set_mode(size, 0, 32)

screen.fill(WHITE)
pygame.display.set_caption("Chess")

clock = pygame.time.Clock()


# Functions ************************************************************************************************************
# Creates a matrix of the board
def create_board(rows, columns):
    board = np.zeros((rows, columns))
    return board


# Sets the pieces on the board
def set_board(board, columns):
    # Places the pieces
    # Player 1: 10
    # Player 2: 20
    # Pawn: 1
    # Rook: 2
    # Knight: 3
    # Bishop: 4
    # Queen: 5
    # King: 6
    for c in range(columns):
        board[0][c] = 10
        board[1][c] = 10
        board[-2][c] = 20
        board[-1][c] = 20
        board[1][c] += 1
        board[-2][c] += 1
        if c == 0 or c == columns - 1:
            board[0][c] += 2
            board[-1][c] += 2
        elif c == 1 or c == columns - 2:
            board[0][c] += 3
            board[-1][c] += 3
        elif c == 2 or c == columns - 3:
            board[0][c] += 4
            board[-1][c] += 4
        elif c == 3:
            board[0][c] += 5
            board[-1][c] += 5
        elif c == 4:
            board[0][c] += 6
            board[-1][c] += 6
    return board


# Checks that kings are alive
def win_con(board, game):
    if 16 not in board and -34 not in board:
        return "2", False
    elif 26 not in board and -24 not in board:
        return "1", False
    return None, game


# Selects piece
def symbol_select(turn, board, size, rows, columns):
    selected = [-100, -100]
    output = False
    # Gets the mouse position
    mouse_pos = pygame.mouse.get_pos()
    # Divided the position by the size and rounds down to determine the row and column the player is hovering over
    c = int(math.floor(mouse_pos[0] / size))
    r = int(math.floor(mouse_pos[1] / size))
    if (turn + 1) * 10 < board[r][c] < (turn + 2) * 10:
        selected = [r, c]
        board = temp_fill_spaces(board, selected, rows, columns)
        output = True
    return selected, output, board


# Places 1 or 2 in the matrix/board
def symbol_place(turn, board, size, selected, rows, columns):
    output = True
    # Gets the mouse position
    mouse_pos = pygame.mouse.get_pos()
    # Divided the position by the size and rounds down to determine the row and column the player is hovering over
    c = int(math.floor(mouse_pos[0] / size))
    r = int(math.floor(mouse_pos[1] / size))
    # If that value is equal to 0
    if board[r][c] == 0:
        # After verifying that this spot is equal to zero we can make all the temp -50's back to original value
        for cl in range(columns):
            for rl in range(rows):
                if board[rl][cl] < 0:
                    board[rl][cl] += 50
        # Depending on the turn it will place 10 or 20 in that r and c as well as change to next players turn and print
        # The players turn in the console
        if turn == 0:
            board[r][c], board[selected[0]][selected[1]] = board[selected[0]][selected[1]], board[r][c]
            turn += 1
        else:
            board[r][c], board[selected[0]][selected[1]] = board[selected[0]][selected[1]], board[r][c]
            turn -= 1
        output = False
    elif (turn + 2) * 10 < board[r][c] < (turn + 3) * 10 or turn * 10 < board[r][c] < (turn + 1) * 10:
        # After verifying that this spot is another players piece we can make all the temp -50's back to original value
        for cl in range(columns):
            for rl in range(rows):
                if board[rl][cl] < 0:
                    board[rl][cl] += 50
        if turn == 0:
            board[r][c], board[selected[0]][selected[1]] = board[selected[0]][selected[1]], 0
            turn += 1
        else:
            board[r][c], board[selected[0]][selected[1]] = board[selected[0]][selected[1]], 0
            turn -= 1
        output = False
    elif board[r][c] == board[selected[0]][selected[1]]:
        for cl in range(columns):
            for rl in range(rows):
                if board[rl][cl] < 0:
                    board[rl][cl] += 50
        output = False
    return turn, board, output


# Mouse highlighting function
def mouse_highlight(screen, size, board, selected, p_selected, turn):
    # Gets mouse pos
    mouse_pos = pygame.mouse.get_pos()
    # Divides location by the SQUARESIZE and rounds it down to find the column and row the mouse is hovering over
    c = int(math.floor(mouse_pos[0] / size))
    r = int(math.floor(mouse_pos[1] / size))
    # Keeps track of the colour of the main square that follows cursor
    if selected:
        pos = (p_selected[1] * size, p_selected[0] * size)
        colour = YELLOW
        draw_library.draw_highlight(screen, size, pos, colour)
        if board[r][c] == 0 or (turn + 2) * 10 < board[r][c] < (turn + 3) * 10 or turn * 10 < board[r][c] < \
                (turn + 1) * 10:
            colour = GREEN
        else:
            colour = RED
    else:
        if (turn + 1) * 10 < board[r][c] < (turn + 2) * 10:
            colour = YELLOW
        else:
            colour = RED
    # Multiplies the size back into c and r to get the position of the square on the screen
    pos = (c * size, r * size)
    # Draws the box
    draw_library.draw_highlight(screen, size, pos, colour)


# Bishops valid move spaces algo
def bishop_moves(board, s_row, s_col, row, column):
    pospos = True
    posneg = True
    negpos = True
    negneg = True
    for i in range(1, column):
        if 0 <= s_row + i < row and 0 <= s_col + i < column and pospos:
            board[s_row + i][s_col + i] += 50
            if board[s_row + i][s_col + i] != 0:
                pospos = False
        if 0 <= s_row - i < row and 0 <= s_col - i < column and negneg:
            board[s_row - i][s_col - i] += 50
            if board[s_row - i][s_col - i] != 0:
                negneg = False
        if 0 <= s_row + i < row and 0 <= s_col - i < column and posneg:
            board[s_row + i][s_col - i] += 50
            if board[s_row + i][s_col - i] != 0:
                posneg = False
        if 0 <= s_row - i < row and 0 <= s_col + i < column and negpos:
            board[s_row - i][s_col + i] += 50
            if board[s_row - i][s_col + i] != 0:
                negpos = False
    return board

# Rooks valid move spaces algo
def rook_moves(board, s_row, s_col, row, column):
    up = True
    down = True
    left = True
    right = True
    for i in range(1, column):
        if 0 <= s_row + i < row and up:
            board[s_row + i][s_col] += 50
            if board[s_row + i][s_col] != 0:
                up = False
        if 0 <= s_row - i < row and down:
            board[s_row - i][s_col] += 50
            if board[s_row - i][s_col] != 0:
                down = False
        if 0 <= s_col - i < column and left:
            board[s_row][s_col - i] += 50
            if board[s_row][s_col - i] != 0:
                left = False
        if 0 <= s_col + i < column and right:
            board[s_row][s_col + i] += 50
            if board[s_row][s_col + i] != 0:
                right = False
    return board


# Valid spaces (adds 50 to all the negative numbers that the selected piece can move to)
def valid_spaces(board, og_board, selected, row, column):
    s_row = selected[0]
    s_col = selected[1]
    selected_value = board[s_row][s_col] + 50
    # Gets rid of the 10 or 20 to determine the piece it is
    if selected_value - 10 < 10:
        selected_value -= 10
    else:
        selected_value -= 20
    # Checks pieces ***************************************************************************************************
    # If its a pawn
    if selected_value == 1:
        board[s_row][s_col] += 50
        if board[s_row][s_col] >= 20 and s_row - 1 >= 0:
            if board[s_row - 1][s_col] + 50 == 0:
                board[s_row - 1][s_col] += 50
                if og_board[s_row][s_col] == board[s_row][s_col] and board[s_row][s_col] >= 20 and \
                        board[s_row - 2][s_col] + 50 == 0:
                    board[s_row - 2][s_col] += 50
            if s_row - 1 >= 0 and s_col - 1 >= 0 and board[s_row - 1][s_col - 1] + 50 != 0:
                board[s_row - 1][s_col - 1] += 50
            if s_row - 1 >= 0 and s_col + 1 < column and board[s_row - 1][s_col + 1] + 50 != 0:
                board[s_row - 1][s_col + 1] += 50
        elif board[s_row][s_col] >= 10 and s_row + 1 < ROWCOUNT:
            if board[s_row + 1][s_col] + 50 == 0:
                board[s_row + 1][s_col] += 50
                if og_board[s_row][s_col] == board[s_row][s_col] and board[s_row][s_col] >= 10 and \
                        board[s_row + 2][s_col] + 50 == 0:
                    board[s_row + 2][s_col] += 50
            if s_row + 1 < row and s_col - 1 >= 0 and board[s_row + 1][s_col - 1] + 50 != 0:
                board[s_row + 1][s_col - 1] += 50
            if s_row + 1 < row and s_col + 1 < column and board[s_row + 1][s_col + 1] + 50 != 0:
                board[s_row + 1][s_col + 1] += 50
    # Elif its a rook
    elif selected_value == 2:
        board = rook_moves(board, s_row, s_col, row, column)
        board[s_row][s_col] += 50
    # Elif its a knight
    elif selected_value == 3:
        knight_moves = [[2,1],[2,-1],[1,2],[1,-2],[-2,1],[-2,-1],[-1,2],[-1,-2]]
        for i in range(8):
            if 0 <= s_row + knight_moves[i][0] < row and 0 <= s_col + knight_moves[i][1] < column:
                board[s_row + knight_moves[i][0]][s_col + knight_moves[i][1]] += 50
        board[s_row][s_col] += 50
    # Elif its a bishop
    elif selected_value == 4:
        board = bishop_moves(board, s_row, s_col, row, column)
        board[s_row][s_col] += 50
    # Elif its a queen
    elif selected_value == 5:
        board = rook_moves(board, s_row, s_col, row, column)
        board = bishop_moves(board, s_row, s_col, row, column)
        board[s_row][s_col] += 50
    # Elif its a king
    elif selected_value == 6:
        king_moves = [[1,1],[-1,-1],[1,-1],[-1,1],[1,0],[-1,0],[0,1],[0,-1]]
        for i in range(8):
            if 0 <= s_row + king_moves[i][0] < row and 0 <= s_col + king_moves[i][1] < column:
                board[s_row + king_moves[i][0]][s_col + king_moves[i][1]] += 50
        board[s_row][s_col] += 50
    return board


# Temporarily fills spaces with negative numbers by subtracting 50 to all the values to then invalidate any moves
# Later adds 50 to all the spaces the specified piece can move
def temp_fill_spaces(board, selected, rows, columns):
    for c in range(columns):
        for r in range(rows):
            board[r][c] -= 50
    board = valid_spaces(board, og_board, selected, rows, columns)
    return board


board = create_board(ROWCOUNT, COLUMNCOUNT)
board = set_board(board, COLUMNCOUNT)
og_board = board.copy()

game = True
turn = 0
piece_selected = False
selected = [-100, -100]
winner = None

while game:
    # User Events ***************************************************
    # Loop waiting for user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game = False
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            if piece_selected:
                # Calls the symbol place function when player clicks their mouse button
                turn, board, piece_selected = symbol_place(turn, board, SQUARESIZE, selected, ROWCOUNT, COLUMNCOUNT)
            else:
                # Calls the symbol select function when player clicks their mouse button
                selected, piece_selected, board = symbol_select(turn, board, SQUARESIZE, ROWCOUNT, COLUMNCOUNT)

    # Drawing functions
    draw_library.draw_board(screen, SQUARESIZE, ROWCOUNT, COLUMNCOUNT)
    draw_library.draw_pieces(screen, SQUARESIZE, ROWCOUNT, COLUMNCOUNT, board)
    mouse_highlight(screen, SQUARESIZE, board, piece_selected, selected, turn)

    pygame.display.flip()

    winner, game = win_con(board, game)

try:
    print("Player " + winner + " WON!")
except:
    print("Nobody won")
