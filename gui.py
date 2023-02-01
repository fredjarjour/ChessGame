from fen import fenToGrid

def viewBoard(fen):
	grid = fenToGrid(fen.split()[0])
	board = "┌" + "-" * 31 + "┐\n"

	for row in grid:
		board += "| "
		for char in row:
			board += char + " | "
		board = board[:-3] + " |\n|" + "-" * 31 + "|\n"
	board = list(board)
	board[-34] = "└"
	board = "".join(board)
	return board[:-2] + "┘"