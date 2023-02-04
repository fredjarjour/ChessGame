from moves import getAllLegalMoves
from fen import updateFen
from result import gameOver
import threefold
import random


results = {}
numGames = 10

for _ in range(numGames):
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    while True:
        legalMoves = getAllLegalMoves(fen)
        move = random.choice(legalMoves)
        fen = updateFen(fen, move)
        game = gameOver(fen) 
        if game[0]:
            results[game[2]] = results.get(game[2], 0) + 1
            break
    threefold.positions = {}

print(f"After running {numGames} games, the results are:")
print(results)