from flask import Flask, request, session
from gui import viewBoard
from moves import getAllLegalMoves
from fen import updateFen
from string import ascii_letters
from datetime import datetime, timedelta
import markdown

app = Flask(__name__)

app.secret_key = 'mysecretkey'.encode()

def convert_to_tuple_coordinate(coord:str) -> tuple[int, int]:
    """a1 becomes (0, 0) and b2 becomes (1, 1) ..."""

    assert len(coord) == 2
    coord = coord.lower()
    letter, number = coord
    
    x = ascii_letters.index(letter)
    # black's a file rook is (0, 0), 
    # so that when the board is rendered, we see white's perspective
    y = 8 - int(number) 
    assert x in range(8) and y in range(8)

    # the grid is a list of lists so it sees the board flipped
    return y, x

def is_player_turn(username):
    turn = fen.split()[1] # gets 'w' if white's turn or 'b' if black's turn
    if turn == 'w' and username == white_username:
        return True
    if turn == 'b' and username == black_username:
        return True
    return False

@app.route('/login', methods=['POST'])
def login():
    global white_username, black_username
    user = request.form['user']
    session['username'] = user

    # make sure there is not already 2 players
    if white_username and black_username:
        return "Game is already full", 423

    if not white_username:
        white_username = user
    else:
        black_username = user

    return f"User {user} logged in successfully", 200


@app.route('/gettimeleft', methods=['POST'])
def gettimeleft():
    """return the amount of seconds left for the player"""
    player = request.form['player'].lower()

    if player == 'w':
        return str((white_time - datetime.now()).seconds)
    if player == 'b':
        return str((white_time - datetime.now()).seconds)

    return -1

@app.route('/submitmove', methods=['POST'])
def submitmove():
    global fen
    if 'username' not in session:
        return "You are not logged in", 401

    print(f"Processing {session['username']}'s turn")

    if not is_player_turn(session['username']):
        return "Not your turn", 425

    if (white_time - datetime.now()).seconds < 0:
        return "No time left on clock", 408

    # in the form a1 or b2 or h7 ...
    form_coord = request.form['from']
    to_coord = request.form['to']
    # which piece to promote to if the pawn reaches the end
    promote = request.form.get('promote', None)

    from_tuple = convert_to_tuple_coordinate(form_coord)
    to_tuple = convert_to_tuple_coordinate(to_coord)

    new_move = (from_tuple, to_tuple)
    print(fen)
    legal_moves = getAllLegalMoves(fen)

    if new_move not in legal_moves:
        return "illegal move", 409
    
    new_fen = updateFen(fen, new_move, promote)
    if not new_fen:
        return "error when updating fen", 422

    fen = new_fen
    print(viewBoard(fen))

    return f"move submitted by user {session['username']}", 200

white_time = datetime.now() + timedelta(minutes=20)
black_time = datetime.now() + timedelta(minutes=20)
white_username = None
black_username = None

fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

if __name__ == "__main__":
    print(viewBoard(fen))
    app.run(debug=False)
