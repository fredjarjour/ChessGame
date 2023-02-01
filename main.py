from gui import viewBoard
from moves import getAllLegalMoves
from fen import updateFen, fenToGrid, gridToFen

print(updateFen("rnb1kbnr/pppp2Pp/8/8/7q/8/PPP1PPPP/RNBQKBNR w KQkq - 1 5", ((1,6), (0,7)), "q"))


