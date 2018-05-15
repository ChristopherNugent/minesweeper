from __init__ import *

if __name__ == '__main__':
    print('Welcome to Minesweeper!')

    while True:
        try:
            x = int(input('Enter X size: '))
            y = int(input('Enter Y size: '))
            m = int(input('Enter number of mines: '))
            g = Game(x, y, m)
        except Exception:
            print('Something went wrong...')
            continue
        break

    while g.alive:
        if g.game_won():
            print(g.to_str(show=True))
            print('You won the game!')
            break
        print(g)
        try:
            x = int(input('Enter X of guess (0 - {}): '.format(g.x - 1)))
            y = int(input('Enter Y of guess (0 - {}): '.format(g.y - 1)))
            g.check(x, y)
        except Exception:
            print('Something went wrong...')
            continue
        print('\n')
