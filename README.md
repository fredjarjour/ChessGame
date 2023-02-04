# API for the server

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


## Examples

see `test.py` for a python3 example of the api