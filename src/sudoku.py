import random

class Sudoku:
    puzzle = [] # Contains the users puzzle 
    squares = [] # Contains the squares checked
    changes = [] # Contains changes made

    # Initialize Puzzle to input or 0's
    def __init__(self,puzzle_str):
        for i in range(9):
            self.puzzle.append([0,0,0,0,0,0,0,0,0])
        
        self.stringtopuzzle(puzzle_str)

    # Print out the puzzle to console
    def __str__(self):
        output = ""
        i = 0
        output += "---\n"
        while i < 9:
            output += str(self.puzzle[i]) + "\n"
            i+=1
        output += "---"
        return output

    # Convert string to 2D List 
    def stringtopuzzle(self,puzzle_str):
        allowed_nums = [1,2,3,4,5,6,7,8,9]
        i = 0
        while i < 81:
            self.puzzle[i//9][i%9] = int(puzzle_str[i])
            i += 1


    ## Run one iteration of a breath first search accross the puzzle
    def horizontalFS(self):
        squares = []
        changes = []
        total_changes = 0
        i = 0
        while i < 9:
            j = 0
            while j < 9:
                if self.puzzle[i][j] == 0:
                    possible_ans = self.checkSquare((i,j))
                    squares.append(i*9+j)
                    if len(possible_ans) == 1:
                        self.puzzle[i][j] = possible_ans[0]
                        changes.append(possible_ans[0])
                        total_changes += 1
                    else:
                        changes.append(0)
                j+=1
            i+=1

        if total_changes == 0:
            return [["nochanges"],[]]
        return [squares,changes]

    # Loop through puzzle from left-to-right until there are no obvious solutions left
    def horizontalFSLoop(self):
        squares = []
        changes = []
        total_changes = 0
        scancomplete = False
        while scancomplete == False:
            changes_this_scan = 0
            i = 0
            while i < 9:
                j = 0
                while j < 9:
                    if self.puzzle[i][j] == 0:
                        possible_ans = self.checkSquare((i,j))
                        squares.append(i*9+j)
                        if len(possible_ans) == 1:
                            self.puzzle[i][j] = possible_ans[0]
                            changes.append(possible_ans[0])
                            total_changes += 1
                            changes_this_scan += 1
                        else:
                            changes.append(0)
                    j+=1
                i+=1
            if changes_this_scan == 0:
                scancomplete = True
        if total_changes == 0:
            return ["nochanges",[]]
        return [squares,changes]

    # Loop through puzzle from left-to-right until there are no obvious solutions
    def verticalFSLoop(self):
        squares = []
        changes = []
        total_changes = 0
        scancomplete = False
        while scancomplete == False:
            changes_this_scan = 0
            i = 0
            while i < 9:
                j = 0
                while j < 9:
                    if self.puzzle[j][i] == 0:
                        possible_ans = self.checkSquare((j,i))
                        squares.append(j*9+i)
                        if len(possible_ans) == 1:
                            self.puzzle[j][i] = possible_ans[0]
                            changes.append(possible_ans[0])
                            total_changes += 1
                            changes_this_scan += 1
                        else:
                            changes.append(0)
                    j += 1
                i += 1
            if changes_this_scan == 0:
                scancomplete = True
        if total_changes == 0:
            return ["nochanges",[]]
        return [squares,changes]

    # Scan through puzzle once from top-to-bottom, revealing obvious solutions
    def verticalFS(self):
        squares = []
        changes = []
        total_changes = 0
        i = 0
        while i < 9:
            j = 0
            while j < 9:
                if self.puzzle[j][i] == 0:
                    possible_ans = self.checkSquare((j,i))
                    squares.append(j*9+i)
                    if len(possible_ans) == 1:
                        self.puzzle[j][i] = possible_ans[0]
                        changes.append(possible_ans[0])
                        total_changes += 1
                    else:
                        changes.append(0)
                j += 1
            i += 1
        if total_changes == 0:
            return ["nochanges",[]]
        return [squares,changes]

    # Scan through puzzle once in order of most solvable squares first, revealing obvious solutions
    def bestFS(self):
        squares = []
        changes = []
        total_changes = 0
        sorted_squares = self.sortedAvailableSquares()
        for sq in sorted_squares:
            possible_ans = self.checkSquare(sq)
            squares.append(sq[0]*9+sq[1])
            if len(possible_ans) == 1:
                self.puzzle[sq[0]][sq[1]] = possible_ans[0]
                changes.append(possible_ans[0])
                total_changes += 1
            else:
                changes.append(0)
        if total_changes == 0:
            return ["nochanges",[]]
        return [squares,changes]

    # Loop through puzzle in order of most solvable squares first, revealing obvious solutions
    def bestFSLoop(self):
        squares = []
        changes = []
        total_changes = 0
        scancomplete = False
        while scancomplete == False:
            changes_this_scan = 0
            sorted_squares = self.sortedAvailableSquares()
            for sq in sorted_squares:
                possible_ans = self.checkSquare(sq)
                squares.append(sq[0]*9+sq[1])
                if len(possible_ans) == 1:
                    self.puzzle[sq[0]][sq[1]] = possible_ans[0]
                    changes.append(possible_ans[0])
                    total_changes += 1
                    changes_this_scan += 1
                else:
                    changes.append(0)
            if changes_this_scan == 0:
                scancomplete = True
        if total_changes == 0:
            return ["nochanges",[]]
        return [squares,changes]

    # Conduct backtracking algorithm       
    def depthFS(self):
        avail_squares = self.getAvailableSquares()
        if not avail_squares:
            return [self.squares,self.changes]
        else:
            sq = avail_squares[0]

        for i in range(1,10):
            if self.isValid(sq,i):
                self.puzzle[sq[0]][sq[1]] = i
                self.squares.append(sq[0]*9+sq[1])
                self.changes.append(i)

                if self.depthFS():
                    return [self.squares,self.changes]

                self.puzzle[sq[0]][sq[1]] = 0
                self.squares.append(sq[0]*9+sq[1])
                self.changes.append(0)
        return False

    # Conduct heuristic a* algorithm
    def astar(self):
        sorted_squares = self.sortedAvailableSquares()
        if not sorted_squares:
            return [self.squares,self.changes]
        else:
            sq = sorted_squares[0]

        for i in range(1,10):
            if self.isValid(sq,i):
                self.puzzle[sq[0]][sq[1]] = i
                self.squares.append(sq[0]*9+sq[1])
                self.changes.append(i)

                if self.astar():
                    return [self.squares,self.changes]

                self.puzzle[sq[0]][sq[1]] = 0
                self.squares.append(sq[0]*9+sq[1])
                self.changes.append(0)
        return False

    # Return a single solved square
    def oneSquare(self):
        unfilled_squares = self.getAvailableSquares()

        original_puzzle = self.puzzle # create copy of original puzzle
        check_for_obvious = self.bestFS() # run simple search
        self.puzzle = original_puzzle # reset puzzle
        solutions = 0
        i = 0
        if check_for_obvious[1]:
            while i < len(check_for_obvious) and solutions == 0:
                if check_for_obvious[1][i] > 0:
                    square = check_for_obvious[0][i]
                    square_sol = check_for_obvious[1][i]
                    solutions += 1
                i += 1
            self.puzzle[square//9][square%9] = square_sol

        if solutions == 0:
            sq = unfilled_squares[0]
            runastar = self.astar()
            if runastar:
                square_sol = self.puzzle[sq[0]][sq[1]]
                self.puzzle = original_puzzle # Reset puzzle 
                self.puzzle[sq[0]][sq[1]] = square_sol # Fill in single square
            else:
                return False
            square = sq[0]*9 + sq[1] # Convert Grid ref to string index 
        

        return [[square],[square_sol]]

    # Check is num is a valid fit for a square
    def isValid(self,sq,num):
        if num in self.checkSquare(sq):
            return True
        else:
            return False

    # Return a list of clashing squares
    def checkErrors(self):
        errors = []
        filled_squares = self.getFilledSquares()

        if len(filled_squares) < 17:
            return ["not_enough_squares",[]]
        elif len(filled_squares) == 81:
            return ["puzzle_complete",[]]
            
        for sq in filled_squares:
            sq_row = self.puzzle[sq[0]]
            sq_col = self.getCol(sq[1])
            sq_cube = self.getCube(sq[0],sq[1])
            allnums = sq_row + sq_col + sq_cube

            if allnums.count(self.puzzle[sq[0]][sq[1]]) > 3: 
               errors.append(sq[0]*9+sq[1])

        if errors:
            return ["input_error",errors]
        else:
            return []


    # Sort squares in the format (x,y) in order of least possible solutions
    def sortedAvailableSquares(self):
        available_squares = self.getAvailableSquares()
        sorted_squares = []
        i = 0
        while available_squares:
            min_sq = available_squares[0]
            for sq in available_squares:
                if len(self.checkSquare(sq)) < len(self.checkSquare(min_sq)):
                    min_sq = sq
            sorted_squares.append(min_sq)
            available_squares.remove(min_sq)

        return sorted_squares

    # Get all blank squares
    def getAvailableSquares(self):
        output = []
        i = 0
        while i < 9:
            j = 0
            while j < 9:
                if self.puzzle[i][j] == 0:
                    output.append((i,j))
                j += 1
            i += 1
        return output
    
    # Get all squares with a value
    def getFilledSquares(self):
        output = []
        i = 0
        while i < 9:
            j = 0
            while j < 9:
                if self.puzzle[i][j] != 0:
                    output.append((i,j))
                j += 1
            i += 1
        return output

    # return amount of possible solutions to squares family  
    def checkSqSurroundings(self,x,y):
        rownums = self.unsolvedCount(self.puzzle[x])
        colnums = self.unsolvedCount(self.getCol(y))
        cubenums = self.unsolvedCount(self.getCube(x,y))

        return rownums+colnums+cubenums-3


    # Return list of possible solutions to a square 
    def checkSquare(self,sq):
        nums = [1,2,3,4,5,6,7,8,9]
        solutions = []
        rownums = self.checkLine(self.puzzle[sq[0]])
        colnums = self.checkLine(self.getCol(sq[1]))
        cubenums = self.checkLine(self.getCube(sq[0],sq[1]))
  
        for n in nums:
            if n in rownums:
                if n in colnums:
                    if n in cubenums:
                        solutions.append(n)

        return solutions

    # Retrive list of elements of the cube in which the square belongs
    def getCube(self,x,y):  
        cube = []

        if x < 3:
            if y < 3:
                cube.extend([self.puzzle[0][0],self.puzzle[0][1],self.puzzle[0][2],self.puzzle[1][0],self.puzzle[1][1],self.puzzle[1][2],self.puzzle[2][0],self.puzzle[2][1],self.puzzle[2][2]])
            elif y < 6:
                cube.extend([self.puzzle[0][3],self.puzzle[0][4],self.puzzle[0][5],self.puzzle[1][3],self.puzzle[1][4],self.puzzle[1][5],self.puzzle[2][3],self.puzzle[2][4],self.puzzle[2][5]])
            else:
                cube.extend([self.puzzle[0][6],self.puzzle[0][7],self.puzzle[0][8],self.puzzle[1][6],self.puzzle[1][7],self.puzzle[1][8],self.puzzle[2][6],self.puzzle[2][7],self.puzzle[2][8]])
        elif x < 6:
            if y < 3:
                cube.extend([self.puzzle[3][0],self.puzzle[3][1],self.puzzle[3][2],self.puzzle[4][0],self.puzzle[4][1],self.puzzle[4][2],self.puzzle[5][0],self.puzzle[5][1],self.puzzle[5][2]])
            elif y < 6:
                cube.extend([self.puzzle[3][3],self.puzzle[3][4],self.puzzle[3][5],self.puzzle[4][3],self.puzzle[4][4],self.puzzle[4][5],self.puzzle[5][3],self.puzzle[5][4],self.puzzle[5][5]])
            else:
                cube.extend([self.puzzle[3][6],self.puzzle[3][7],self.puzzle[3][8],self.puzzle[4][6],self.puzzle[4][7],self.puzzle[4][8],self.puzzle[5][6],self.puzzle[5][7],self.puzzle[5][8]])
        else:
            if y < 3:
                cube.extend([self.puzzle[6][0],self.puzzle[6][1],self.puzzle[6][2],self.puzzle[7][0],self.puzzle[7][1],self.puzzle[7][2],self.puzzle[8][0],self.puzzle[8][1],self.puzzle[8][2]])
            elif y < 6:
                cube.extend([self.puzzle[6][3],self.puzzle[6][4],self.puzzle[6][5],self.puzzle[7][3],self.puzzle[7][4],self.puzzle[7][5],self.puzzle[8][3],self.puzzle[8][4],self.puzzle[8][5]])
            else:
                cube.extend([self.puzzle[6][6],self.puzzle[6][7],self.puzzle[6][8],self.puzzle[7][6],self.puzzle[7][7],self.puzzle[7][8],self.puzzle[8][6],self.puzzle[8][7],self.puzzle[8][8]])

        return cube


  
    ## Retrive list is elements of the column in which the square belongs
    def getCol(self,y):
        col = []
        i = 0
        while i < 9:
            col.append(self.puzzle[i][y])
            i += 1

        return col

    ## Return list of possible solutions to a list of numbers
    def checkLine(self,line):
        nums = [1,2,3,4,5,6,7,8,9]
        unfilled = []
        for n in nums:
            if n not in line:
                unfilled.append(n)

        return unfilled

    # Count the unsolved squares in a line
    def unsolvedCount(self,line):
        count = 0
        for n in line:
            if n == 0:
                count += 1
        return count

    # Load puzzle from memory
    def generatePuzzle(puzzle_difficulty):
        easypuzzles = []
        medpuzzles =[]
        hardpuzzles = []

        easypuzzles.append("040050209600000408090730051060400502004809100209005080920081040501000006403070010") #easy
        easypuzzles.append("401600090020701000000402501900013006056080420300540009708105000000804060060009708") #easy
        easypuzzles.append("080030009060007020000090380278000490000709000095000671037010000020900060900070030") #easy
        easypuzzles.append("705100004012400080400080000001609020000030000040705300000090008020004170100008906") #easy
        easypuzzles.append("040000000063205000720000401800930002070000010900072004205000079000608140000000030") #easy
        medpuzzles.append("700000001068002053001050600642900010000000000010004567006090800190800270300000005") #med
        medpuzzles.append("020000060900406100100080700005079000400060003000140800008010002003207001060000090") #med
        medpuzzles.append("300008700002700039000350000000006217003000400217800000000095000980003600001600003") #med
        medpuzzles.append("030020080000001026000600100001030002407090305900070600002007000790200000010050030") #med
        medpuzzles.append("000400700094007005005028000600000070701090302080000001000170200200300490008006000") #med
        hardpuzzles.append("009085000710000040000100020003040700800309002002070900080003000050000093000860100") #hard
        hardpuzzles.append("061030000050100700900000085004200003000000000200005400670000009009008060000090250") #hard
        hardpuzzles.append("800000010001200800090060047000017000307000405000530000150090080006003200070000003") #hard
        hardpuzzles.append("000000103001400002065700000000030807003080200507020000000006310600009400304000000") #hard

        puzzles = [easypuzzles,medpuzzles,hardpuzzles] # gather all puzzles together in a list [[easy],[medium],[hard]]
        random_num = random.randint(0, len(puzzles[puzzle_difficulty])-1) # select a random puzzle from the chosen difficulty

        return (puzzles[puzzle_difficulty][random_num])