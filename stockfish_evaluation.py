from stockfish import Stockfish
import requests

halfmoves = 1
sf = Stockfish()
val_type = None
val = None

while not (val_type == 'mate' and val == 0):
    r = requests.get(f"http://localhost:5000/getfen?halfmove={halfmoves}")
    fen = r.text

    print()
    print("-------------------------")
    sf.set_fen_position(fen)
    best_move = sf.get_best_move()
    print("Best move: was", best_move)
    val_type, val = sf.get_evaluation().values()
    if (val_type == 'mate'):
        print("Mate in", val, "moves")
    else:
        print("Evaluation:", round(val/100, 2))
    print("-------------------------")
    print()

    halfmoves += 1
