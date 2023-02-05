# Chess Game

Chess Game is an implementation of the full game of chess. It also has multiple other features such as displaying a command-line version the board, finding all the legal moves in a position, parsing [FEN](https://www.chess.com/terms/fen-chess) positions, etc.

Its main use is as a tool to be used for games between chess bots created by the players, either using the ChessGame functions or not. It does so by using a server, which receives moves from a player and communicates it to the other. The full API for the server is found below in the README.

To use ChessGame as a basis for a bot, simply clone this repository inside of the folder containing your bot script, then `import ChessGame.[file]` or `from ChessGame.[file] import [function]`.


## API for the server

* POST /gettimeleft
  * post data:
    * player = [w | b]
  * returns:
    * the number of seconds on the clock for the given player -- 200 OK
* POST /submitmove
  * post data:
    * from = [a-h][1-8]
    * to = [a-h][1-8]
  * returns:
    * "move submitted" if everything went right -- 200 OK
    * "illegal move" if move is not legal -- 409 Conflict
    * "error when updating fen" if other error like the pawn promotion was not specified -- 422 Unprocessable Entity
    * "No time left on clock" if player lost on time -- 408 Request Timeout
    * "Not your turn" -- 425 Too Early
* POST /login
  * post data:
    * user = [A-Za-z0-9]*
  * returns
    * "User {user} logged in successfully" -- 200
    * "Game is already full" -- 423 Locked


### Examples

See `test.py` for a python3 example of the api
