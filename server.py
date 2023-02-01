from flask import Flask, url_for, request
from gui import viewBoard
from moves import getAllLegalMoves
from string import ascii_letters

app = Flask(__name__)

def convert_to_tuple_coordinate(coord:str) -> tuple[int, int]:
    """a1 becomes (0, 0) and b2 becomes (1, 1) ..."""

    assert len(coord) == 2
    coord = coord.lower()
    letter, number = coord
    
    x = ascii_letters.index(letter)
    y = 8 - int(number)
    assert x in range(8) and y in range(8)

    # the grid is a list of lists so it sees the board flipped
    return y, x
    


@app.route('/submitmove', methods=['POST'])
def submitmove():
    # in the form a1 or b2 or h7 ...
    form_coord = request.form['from']
    to_coord = request.form['to']

    print(list(request.form.values()))

    print(f'Moving from {form_coord} to {to_coord}')

    from_tuple = convert_to_tuple_coordinate(form_coord)
    to_tuple = convert_to_tuple_coordinate(to_coord)

    new_move = (from_tuple, to_tuple)
    legal_moves = getAllLegalMoves(fen)

    assert new_move in legal_moves
    return "move submitted"


fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
viewBoard(fen)

app.run(debug=True)