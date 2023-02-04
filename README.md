# API for the server

1) POST /gettimeleft
   1) post data:
      1) player = [0 | 1]
   2) returns:
      1) the number of seconds on the clock for the given player -- 200 OK
2) POST /submitmove
   1) post data:
      1) from = [a-h][1-8]
      2) to = [a-h][1-8]
   2) returns:
      1) "move submitted" if everything went right -- 200 OK
      2) "illegal move" if move is not legal -- 409 Conflict
      3) "error when updating fen" if other error like the pawn promotion was not specified -- 422 Unprocessable Entity
      4) "No time left on clock" if player lost on time -- 408 Request Timeout