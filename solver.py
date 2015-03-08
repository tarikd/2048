# -*- coding: utf-8 -*-

import game
from time import sleep
from os import system
import copy
from scipy import array

class SimpleAI(game.Game):
	def __init__(self, r, *args):
		'''
		Initializes the AI object using game.Game's __init__
		function.

		r - ratio for heuristic function
		*args - all other arguments for the creation of the game
		'''
		self.r = r
		game.Game.__init__(self, *args)
		self.testGame = game.Game(*args)

	def value(self, board):
		'''
		Calculates the 'value' of the board based on the ratio
		the board given

		returns: heuristic value for the board
		'''
		r = 1
		hScore = 0
		for rowIndex in range(len(board)):
			row = board[rowIndex] if rowIndex%2 == 0 else board[rowIndex][::-1] 
			for val in row:
				hScore += r*val
				r *= self.r
		return hScore

	def getBestMove(self, board):
		'''
		Determines the optimal move based on the value function

		returns: direction of optimal move
		'''
		self.testGame.board = board
		bestMove = None
		bestH = 0
		for move in self.testGame.canMove():
			self.testGame.board = board
			self.testGame.score = 0
			self.testGame.slide(move, addTile=False)
			if (self.value(self.testGame.board) + self.testGame.score) > bestH:
				bestH = (self.value(self.testGame.board) + self.testGame.score)
				bestMove = move
		return bestMove

	def loop(self, printBoard=False):
		'''
		Overwrites the loop function in game.Game to fit the
		playstyle of the AI
		'''
		while not self.isOver():
			#print self.getBestMove(self.board)
			#self.slide(self.getBestMove(self.board))
			

			# self.slide(self.nextMove(self.board, 4))
			# print self.gradient(self.board)
			
			#print self.playerMax(self.board, 4)
			self.slide(self.playerMax(self.board, 4)[0])

			# system('clear')
			self.printBoard()
			# sleep(.5)
		if printBoard: self.printBoard() 

	def simPlay(self, numTrials):
		'''
		Plays a 2048 game from start to finish numTrials times
		and prints the max, min, and average score
		'''
		try:
			scores = []
			for i in range(numTrials):
				if i%100 == 0:
					print i
				self.reset()
				self.loop()
				scores.append(self.score)
				if self.isWon():
					print '>>>>>>>>>>>   Winner Winner   <<<<<<<<<<<'
					self.printBoard()
					scores.append(self.score)
					break
			print 'Max Score:', max(scores)
			print 'Min Score:', min(scores)
			print 'Average Score:', sum(scores)/len(scores)
		except KeyboardInterrupt:
			print 'Max Score:', max(scores)
			print 'Min Score:', min(scores)
			print 'Average Score:', sum(scores)/len(scores)


	def gradient(self, board):
		'''
		Gradient
		'''

		tabHeurBottomRight = array([[-3,-2,-1,0]
			,[-2,-1,0,1]
			,[-1,0,1,2]
			,[0,1,2,3]])

		tabHeurTopRight = array([[0,1,2,3]
			,[-1,0,1,2]
			,[-2,-1,0,1]
			,[-3,-2,-1,0]])

		tabHeurTopLeft = array([[3,2,1,0]
			,[2,1,0,-1]
			,[1,0,-1,-2]
			,[0,-1,-2,-3]])

		tabHeurBottomLeft = array([[0,-1,-2,-3]
			,[1,0,-1,-2]
			,[2,1,0,-1]
			,[3,2,1,0]])

		tabHeur = [tabHeurBottomRight, tabHeurTopRight, tabHeurTopLeft, tabHeurBottomLeft]

		gradMax = 0
		for tabGrad in tabHeur:
			result = 0.0
			for i in range(0,4):
				for j in range(0,4):
					if board[i][j] != "      ":
						result += int(board[i][j])*int(tabGrad[i][j])

			gradMax = max(gradMax, result)

		return gradMax


	# NAIF
	def nextMove(self, board, depth):
		m, s = self.nextMoveRecur(board, depth, depth)
		return m

	def nextMoveRecur(self, board, depth, depthMax, base=0.9):
		bestScore = -1.
		bestMove = None
		possibleMoves = ["l","u","d","r"]
		self.testGame.board = board

		for move in self.testGame.canMove():
			self.testGame.board = board
			self.testGame.slide(move)
			score = self.gradient(self.testGame.board)
			if depth != 0:
				my_m, my_s = self.nextMoveRecur(self.testGame.board, depth-1, depthMax)
				score += my_s*pow(base, depthMax-depth+1)

			if score > bestScore:
				bestMove = move
				bestScore = score

		return bestMove, bestScore




	def playerMax(self, board, depth):
		'''
		Expectimax
		'''

		bestScore = -1
		bestMove = ""
		possibleMoves = ["l","u","d","r"]
		self.testGame.board = board

		if depth == 0:
			return "A", self.calculeScorePosition(self.testGame.board)

		for move in self.testGame.canMove():
			score = 0
			self.testGame.board = board
			self.testGame.slide(move)

			score += self.playerExpect(self.testGame.board, depth-1)

			if score >= bestScore:
				bestMove = move
				bestScore = score

		return bestMove, bestScore


	def playerExpect(self, board, depth):
		totalScore = 0
		totalWeight = 0
		probability = 0
		listPositionAvailable = self.testGame.getEmptyTiles()
		self.testGame.board = board

		for position in listPositionAvailable:
			self.testGame.board = board
			val = self.testGame.addTile(position)
			move, score = self.playerMax(self.testGame.board, depth-1)

			if val == "2":
				probability = 0.9
			else:
				probability = 0.1
			
			totalScore += score*probability
			totalWeight += probability

		if totalWeight != 0:
			return totalScore/totalWeight
		else:
			return 0


	def calculScoreH2_1(self, board):
		result = 0
		self.testGame.board = board

		result += self.gradient(self.testGame.board)
		
		nbFreeTitle = len(self.testGame.getEmptyTiles())

		result += -(16-nbFreeTitle)**2

		return result



	def calculeScorePosition(self, board, r=0.25):
		tabHeur = array([[13,12,5,4]
						,[14,11,6,3]
						,[15,10,7,2]
						,[16,9,8,1]])


		result = 0.0

		for i in range(0,4):
			for j in range(0,4):
				if board[i][j] != "":
					result += int(board[i][j])*r**int(tabHeur[i][j])

		return result































	# def getBestMove2(self, board):
	# 	'''
	# 	Determines the optimal move based on the value function

	# 	returns: direction of optimal move
	# 	'''
	# 	self.testGame.board = board
	# 	bestMove = None
	# 	bestH = 0
	# 	for move in self.testGame.canMove():
	# 		self.testGame.board = board
	# 		self.testGame.score = 0
	# 		self.testGame.slide(move, addTile=False)
	# 		print self.gradient(self.testGame.board) + self.testGame.score
	# 		if (self.gradient(self.testGame.board) + self.testGame.score) > bestH:
	# 			bestH = (self.gradient(self.testGame.board) + self.testGame.score)
	# 			bestMove = move
	# 	return bestMove














'''
	def playerBestScore(self, board, depth):
		if depth == 0:
			if self.canMove():
				return self.value(board)
			else:
				return 0

		bestScore = -1
		bestDirection = -1

		for move in self.canMove():
			score = computerAverageScore(board, depth-1)

			if score == bestScore:
				bestScore = score
				bestDirection = direction

		return bestScore, bestDirection


	def computerAverageScore(self, board, depth):
		totalScore = 0
		totalWeight = 0

		for 





function computer_average_score(grid, depth){
    total_score = 0;
    total_weight = 0;
 
    foreach (next_grid in grid.add_tile_possibilities){
        // The above exhausts all possible randomly added tiles
 
        // Recursion to player_best_score (defined above)
        score = player_best_score(next_grid, depth - 1).score; 
 
        // Takes weighted average
        total_score += score * next_grid.probability;
        total_weight += next_grid.probability;
    }
 
    return total_score / total_weight;
}


'''



# class DigDeeperAI(SimpleAI):
# 	def __init__(self, *args):
# 		SimpleAI.__init__(self, *args)

# 	def loop(self, printBoard=False):
# 		while not self.isOver():
# 			bestMove = None
# 			bestH = 0
# 			for move in self.canMove():
# 				self.testGame.board = self.board
# 				self.testGame.slide(move, addTile=False)
# 				m = self.getBestMove(self.testGame.board)
# 				self.testGame.slide(m, addTile=False)
# 				# print move, m, self.value(self.testGame.board), bestH
# 				if self.value(self.testGame.board) > bestH:
# 					bestH = self.value(self.testGame.board)
# 					bestMove = move
# 			# print bestMove
# 			self.slide(bestMove)
# 			sleep(.5)
# 			system('clear')
# 			self.printBoard()
# 			# print self.value(self.board)
# 		if printBoard: self.printBoard()


"""
	def nextMove(self, board, recursion_depth=3):
		self.testGame.board = board
		m, s = self.nextMoveRecur(board, recursion_depth, recursion_depth)
		return m

	def nextMoveRecur(self, board, depth, maxDepth, base=0.9):
		self.testGame.board = board
		bestScore = -1.
		bestMove = 0
		moves = ['up', 'left', 'right', 'down']
		for m in moves:
			if m in self.testGame.canMove():
				newBoard = copy.deepcopy(board)
				print newBoard
				newBoard.slide(m, add_tile=True)

				score = self.testGame.score
				if depth != 0:
					my_m, my_s = self.nextMoveRecur(newBoard,depth-1,maxDepth)
					score += my_s*pow(base,maxDepth-depth+1)

				if(score > bestScore):
					bestMove = m
					bestScore = score
		return (bestMove, bestScore);


	def loop2(self, printBoard=False):
		'''
		Overwrites the loop function in game.Game to fit the
		playstyle of the AI
		'''
		while not self.isOver():
			#print self.getBestMove(self.board)
			self.slide(self.nextMove(self.board))
			# system('clear')
			self.printBoard()
			# sleep(.5)
		if printBoard: self.printBoard() 
"""