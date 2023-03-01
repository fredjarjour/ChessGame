try:
    from moves import isCheck, getAllLegalMoves
    from fen import fenToGrid
    import threefold
except ImportError:
    from ChessGame.moves import isCheck, getAllLegalMoves
    from ChessGame.fen import fenToGrid
    import ChessGame.threefold as threefold
import math

# return a tuple: (isGameOver: bool, result: string explaining)
def gameOver(fen, legalMoves=None):
    if int(fen.split()[-2]) >= 100:
        return [True, 0, "50-move rule"]
    
    if threefoldRepetition(fen):
        return [True, 0, "Threefold repetition"]

    if legalMoves == None:
        legalMoves = getAllLegalMoves(fen)
    # checkmate or stalemate
    if legalMoves == []:
        if isCheck(fenToGrid(fen.split()[0]), fen.split()[1]):
            return [True, math.inf * (-1 if fen.split()[1] == "w" else 1), "Checkmate"]
        return [True, 0, "Stalemate"]
    
    return [False, None, None]

def threefoldRepetition(fen):
    position = fen.split()[0]
    if threefold.positions.get(position, 0) >= 3:
        return True
    threefold.positions[position] = threefold.positions.get(position, 0) + 1
    return False