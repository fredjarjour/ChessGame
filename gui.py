try:
	from fen import fenToGrid
except ImportError:
	from Chess.fen import fenToGrid

def viewBoard(position):
	grid = fenToGrid(position)
	board = "|" + "-" * 31 + "|\n"

	for row in grid:
		board += "| "
		for char in row:
			board += char + " | "
		board = board[:-3] + " |\n|" + "-" * 31 + "|\n"
	board = list(board)
	board = "".join(board)
	return board[:-2] + "|"