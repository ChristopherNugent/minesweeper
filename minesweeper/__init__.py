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

        self.board = [ [Tile(False) for i in range(y)] for j in range(x)]

        all_coords = list(itertools.product(range(x), range(y)))
        random.shuffle(all_coords)

        for mine_tile in all_coords[:num_mines]:
            i, j = mine_tile
            self.board[i][j].mine = True


    def check_single(self, x, y) -> bool:
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
                            if self._in_bounds(x + i, y + j)
                               and self.board[x + i][y + j].mine])
        self.board[x][y].adjacent = mines_nearby
        return True


    def check(self, x, y):
        potentials = []
        potentials.append((x,y))
        while potentials:
            x, y = potentials.pop()
            self.check_single(x, y)
            if self.board[x][y].adjacent == 0:
                adjacent = [(x + i, y + j) for i, j in 
                            itertools.product(range(-1, 2), range(-1, 2))
                            if self._checkable(x + i, y + j)]
                potentials.extend(adjacent)


    def _in_bounds(self, x, y) -> bool:
        return not (x < 0 or y < 0 or x >= self.x or y >= self.y)

    def _checkable(self, x, y) -> bool:
            return self._in_bounds(x,y) and not self.board[x][y].checked
                
    def _fill_adjacents(self):
        all_coords = itertools.product(range(self.x), range(self.y))

        for x, y in all_coords:
            offsets = itertools.product(range(-1, 2), range(-1, 2))
            mines_nearby = sum([1 for i, j in offsets 
                                if self._in_bounds(x + i, y + j)
                                   and self.board[x + i][y + j].mine])
            self.board[x][y].adjacent = mines_nearby

    def to_string(self, show=False) -> str:
        return "\n".join([' '.join([self.board[x][y].to_string(show) 
               for x in range(self.x)]) 
               for y in range(self.y)])



    def __str__(self):
        return self.to_string()