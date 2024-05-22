import pygame as p
from chess import ChessEngine

WIDTH = HEIGHT = 800
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 #FOR ANIMATION
IMAGES = {}

def loadImages():
    pieces = ['bB', 'bK', 'bN', 'bp', 'bQ', 'bR', 'wB', 'wK', 'wN', 'wp', 'wQ', 'wR']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" +piece+ ".png"), (SQ_SIZE,SQ_SIZE))

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False

    loadImages() #we are only loading the image once
    running = True
    sqSelected = () #keep track of the last click
    playerClicks = [] #keep track of player clicks
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x,y) location of the mouse
                col = location[0]//SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col): #the user clicked the same row twice
                    sqSelected = () #deselect
                    playerClicks = [] #clear player click
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) #append for first and second clicks
                if len(playerClicks) == 2: #after second clicks
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            moveMade = True
                            sqSelected = () #reset user click
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_u: #press u to undo a move
                    gs.undoMove()
                    moveMade = True

            if moveMade:
                validMoves = gs.getValidMoves()
                moveMade = False

            drawGameState(screen, gs)
            clock.tick(MAX_FPS)
            p.display.flip()


def drawGameState(screen , gs):
    drawBoard(screen)
    drawPiece(screen, gs.board)


# def drawBoard(screen):
#     colors = [p.Color(233, 237, 204), p.Color(119, 153, 84)]
#     for r in range(DIMENSION):
#         for c in range(DIMENSION):
#             color = colors[((r+c) % 2)]
#             p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawBoard(screen):
    # Load the chess board image
    board_image = p.image.load("images/board.png")
    # Scale the image to fit the screen
    board_image = p.transform.scale(board_image, (WIDTH, HEIGHT))

    # Blit the chess board image onto the screen
    screen.blit(board_image, (0, 0))

def drawPiece(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__=="__main__":
    main()





















