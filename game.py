import random
import os

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLORAMA = True
    COLORS = {
           0: Fore.WHITE,
           2: Fore.GREEN,
           4: Fore.BLUE + Style.BRIGHT,
           8: Fore.CYAN,
          16: Fore.RED,
          32: Fore.MAGENTA,
          64: Fore.CYAN,
         128: Fore.BLUE + Style.BRIGHT,
         256: Fore.MAGENTA,
         512: Fore.GREEN,
        1024: Fore.RED,
        2048: Fore.YELLOW,
        # For overacheivers like August
        4096: Fore.MAGENTA,
        8192: Fore.CYAN,
    }
except:
    COLORAMA = False
    print "\033[93mNOTE: in order for text to be colored, you must install 'termred' from PyPI\033[0m\n"

class InvalidMoveError(Exception):
    '''
    Raised by Game.shiftLeft or Game.shiftRight if the move
    did not change anything
    '''
    pass

class Game(object):
    def __init__(self, size=4, prob=.9, goal=2048, numStartTiles=2):
        '''
        Initializes the game with a board size x size big with numStartTiles
        tiles to begin

        w - width of the board
        h - height of the board
        prob - probability of spawning a 2 over a 4
        goal - the number used check if the game is won
        numStartTiles - the number of tiles to begin with
        '''
        self.size = size
        self.board = [[0 for a in range(size)] for b in range(size)]
        self.score = 0
        self.prob = prob
        self.goal = goal
        for i in range(numStartTiles):
            self.addTile()

    def reset(self, numStartTiles=2):
        '''
        Resets the game - board is cleaned and score is set to
        0 - and adds numStartTiles to the board
        '''
        self.board = [[0 for a in range(self.size)] for b in range(self.size)]
        self.score = 0
        for i in range(numStartTiles):
            self.addTile()

    def loop(self):
        '''
        Main loop for the game
        '''
        os.system('cls' if os.name == 'nt' else 'clear')
        self.printBoard()
        while not self.isOver():
            try:
                move = raw_input("Slide: ").lower()
                if move == 'exit':
                    break
                elif move == '':
                    pass
                elif move == 'elite haxor':
                    self.addTile()
                else:
                    self.slide(move)
                os.system('cls' if os.name == 'nt' else 'clear')
                self.printBoard()
            except InvalidMoveError:
                print 'Invalid Move.'
        if self.isWon():
            print 'You win!'
        elif not self.canMove():
            print 'Game over.'
        print 'Final Score:', self.getScore()

    def isWon(self):
        '''
        Sees if self.goal is on the board

        returns: True if the game is won, else False
        '''
        for row in self.board:
            if self.goal in row:
                return True
        return False

    def canMove(self):
        '''
        Sees if there is a possible move that you can make

        returns: list of possible moves if there is at least
                 one move available, else False
        '''
        invertedBoard = self.invert(self.board)
        possibleMoves = []
        if self.shiftLeft(self.board) != self.board or self.mergeLeft(self.board, 0)[0] != self.board:
            possibleMoves.append('left')
        if self.shiftRight(self.board) != self.board or self.mergeRight(self.board, 0)[0] != self.board:
            possibleMoves.append('right')
        if self.shiftLeft(invertedBoard) != invertedBoard or self.mergeLeft(invertedBoard, 0)[0] != invertedBoard:
            possibleMoves.append('up')
        if self.shiftRight(invertedBoard) != invertedBoard or self.mergeRight(invertedBoard, 0)[0] != invertedBoard:
            possibleMoves.append('down')
        return possibleMoves if possibleMoves else False


    def isOver(self):
        '''
        Sees if the game is won or if no move is possible

        returns: True if the game is over, else False
        '''
        if self.isWon() or not self.canMove():
            return True
        return False

    def getScore(self):
        '''
        returns: the current score of the game
        '''
        return self.score

    def printBoard(self):
        '''
        Prints the current board in a pretty array fashion
        '''
        for rowIndex in range(len(self.board)):
            for val in self.board[rowIndex]:
                if COLORAMA:
                    print '{0}{1:<6}'.format(COLORS[val], val),
                else:
                    print '{:<6}'.format(val),
            if rowIndex == 0:
                print "\tScore:",self.getScore(),
            print

    def getEmptyTiles(self):
        '''
        returns: a list of all of the coordinates of empty tiles
        on the board
        '''
        emptyTiles = []
        for rowNum in range(len(self.board)):
            for colNum in range(len(self.board[rowNum])):
                if not self.board[rowNum][colNum]:
                    emptyTiles.append((rowNum, colNum))
        return emptyTiles

    def addTile(self, loc=None):
        '''
        Places a tile at loc if loc given, or else it places one
        in a random empty tile

        loc - tuple formatted (row, col)
        '''
        try:
            row, col = random.choice(self.getEmptyTiles())
            self.board[row][col] = 2 if random.random() < self.prob else 4
            return True
        except:
            return False

    @staticmethod
    def shiftLeft(board):
        '''
        Moves every element in the board all the way to the LEFT

        returns: new board with elements shifted LEFT
        '''
        newBoard = [filter(lambda x: x!=0, row) for row in board]
        for row in newBoard:
            while len(row) != len(newBoard):
                row.append(0)
        return newBoard

    @staticmethod
    def shiftRight(board):
        '''
        Moves every element in the board all the way to the RIGHT

        returns: new board with elements shifted RIGHT
        '''
        newBoard = [filter(lambda x: x!=0, row) for row in board]
        for row in newBoard:
            while len(row) != len(newBoard):
                row.insert(0, 0)
        return newBoard

    @staticmethod
    def mergeLeft(board, score):
        '''
        Merges identical values favoring the LEFT

        returns: the new board, new score
        '''
        currentScore = score
        newBoard = [row[:] for row in board]
        for row in newBoard:
            for i in range(len(row)-1):
                if row[i] == row[i+1]:
                    currentScore += row[i]*2
                    row[i] = row[i]*2
                    row[i+1] = 0
        return newBoard, currentScore

    @staticmethod
    def mergeRight(board, score):
        '''
        Merges identical values favoring the RIGHT

        returns: the new board, new score
        '''
        currentScore = score
        newBoard = [row[:] for row in board]
        for row in newBoard:
            for i in range(len(row)-1)[::-1]:
                if row[i] == row[i+1]:
                    currentScore += row[i]*2
                    row[i+1] = row[i+1]*2
                    row[i] = 0
        return newBoard, currentScore

    @staticmethod
    def invert(board):
        '''
        Inverts the board - makes number at (x, y) at (y, x) -
        in order to used shiftLeft/Right and mergeLeft/Right to
        slide up and down

        returns: inverted board
        '''
        newBoard = []
        for i in range(len(board)):
            newBoard.append([row[i] for row in board])
        return newBoard

    def slide(self, direction, addTile=True):
        '''
        Makes a move in the game and adds a tile if addTile is
        True

        returns: True if a move was made, else False
        '''
        compareBoard = [row[:] for row in self.board]
        if direction == 'left' or direction == 'l':
            self.board = self.shiftLeft(self.board)
            self.board, self.score = self.mergeLeft(self.board, self.score)
            self.board = self.shiftLeft(self.board)
        elif direction == 'right' or direction == 'r':
            self.board = self.shiftRight(self.board)
            self.board, self.score = self.mergeRight(self.board, self.score)
            self.board = self.shiftRight(self.board)
        elif direction == 'up' or direction == 'u':
            invertedBoard = self.invert(self.board)
            invertedBoard = self.shiftLeft(invertedBoard)
            invertedBoard, self.score = self.mergeLeft(invertedBoard, self.score)
            invertedBoard = self.shiftLeft(invertedBoard)
            self.board = self.invert(invertedBoard)
        elif direction == 'down' or direction == 'd':
            invertedBoard = self.invert(self.board)
            invertedBoard = self.shiftRight(invertedBoard)
            invertedBoard, self.score = self.mergeRight(invertedBoard, self.score)
            invertedBoard = self.shiftRight(invertedBoard)
            self.board = self.invert(invertedBoard)
        if compareBoard != self.board and addTile:
            self.addTile()
        elif addTile:
            raise InvalidMoveError