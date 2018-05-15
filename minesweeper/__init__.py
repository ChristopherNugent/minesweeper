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

    def to_str(self, show: bool=False) -> str:
        if self.checked or show:
            if self.mine:
                return 'M'
            elif self.adjacent:
                return str(self.adjacent)
            else:
                return '.'
        else:
            return '-'

    def __str__(self):
        return self.to_str()


class Game:

    def __init__(self, x: int, y: int, num_mines: int):
        if x < 1 or y < 1:
            raise ValueError('No negative board sizes!')
        if num_mines > x * y:
            raise ValueError('Not enough space on board')
        if num_mines < 0:
            raise ValueError('Negative mines?')
        self.x = x
        self.y = y
        self.num_mines = num_mines
        self.alive = True
        self.revealed = 0

        self.board = [[Tile(False) for i in range(y)] for j in range(x)]

        all_coords = list(itertools.product(range(x), range(y)))
        random.shuffle(all_coords)

        for mine_tile in all_coords[:num_mines]:
            i, j = mine_tile
            self.board[i][j].mine = True

    def check(self, x: int, y: int):
        potentials = []
        potentials.append((x, y))
        while potentials:
            x, y = potentials.pop()
            self.check_single(x, y)
            if self.board[x][y].adjacent == 0:
                adjacent = [(x + i, y + j) for i, j in
                            itertools.product(range(-1, 2), range(-1, 2))
                            if self._checkable(x + i, y + j)]
                potentials.extend(adjacent)

    def check_single(self, x: int, y: int):
        if x < 0 or y < 0:
            raise ValueError('No negative coords')
        elif x > self.x or y > self.y:
            raise ValueError('Coords beyond board')
        if self.board[x][y].checked:
            return

        mine_clicked = self.board[x][y].check()
        if mine_clicked:
            self.alive = False
            return

        self.revealed += 1

        offsets = itertools.product(range(-1, 2), range(-1, 2))
        mines_nearby = sum([1 for i, j in offsets
                            if self._in_bounds(x + i, y + j)
                            and self.board[x + i][y + j].mine])
        self.board[x][y].adjacent = mines_nearby

    def _checkable(self, x: int, y: int) -> bool:
        return self._in_bounds(x, y) and not self.board[x][y].checked

    def _in_bounds(self, x: int, y: int) -> bool:
        return not (x < 0 or y < 0 or x >= self.x or y >= self.y)

    def game_won(self) -> bool:
        return self.revealed >= self.x * self.y - self.num_mines \
            or self.num_mines == 0

    def to_str(self, show=False) -> str:
        if show:
            self._fill_adjacents()
        return "\n".join([' '.join([self.board[x][y].to_str(show)
                                    for x in range(self.x)])
                          for y in range(self.y)])

    def _fill_adjacents(self):
        all_coords = itertools.product(range(self.x), range(self.y))

        for x, y in all_coords:
            offsets = itertools.product(range(-1, 2), range(-1, 2))
            mines_nearby = sum([1 for i, j in offsets
                                if self._in_bounds(x + i, y + j)
                                and self.board[x + i][y + j].mine])
            self.board[x][y].adjacent = mines_nearby

    def __str__(self):
        return self.to_str(show=False)
