def updateFen(previousFen, move, promote = "q"):
	position, color, castling, passant, halfmove, fullmove = previousFen.split()
	grid = fenToGrid(position)

	capture = False if grid[move[1][0]][move[1][1]] == " " else True

	letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
	
	newFen = ""
	
	newGrid = updateGrid(grid, move, passant, promote)
	newFen += gridToFen(newGrid)

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

	newFen += castling if len(castling) > 0 else "-"

	# en passant
	rowNumber = 3 if color == "b" else 4
	direction = 1 if color == "b" else -1
	foundPassant = False
	for char in range(1, 7):
		if newGrid[rowNumber][char] == ("P" if color == "b" else "p") and newGrid[rowNumber - direction][char] == newGrid[rowNumber - direction * 2][char] == " ":
			if newGrid[rowNumber][char - 1] == ("p" if color == "b" else "P") or newGrid[rowNumber][char + 1] == ("p" if color == "b" else "P"):
				temprow = position.split("/")[rowNumber - 2 * direction]
				row = ""
				for c in temprow:
					if c.isdigit():
						row += " " * int(c)
					else:
						row += c
				if row[char].lower() == "p":
					newFen += " " + letters[char] + str(rowNumber - direction) + " "
					foundPassant = True
					break
	if not foundPassant:
		newFen += " - "

	if capture or grid[move[0][0]][move[0][1]].lower() == "p" or foundPassant:
		newFen += "0 "
	else:
		newFen += str(int(halfmove) + 1) + " "
	newFen += fullmove if color == "w" else str(int(fullmove) + 1)

	return newFen

def updateGrid(grid, move, passant="-", promote="q"):
	numbers = ["8", "7", "6", "5", "4", "3", "2", "1"]
	letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
	# position
	piece = grid[move[0][0]][move[0][1]]
	grid[move[0][0]][move[0][1]] = " "
	
	# promotion
	if piece.lower() == "p" and move[1][0] in [0, 7]:
		if promote.lower() in ["q", "r", "b", "n"]:
			piece = promote.upper() if piece.isupper() else promote.lower()
		else:
			return False

	grid[move[1][0]][move[1][1]] = piece

	# passant
	if piece.lower() == "p" and passant != "-":
		if numbers[move[1][0]] == passant[1] and letters[move[1][1]] == passant[0]:
			grid[move[0][0]][move[1][1]] = " "
	
	# castling
	if piece.lower() == "k" and abs(move[0][1] - move[1][1]) == 2:
		if move[1][1] == 7:
			grid[move[1][0]][5] = grid[move[1][0]][7]
			grid[move[1][0]][7] = " "
		else:
			grid[move[1][0]][3] = grid[move[1][0]][0]
			grid[move[1][0]][0] = " "
	return grid


def fenToGrid(position):
	grid = []
	rows = position.split("/")

	for row in rows:
		for char in row:
			if char.isdigit():
				row = row.replace(char, int(char) * " ")
		grid.append(list(row))

	return grid

def gridToFen(grid):
	fen = ""

	for row in grid:
		emptyCount = 0
		for char in row:
			if char == " ":
				emptyCount += 1
				continue
			if emptyCount > 0:
				fen += str(emptyCount)
				emptyCount = 0
			fen += char
		if emptyCount > 0:
			fen += str(emptyCount)
		fen += "/"

	return fen[:-1]

#This could be optimized when checking if letter == Capitalized letter or not capitalized letter
def fensToPgn(fens, Coordmoves):

    moveList = []
    remeberCoords = ""

    for i in range(len(fens)):

        current = fens[i]
        Coordmove = Coordmoves[i][0]
        Coordmove2 = Coordmoves[i][1]

        grid = fenToGrid(current.split()[0])
        letter = grid[int(Coordmove[0])][int(Coordmove[1])]

        if remeberCoords != "":
            lastMove = moveList.pop()
            promoted = grid[int(remeberCoords[0])][int(remeberCoords[1])]
            if promoted == "Q" or promoted == "q":
                lastMove += "Q"
            elif promoted == "R" or promoted == "r":
                lastMove += "R"
            elif promoted == "B" or promoted == "b":
                lastMove += "B"
            elif promoted == "N" or promoted == "n":
                lastMove += "N"
            moveList.append(lastMove)
            remeberCoords = ""
        
        currentP = ""

        if letter == "K" or letter == "k":
            currentP = "K"
        elif letter == "Q" or letter == "q":
            currentP = "Q"
        elif letter == "R" or letter == "r":
            currentP = "R"
        elif letter == "B" or letter == "b":
            currentP = "B"
        elif letter == "N" or letter == "n":
            currentP = "N"
        elif letter == "P" or letter == "p":
            currentP = "P"

        moveToAppend = ""

        if currentP == "P":

            if abs(int(Coordmove[0]) - int(Coordmove2[0])) == 2:
                moveToAppend = chr(Coordmove[1]+97) + str(8-Coordmove2[0])

            elif Coordmove[1] == Coordmove2[1]:
                moveToAppend = chr(Coordmove[1]+97) + str(8-Coordmove2[0])

            else:
                moveToAppend = chr(Coordmove[1]+97) + "x" + chr(Coordmove2[1]+97) + str(8-Coordmove2[0])
            if Coordmove2[0] == 0 or Coordmove2[0] == 7:
                    promoted = grid[int(Coordmove2[0])][int(Coordmove2[1])]
                    remeberCoords = Coordmove2
                    moveToAppend += "="
        elif currentP == "B":
            moveToAppend = "B"+chr(Coordmove[1]+97) + str(8-Coordmove[0])
            if grid[Coordmove2[0]][Coordmove2[1]] != " ":
                moveToAppend += "x"
            moveToAppend +=chr(Coordmove2[1]+97) + str(8-Coordmove2[0])
        elif currentP == "N":
            moveToAppend = "N"+chr(Coordmove[1]+97) + str(8-Coordmove[0])
            if grid[Coordmove2[0]][Coordmove2[1]] != " ":
                moveToAppend += "x"
            moveToAppend +=chr(Coordmove2[1]+97) + str(8-Coordmove2[0])
        elif currentP == "R":
            moveToAppend = "R"+chr(Coordmove[1]+97) + str(8-Coordmove[0])
            if grid[Coordmove2[0]][Coordmove2[1]] != " ":
                moveToAppend += "x"
            moveToAppend +=chr(Coordmove2[1]+97) + str(8-Coordmove2[0])
        elif currentP == "Q":
            moveToAppend = "Q"+chr(Coordmove[1]+97) + str(8-Coordmove[0])
            if grid[Coordmove2[0]][Coordmove2[1]] != " ":
                moveToAppend += "x"
            moveToAppend +=chr(Coordmove2[1]+97) + str(8-Coordmove2[0])
        elif currentP == "K":
            if int(Coordmove[1]) - int(Coordmove2[1]) == 2:
                moveToAppend = "O-O-O"
            elif int(Coordmove[1]) - int(Coordmove2[1]) == -2:
                moveToAppend = "O-O"
            else :
                moveToAppend = "K"+chr(Coordmove[1]+97) + str(8-Coordmove[0])
                if grid[Coordmove2[0]][Coordmove2[1]] != " ":
                    moveToAppend += "x"
                moveToAppend +=chr(Coordmove2[1]+97) + str(8-Coordmove2[0])

        moveList.append(moveToAppend)

    pgn = ""
    for i in range(len(moveList)):
        if i % 2 == 0:
            pgn += str(i//2+1) + ". " + moveList[i] + " "
        else:
            pgn += moveList[i] + " "

    return pgn