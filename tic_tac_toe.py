class GameState:
    def __init__(self):
        self.on = True
        self.state_table = [[' '] * SIZE for _ in range(SIZE)]
        self.count_moves = 0
        self.free_cells = [[i + 1, j + 1] for i in range(SIZE) for j in range(SIZE)]

    def put(self, cell_x, cell_y, symbol):
        self.state_table[cell_x][cell_y] = symbol

    def get(self, cell_x, cell_y):
        if 0 <= cell_x < SIZE and 0 <= cell_y < SIZE:
            return self.state_table[cell_x][cell_y]
        else:
            return ' '


class User:
    name = 'User'

    def move(self):
        while True:
            coordinates = input('Enter the coordinates: ')
            try:
                x, y = map(int, coordinates.split())
            except Exception:
                print('You should enter numbers!')
            else:
                if not (x in range(1, SIZE + 1) and y in range(1, SIZE + 1)):
                    print(f'Coordinates should be from 1 to {SIZE}!')
                elif game.state_table[x - 1][y - 1] != ' ':
                    print('This cell is occupied! Choose another one!')
                else:
                    return x, y


class Easy:
    name = 'Easy'

    def move(self):
        import random
        import time

        print('Making move level "easy"')
        time.sleep(0.9)

        return random.choice(game.free_cells)


def illustrate(state_table):
    print('---' * SIZE)
    for i in range(SIZE):
        print('|', end=' ')
        for j in range(SIZE):
            print(state_table[i][j], end=' ')
        print('|')
    print('---' * SIZE)


def check_move(coordinates, symbol):
    game.count_moves += 1

    x, y = coordinates
    game.state_table[x - 1][y - 1] = symbol
    game.free_cells.remove([x, y])

    illustrate(game.state_table)

    won = win(game.state_table, symbol)
    if won or game.count_moves == SIZE ** 2:
        if won:
            print(f'{symbol} wins')
        else:
            print('Draw')

        return False

    return True


def win(state_table, symbol):
    horizontals = any(all(state_table[i][j] == symbol for j in range(SIZE)) for i in range(SIZE))
    verticals = any(all(state_table[i][j] == symbol for i in range(SIZE)) for j in range(SIZE))
    diagonal1 = all(state_table[i][i] == symbol for i in range(SIZE))
    diagonal2 = all(state_table[i][SIZE - i - 1] == symbol for i in range(SIZE))

    return horizontals or verticals or diagonal1 or diagonal2


def first_command():
    import sys

    while True:
        command = input('Input command: ').lower()

        if command == 'exit':
            sys.exit()

        command = command.split()
        if len(command) == 3 and command[0] == 'start':
            names = command[1:3]
            if all(n in available_players for n in names):
                return [available_players[n] for n in names]

        print('Bad parameters!')


SIZE = 3
available_players = {'user': User(), 'easy': Easy()}
symbols = ['X', 'O']


if __name__ == '__main__':

    while True:
        game = GameState()
        players = first_command()  # start user easy

        illustrate(game.state_table)

        while game.on:
            # TODO: introduce symbol as an attribute of player
            assert len(players) == len(symbols) == 2
            player = players[game.count_moves % len(players)]
            symbol = symbols[game.count_moves % len(symbols)]

            coordinates = player.move()
            game.on = check_move(coordinates, symbol)
