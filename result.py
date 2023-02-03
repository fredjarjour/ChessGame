try:
    from moves import isCheck, getAllLegalMoves
    from fen import fenToGrid
    import threefold
except ImportError:
    from Chess.moves import isCheck, getAllLegalMoves
    from Chess.fen import fenToGrid
    import Chess.threefold as threefold
import math

# return a tuple: (isGameOver: bool, result: string explaining)
def gameOver(fen):
    if int(fen.split()[-2]) >= 100:
        return [True, 0, "50-move rule"]
    
    if threefoldRepetition(fen):
        return [True, 0, "Threefold repetition"]

    # checkmate or stalemate
    if getAllLegalMoves(fen) == []:
        if isCheck(fenToGrid(fen.split()[0]), fen.split()[1]):
            return [True, math.inf * (-1 if fen.split()[1] == "w" else 1), "Checkmate"]
        return [True, 0, "Stalemate"]
    
    return [False, None, None]

def threefoldRepetition(fen):
    position = fen.split()[0]
    if threefold.positions.get(position, 0) >= 2:
        return True
    threefold.positions[position] = threefold.positions.get(position, 0) + 1
    return False