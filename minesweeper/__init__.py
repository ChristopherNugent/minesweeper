import itertools
import random

class Tile:

	def __init__(self, mine: bool, checked: bool=False):
		self.mine = mine
		self.checked = checked
		self.adjacent = 0


	def check(self) -> bool:
		self.checked = True
		return self.mine


	def to_string(self, show: bool=False) -> str:
		if self.checked or show:
			return 'M' if self.mine else str(self.adjacent)
		else:
			return '?'


	def __str__(self):
		return self.to_string()


class Game:

	def __init__(self, x: int, y: int, num_mines: int):
		if num_mines > x * y:
			raise ValueError('Not enough space on board')
		self.x = x
		self.y = y
		self.num_mines = num_mines

		self.board = [ [Tile(False) for i in range(x)] for j in range(y)]

		all_coords = list(itertools.product(range(x), range(y)))
		random.shuffle(all_coords)

		for mine_tile in all_coords[:num_mines]:
			i, j = mine_tile
			self.board[i][j].mine = True


	def check(self, x, y) -> bool:
		if x < 0 or y < 0:
			raise ValueError('No negative coords')
		elif x > self.x or y > self.y:
			raise ValueError('Coords beyond board')

		mine_clicked = self.board[x][y].check()

		if mine_clicked:
			print('You lose!')
			return False

		# Update count
		offsets = itertools.product(range(-1, 2), range(-1, 2))
		mines_nearby = sum([1 for i, j in offsets 
			                if self.board[x - i][y - j].mine])
		self.board[x][y].adjacent = mines_nearby


	def to_string(self) -> str:
		return "\n".join([' '.join([str(self.board[x][y]) 
			   for x in range(self.x)]) 
		       for y in range(self.y)])

	def __str__(self):
		return self.to_string()