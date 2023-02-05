try:
	from fen import fenToGrid, updateGrid
	from pieces import movements
except ImportError:
	from Chess.fen import fenToGrid, updateGrid
	from Chess.pieces import movements

def getAllLegalMoves(fen):
	pseudoLegalMoves = []

	fenWords = fen.split()
	grid = fenToGrid(fenWords[0])
	color = fenWords[1]
	castling = fenWords[2]
	passant = fenWords[3]

	for row in range(len(grid)):
		for char in range(len(grid[row])):
			if grid[row][char] == " ":
				continue
			if grid[row][char].isupper() == (color == "w"):
				test = getLegalMoves(grid, (row, char), castling, passant)
				pseudoLegalMoves += test

	# remove checks
	legalMoves = []
	for move in pseudoLegalMoves:
		if not checkForCheck(grid, move, color):
			legalMoves.append(move)
	
	return legalMoves

def getLegalMoves(grid, position, castling, passant):
	legalMoves = []
	piece = grid[position[0]][position[1]]
	color = "w" if piece.isupper() else "b"

	#pawn
	if piece.lower() == "p":
		direction = 1 if color == "b" else -1
		# moving up 2
		if position[0] == (1 if direction == 1 else 6) and grid[position[0] + direction][position[1]] == grid[position[0] + direction * 2][position[1]] == " ":
			legalMoves.append((position, (position[0] + direction * 2, position[1])))
		# moving up 1
		if grid[position[0] + direction][position[1]] == " ":
			legalMoves.append((position, (position[0] + direction, position[1])))
		#captures
		if position[1] > 0 and (grid[position[0] + direction][position[1] - 1].isupper() == (color == "b")) and (grid[position[0] + direction][position[1] - 1] != " "):
			legalMoves.append((position, (position[0] + direction, position[1] - 1)))
		if position[1] < 7 and (grid[position[0] + direction][position[1] + 1].isupper() == (color == "b")) and (grid[position[0] + direction][position[1] + 1] != " "):
			legalMoves.append((position, (position[0] + direction, position[1] + 1)))
		# en passant
		if len(passant) > 1:
			print(passant, position)
			letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
			numbers = ["8", "7", "6", "5", "4", "3", "2", "1"]
			if position[1] > 0 and numbers[position[0] + direction] == passant[1] and position[1] - 1 == letters.index(passant[0]):
				legalMoves.append((position, (position[0] + direction, position[1] - 1)))
			if position[1] < 7 and numbers[position[0] + direction] == passant[1] and position[1] + 1 == letters.index(passant[0]):
				legalMoves.append((position, (position[0] + direction, position[1] + 1)))

	# knight
	if piece.lower() == "n":
		for move in movements["n"]:
			if not (0 <= position[0] + move[0] <= 7 and 0 <= position[1] + move[1] <= 7):
				continue
			if grid[position[0] + move[0]][position[1] + move[1]] == " " or (grid[position[0] + move[0]][position[1] + move[1]].isupper() == (color == "b")):
				legalMoves.append((position, (position[0] + move[0], position[1] + move[1])))

	# rook, bishop and queen
	if piece.lower() in ["r", "b", "q"]:
		for moveList in movements[piece.lower()]:
			for move in moveList:
				# stop if reached end of board
				if not (0 <= position[0] + move[0] <= 7 and 0 <= position[1] + move[1] <= 7):
					break
				target = grid[position[0] + move[0]][position[1] + move[1]]
				
				if target == " ":
					legalMoves.append((position, (position[0] + move[0], position[1] + move[1])))
					continue
				# stop in that direction if you can capture
				if (target.isupper() == (color == "b")):
					legalMoves.append((position, (position[0] + move[0], position[1] + move[1])))
					break
				# stop if you're blocked by your own piece
				else:
					break
				

	# king
	if piece.lower() == "k":
		for move in movements["k"]:
			if not (0 <= position[0] + move[0] <= 7 and 0 <= position[1] + move[1] <= 7):
				continue
			# normal moves
			if grid[position[0] + move[0]][position[1] + move[1]] == " " or (grid[position[0] + move[0]][position[1] + move[1]].isupper() == (color == "b")):
				legalMoves.append((position, (position[0] + move[0], position[1] + move[1])))
			# castling
		for char in castling:
			if char.isupper() == piece.isupper():
				row = 0 if color == "b" else 7
				if char.lower() == "q":
					if grid[row][1] == grid[row][2] == grid[row][3] == " ":
						legalMoves.append((position, (row, 2)))
				elif char.lower() == "k":
					if grid[row][5] == grid[row][6] == " ":
						legalMoves.append((position, (row, 6)))

	return legalMoves


def checkForCheck(grid, move, color):
	castling = grid[move[0][0]][move[0][1]].lower() == "k" and abs(move[0][1] - move[1][1]) == 2
	
	if castling:
		if isCheck(grid, color):
			return True
		middleMove = (move[0], (move[1][0], abs(move[0][1] + move[1][1]) // 2))
		newGrid = updateGrid([row[:] for row in grid], middleMove)
		if isCheck(newGrid, color):
			return True
			
	newGrid = updateGrid([row[:] for row in grid], move)

	return isCheck(newGrid, color)
	
def isCheck(grid, color):
	king = None
	# find king
	if color == "w": grid = grid[::-1]
	for row in range(8):
		for char in range(8):
			if grid[row][char] == ("K" if color == "w" else "k"):
				king = (row, char)
				break
		if king != None:
			break
	if color == "w":
		grid = grid[::-1]
		king = (7 - king[0], king[1])

	# queen and rook
	for moveList in movements["q"]:
		for move in moveList:
			# stop if reached end of board
			if not (0 <= king[0] + move[0] <= 7 and 0 <= king[1] + move[1] <= 7):
				break
			target = grid[king[0] + move[0]][king[1] + move[1]]
			
			if target == " ":
				continue
			# stop in that direction if you can capture
			if (target.isupper() == (color == "b")):
				if abs(move[0]) == abs(move[1]) and target.lower() in ["q", "b"]:
					return True
				if (move[0] == 0 or move[1] == 0) and target.lower() in ["q", "r"]:
					return True
				break
			break

	# knight
	for move in movements["n"]:
		if not (0 <= king[0] + move[0] <= 7 and 0 <= king[1] + move[1] <= 7):
			continue
		if grid[king[0] + move[0]][king[1] + move[1]] == ("n" if color == "w" else "N"):
			return True

	# king
	for move in movements["k"]:
		if not (0 <= king[0] + move[0] <= 7 and 0 <= king[1] + move[1] <= 7):
			continue
		if grid[king[0] + move[0]][king[1] + move[1]] == ("k" if color == "w" else "K"):
			return True

	# pawn
	direction = -1 if color == "w" else 1
	if not (0 <= king[0] + direction <= 7):
		return False
	if 0 <= king[1] - 1 <= 7 and grid[king[0] + direction][king[1] - 1] == ("p" if color == "w" else "P"):
		return True
	if 0 <= king[1] + 1 <= 7 and grid[king[0] + direction][king[1] + 1] == ("p" if color == "w" else "P"):
		return True
	
	return False