from gui import viewBoard
from moves import getAllLegalMoves
from fen import updateFen, fenToGrid, gridToFen
import random

m = 1000

for games in range(1000):
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    legalMoves = getAllLegalMoves(fen)
    i = 0
    while len(legalMoves) > 0 and i < 500:
        i += 1
        move = random.choice(legalMoves)
        fen = updateFen(fen, move)
        legalMoves = getAllLegalMoves(fen)

    if len(legalMoves) == 0:
        if int(fen.split()[-1]) < m:
            m = int(fen.split()[-1])
            print(fen)

