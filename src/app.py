from flask import Flask, render_template, jsonify, request
from sudoku import Sudoku


app = Flask(__name__)


def getPuzzlePattern(puzzle,algo):
	if algo == "onesquare":
		pattern = puzzle.oneSquare()
	elif algo == "bestfs":
		pattern = puzzle.bestFS()
	elif algo == "bestfsLoop":
		pattern = puzzle.bestFSLoop()
	elif algo == "horizontalfs":
		pattern = puzzle.horizontalFS()
	elif algo == "horizontalfsLoop":
		pattern = puzzle.horizontalFSLoop()
	elif algo == "verticalfs":
		pattern = puzzle.verticalFS()
	elif algo == "verticalfsLoop":
		pattern = puzzle.verticalFSLoop()
	elif algo == "astar":
		pattern = puzzle.astar()
		if pattern == False:
			return ("nosolution",[])
	elif algo == "depthfs":
		pattern = puzzle.depthFS()
		if pattern == False:
			return ("nosolution",[])

	return pattern

# Load home page
@app.route('/')
def index():
	return render_template('index.html')

# Receive user input, return generated solution in the form of [[squares],[changes]]
@app.route("/update_game", methods=['POST'])
def update_game():
	data = request.get_json()
	algo = data['algo']
	puzzle_str = data['puzzle_str']

	puzzle = Sudoku(puzzle_str)
	puzzle.squares = [] # reset object in case of user's second entry
	puzzle.changes = [] # reset object in case of user's second entry

	errorchecking = puzzle.checkErrors()
	if errorchecking:
		return jsonify(errorchecking)
	else:
		pattern = getPuzzlePattern(puzzle,algo)
	
	return jsonify(pattern)

# Load a puzzle from memory
@app.route("/load_test", methods=['POST'])
def load_test():
	puzzle_difficulty = request.get_json()
	puzzle_str = Sudoku.generatePuzzle(puzzle_difficulty)
	return jsonify(puzzle_str)

if __name__ == "__main__":
	app.run(debug=True)