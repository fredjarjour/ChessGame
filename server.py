from flask import Flask, request, session
from gui import viewBoard
from moves import getAllLegalMoves
from fen import updateFen
from string import ascii_letters
from datetime import datetime, timedelta
import time

app = Flask(__name__)

app.secret_key = 'mysecretkey'.encode()

def convert_to_tuple_coordinate(coord:str) -> tuple[int, int]:
    """a1 becomes (0, 0), and b2 becomes (1, 1) ..."""

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

def convert_to_chess_coordinate(coord: tuple[int, int]) -> str:
    """(0, 0) become a1, and (1, 1) becomes b2 ..."""
    # the grid is a list of lists so it sees the board flipped
    y, x = coord
    file = ascii_letters[x]
    rank = str(8 - y)

    return file + rank

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
    print("User", user, "logged in")
    session['username'] = user

    # make sure there is not already 2 players
    if white_username and black_username:
        return "Game is already full", 423

    if not white_username:
        white_username = user
    else:
        black_username = user

    return f"User {user} logged in successfully", 200


@app.route('/gettimeleft', methods=['GET'])
def gettimeleft():
    """return the amount of seconds left for the player"""
    player = request.args.get('player')

    print("Getting time left for player", player)

    w_time_left = str((white_time - datetime.now()).seconds)
    b_time_left = str((black_time - datetime.now()).seconds)

    if player == 'w':
        return w_time_left
    if player == 'b':
        return b_time_left

    return "Invalid player", 400

@app.route('/submitmove', methods=['POST'])
def submitmove():
    global fen, last_move
    if 'username' not in session:
        return "You are not logged in", 401

    print(f"Processing {session['username']}'s turn")

    if not is_player_turn(session['username']):
        return "Not your turn", 425

    if (white_time - datetime.now()).seconds < 0:
        return "No time left on clock", 408

    # in the form a1 or b2 or h7 ...
    from_coord = request.form['from']
    to_coord = request.form['to']
    # which piece to promote to if the pawn reaches the end
    promote = request.form.get('promote', None)

    print(f'from {from_coord} to {to_coord} {"promote to " + promote if promote is not None else ""}')

    from_tuple = convert_to_tuple_coordinate(from_coord)
    to_tuple = convert_to_tuple_coordinate(to_coord)

    legal_moves = getAllLegalMoves(fen)

    new_move = (from_tuple, to_tuple)

    if new_move not in legal_moves:
        return "Illegal move", 409
    
    new_fen = updateFen(fen, new_move, promote)
    if not new_fen:
        return "Error when updating fen", 422

    print(new_fen)
    print(viewBoard(new_fen))

    # last move is a string that looks like "a1b2" or "a1b2q" with the promotion piece
    last_move = from_coord + to_coord + (promote or '')

    # lock in this move by updating the fen at the end of the function
    # this avoids race conditions where the other player thinks it is their turn
    fen = new_fen 
    
    return f"Move submitted by user {session['username']}", 200

@app.route('/getmove', methods=['GET'])
def getmove():
    if 'username' not in session:
        return "You are not logged in", 401

    username = session['username']

    # the player whose turn it ISNT, waits until it is their turn to read the last move
    while not is_player_turn(username) or last_move is None:
        time.sleep(0.2)

    # the player who currently needs to play
    # requires the other player's last move
    return last_move


last_move = None, None # used to hold the last move so it can be given to the other player
white_time = datetime.now() + timedelta(minutes=20)
black_time = datetime.now() + timedelta(minutes=20)
white_username = None
black_username = None

fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

if __name__ == "__main__":
    print(viewBoard(fen))
    app.run(debug=False, host='0.0.0.0')
