import random
import time


class GameState:
    def __init__(self):
        self.on = True
        self.state_table = [[' '] * SIZE for _ in range(SIZE)]
        self.free_cells = [[i + 1, j + 1] for i in range(SIZE) for j in range(SIZE)]

    def put(self, cell_x, cell_y, symbol):
        self.state_table[cell_x][cell_y] = symbol

    def get(self, cell_x, cell_y):
        if 0 <= cell_x < SIZE and 0 <= cell_y < SIZE:
            return self.state_table[cell_x][cell_y]
        else:
            return ' '


class User:
    name = 'user'

    def __init__(self, symbol):
        self.symbol = symbol

    def move(self):
        while True:
            coords = input('Enter the coordinates: ')
            try:
                x, y = map(int, coords.split())
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
    name = 'easy'

    def __init__(self, symbol):
        self.symbol = symbol

    def coordinates(self):
        return random.choice(game.free_cells)

    def move(self):
        print(f'Making move level "{self.name}"')

        start_time = time.monotonic()
        coords = self.coordinates()
        finish_time = time.monotonic()

        thinking_time = finish_time - start_time
        sleep_time = 0.9
        if thinking_time < sleep_time:
            time.sleep(sleep_time - thinking_time)

        return coords


class Medium(Easy):
    name = 'medium'

    def search_win(self, state_table, symbol):
        for i, j in game.free_cells:
            state_table[i - 1][j - 1] = symbol
            if win(state_table, symbol):
                state_table[i - 1][j - 1] = ' '
                return i, j
            else:
                state_table[i - 1][j - 1] = ' '

    def coordinates(self):
        other_symbol = next(s for s in symbols if s != self.symbol)

        win_medium = self.search_win(game.state_table, self.symbol)
        not_lose_medium = self.search_win(game.state_table, other_symbol)

        return win_medium or not_lose_medium or random.choice(game.free_cells)


class Hard(Easy):
    name = 'hard'

    def end_game(self, state_table, free_cells):
        x_win = win(state_table, 'X')
        o_win = win(state_table, 'O')
        draw = len(free_cells) == 0

        if x_win or o_win or draw:
            return True

        return False

    def score(self, state_table, depth):
        if win(state_table, self.symbol):
            return POINTS

        other_symbol = next(s for s in symbols if s != self.symbol)
        if win(state_table, other_symbol):
            return depth - POINTS

        return 0

    def minimax(self, state_table, free_cells, depth):
        if self.end_game(state_table, free_cells):
            return self.score(state_table, depth), None

        scores = []

        for cell in free_cells:
            state_table[cell[0] - 1][cell[1] - 1] = symbols[(len(free_cells) + 1) % 2]
            copy_free_cells = free_cells.copy()
            copy_free_cells.remove(cell)
            cur_scores, _ = self.minimax(state_table, copy_free_cells, depth + 1)
            scores.append(cur_scores)
            state_table[cell[0] - 1][cell[1] - 1] = ' '

        if symbols[(len(free_cells) + 1) % 2] == player.symbol:
            max_score = max(scores)
        else:
            max_score = min(scores)

        max_indices = [idx for idx in range(len(scores)) if scores[idx] == max_score]
        coords = free_cells[random.choice(max_indices)]

        return max_score, coords

    def coordinates(self):
        _, coords = self.minimax(game.state_table, game.free_cells, 0)
        return coords


def illustrate(state_table):
    print('---' * SIZE)
    for i in range(SIZE):
        print('|', end=' ')
        for j in range(SIZE):
            print(state_table[i][j], end=' ')
        print('|')
    print('---' * SIZE)


def check_move(coordinates, symbol):
    x, y = coordinates
    game.state_table[x - 1][y - 1] = symbol
    game.free_cells.remove([x, y])

    illustrate(game.state_table)

    won = win(game.state_table, symbol)
    if won or len(game.free_cells) == 0:
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


def create_player(name, symbol):
    return available_players[name](symbol)


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
                return list(map(create_player, names, symbols))

        print('Bad parameters!')


SIZE = 3
POINTS = 10
available_players = {'user': User, 'easy': Easy, 'medium': Medium, 'hard': Hard}
symbols = ['X', 'O']


if __name__ == '__main__':

    while True:
        game = GameState()
        players = first_command()

        # game.state_table = [['X', ' ', 'X'], ['X', 'O', 'O'], ['O', ' ', 'X']]
        # game.free_cells = [[i + 1, j + 1] for i in range(3) for j in range(3) if game.state_table[i][j] == ' ']

        illustrate(game.state_table)

        while game.on:
            player = players[(len(game.free_cells) + 1) % 2]

            coordinates = player.move()
            game.on = check_move(coordinates, player.symbol)
