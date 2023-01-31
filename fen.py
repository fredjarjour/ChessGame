def generateFen(previousFen, newGrid):
	_, color, castling, _, halfmove, fullmove = previousFen.split()

	newFen = ""

	# position
	for row in newGrid:
		emptyCount = 0
		for char in row:
			if char == " ":
				emptyCount += 1
				continue
			if emptyCount > 0:
				newFen += str(emptyCount)
				emptyCount = 0
			newFen += char
		if emptyCount > 0:
			newFen += str(emptyCount)
		newFen += "/"

	# color
	newFen += " w " if color == "b" else " b "

	# castling
	if color == "w" and ("K" in castling or "Q" in castling):
		if newGrid[7][4] != "K":
			if "K" in castling:
				castling = castling.replace("K", "")
			if "Q" in castling:
				castling = castling.replace("Q", "")
		if "K" in castling and newGrid[7][7] != "R":
			castling = castling.replace("K", "")
		if "Q" in castling and newGrid[7][0] != "R":
			castling.replace("Q", "")

	if color == "b" and ("k" in castling or "q" in castling):
		if newGrid[0][4] != "k":
			if "k" in castling:
				castling = castling.replace("k", "")
			if "q" in castling:
				castling = castling.replace("q", "")
		if "k" in castling and newGrid[0][7] != "r":
			castling = castling.replace("k", "")
		if "q" in castling and newGrid[0][0] != "r":
			castling = castling.replace("q", "")

	newFen += castling

	# TODO : Detect en passant
	newFen += " - "

	newFen += str(int(halfmove) + 1) + " "
	newFen += fullmove if color == "w" else str(int(fullmove) + 1)

	return newFen