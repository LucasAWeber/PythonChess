# Import
import pygame

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 150, 200)


# Draw Board
def draw_board(screen, size, rows, columns):
    colour = WHITE
    for c in range(columns):
        for r in range(rows):
            pygame.draw.rect(screen, colour, (r * size, c * size, size, size))
            if r != rows - 1 and colour == WHITE:
                colour = BLUE
            elif r != rows - 1:
                colour = WHITE


def draw_pieces(screen, size, rows, columns, board):
    for c in range(columns):
        for r in range(rows):
            subtract = False
            if board[r][c] < 0:
                board[r][c] += 50
                subtract = True
            if board[r][c] == 11:
                piece = 'WhitePawn.png'
            elif board[r][c] == 12:
                piece = 'WhiteRook.png'
            elif board[r][c] == 13:
                piece = 'WhiteKnight.png'
            elif board[r][c] == 14:
                piece = 'WhiteBishop.png'
            elif board[r][c] == 15:
                piece = 'WhiteQueen.png'
            elif board[r][c] == 16:
                piece = 'WhiteKing.png'
            elif board[r][c] == 21:
                piece = 'BlackPawn.png'
            elif board[r][c] == 22:
                piece = 'BlackRook.png'
            elif board[r][c] == 23:
                piece = 'BlackKnight.png'
            elif board[r][c] == 24:
                piece = 'BlackBishop.png'
            elif board[r][c] == 25:
                piece = 'BlackQueen.png'
            elif board[r][c] == 26:
                piece = 'BlackKing.png'
            else:
                piece = 'ClearSpace.png'
            if subtract:
                board[r][c] -= 50
            image = pygame.image.load('extra/images/' + piece)
            image = pygame.transform.scale(image, (size, size))
            screen.blit(image, [c * size, r * size])


# Draws the selection rectangle/box highlight
def draw_highlight(screen, size, pos, colour):
    select = pygame.Surface((size, size))
    # Makes square semi transparent
    select.set_alpha(128)
    select.fill(colour)
    screen.blit(select, pos)
