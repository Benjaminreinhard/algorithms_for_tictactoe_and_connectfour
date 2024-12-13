'''Game tree info

This file can be run to receive information on the game tree.

	Below you can specify a parameter 'prun' which can be either 'True' or 'False'.
	If you choose 'True' and run the file, you will see in the console the info of a
	pruned game tree according to the Alpha-beta pruning algorihm. If you choose 'False',
	then you will see the info of a non-pruned game tree.

	Also, you can specify a parameter 'depth' which is a natural number and says up to
	what depth the game tree should be travered.

The function 'Phi' traverses the game tree.
'''


import random

from math import inf as infinity
from sys import getsizeof

from game import ConnectFour


def Phi(game, V, alpha, beta, prun, depth):
	state = []
	for row in game.board:
		state += row
	state = tuple(state)

	if game.terminated:
		if game.winner == 'x':
			V[state] = 1
			return 1, 1, 1
		elif game.winner == 'o':
			V[state] = -1
			return -1, 1, 1
		else:
			V[state] = 0
			return 0, 1, 1
	elif depth == 0:
		if game.player == 1:
			v = 0.5
			V[state] = v
			return v, 1, 1
		else:
			v = -0.5
			V[state] = v
			return v, 1, 1
	else:
		if game.player == 1:
			v = -infinity
			count1 = 0
			count2 = 0
			for action in game.legal_actions():
				game.execute(action)
				e, c1, c2 = Phi(game, V, alpha, beta, prun, depth-1)
				v = max(v, e)
				count1 += c1
				count2 += c2
				if prun:
					alpha = max(alpha,e)
					if alpha >= beta:
						game.undo(action)
						break
				game.undo(action)
			V[state] = v
			return v, count1 + 1, count2
		else:
			v = infinity
			count1 = 0
			count2 = 0
			for action in game.legal_actions():
				game.execute(action)
				e, c1, c2 = Phi(game, V, alpha, beta, prun, depth-1)
				v = min(v, e)
				count1 += c1
				count2 += c2
				if prun:
					beta = min(beta, e)
					if alpha >= beta:
						game.undo(action)
						break
				game.undo(action)
			V[state] = v
			return v, count1 + 1, count2


# Initialize game
connectfour = ConnectFour(6, 7)


# Set algorithm parameters
prun = True
depth = 8


# Print info
print('Game tree info of', connectfour.name, 'with root node:', connectfour.board)
print('prun:', prun, ' | depth:', depth)
print()

V = {}
value_of_empty_board, number_of_nodes, number_of_leaves = Phi(connectfour, V, -infinity, infinity, prun, depth)
number_of_boards = len(V)
size = getsizeof(V)

print('Value of root node:', value_of_empty_board)
print()
print('Number of visited nodes:', number_of_nodes)
print('Number of visited leaves:', number_of_leaves)
print('Number of visited boards:', number_of_boards)
print()
print('Memory size of V:', size, 'bytes whis is around', round(size/1000000, 1), 'megabyte')