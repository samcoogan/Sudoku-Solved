from sudoku import Sudoku
import sys

def startgame(game):
	print(game)

	text = input("Enter search or end: ")
	if text == "onesq":
		print("Changes: " + str(game.oneSquare()))
	elif text == "vert":
		print("Changes: " + str(game.verticalFS()[1]))
	elif text == "vertloop":
		print("Changes: " + str(game.verticalLoopFS()[1]))
	elif text == "dfs":
		print("Changes: " + str(game.depthFS()[1]))
	elif text == "hor":
		print("Changes: " + str(game.horizontalFS()))
	elif text == "horloop":
		print("Changes: " + str(game.horizontalFSLoop()[1]))
	elif text == "best":
		print("Changes: " + str(game.bestFS()[1]))
	elif text == "bestloop":
		print("Changes: " + str(game.bestFSLoop()[1]))
	elif text == "astar":
		a = game.astar()
	elif text == "getsq":
		print(game.getAvailableSquares())
		startgame(game)
	elif text == "b":
		game.backtrack()
	elif text == end:
		print(game)
		print("End game")

	print(game)
	startgame(game)



def main():
	game = Sudoku.generatePuzzle(2)
	game1 = Sudoku(game)
	startgame(game1)


if __name__ == "__main__":
	main()