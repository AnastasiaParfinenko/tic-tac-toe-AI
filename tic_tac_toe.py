import random
import time


class GameState:
    def __init__(self):
        self.state_table = [[' '] * SIZE for _ in range(SIZE)]
        self.free_cells = [(i + 1, j + 1) for i in range(SIZE) for j in range(SIZE)]
        self.interactive = True

    def put(self, coords, symbol):
        x, y = coords
        self.state_table[x - 1][y - 1] = symbol
        self.free_cells.remove(coords)

    def print_result(self):
        if self.check_win('O'):
            print('O wins')
        elif self.check_win('X'):
            print('X wins')
        elif len(self.free_cells) == 0:
            print('Draw')

    def check_win(self, symbol):
        horizontals = any(all(self.state_table[i][j] == symbol for j in range(SIZE)) for i in range(SIZE))
        verticals = any(all(self.state_table[i][j] == symbol for i in range(SIZE)) for j in range(SIZE))
        diagonal1 = all(self.state_table[i][i] == symbol for i in range(SIZE))
        diagonal2 = all(self.state_table[i][SIZE - i - 1] == symbol for i in range(SIZE))

        return horizontals or verticals or diagonal1 or diagonal2

    def is_end(self):
        x_win = self.check_win('X')
        o_win = self.check_win('O')
        draw = len(self.free_cells) == 0

        return x_win or o_win or draw

    def illustrate(self):
        print('---' * SIZE)
        for i in range(SIZE):
            print('|', end=' ')
            for j in range(SIZE):
                print(self.state_table[i][j], end=' ')
            print('|')
        print('---' * SIZE)

    def play(self, players):
        if self.interactive:
            self.illustrate()

        while not self.is_end():
            player = players[(len(self.free_cells) + 1) % 2]

            coordinates = player.get_coords()
            self.put(coordinates, player.symbol)

            if self.interactive:
                self.illustrate()

        if self.interactive:
            self.print_result()


class Player:
    name = 'player'

    def __init__(self, symbol, game):
        self.symbol = symbol
        self.game = game

    def move(self):
        raise NotImplementedError('Please Implement this method')

    def calc_coords(self):
        raise NotImplementedError('Please Implement this method')

    def get_coords(self):
        if self.game.interactive:
            return self.move()
        else:
            return self.calc_coords()


class User(Player):
    name = 'user'

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
                elif self.game.state_table[x - 1][y - 1] != ' ':
                    print('This cell is occupied! Choose another one!')
                else:
                    return x, y


class Easy(Player):
    name = 'easy'

    def calc_coords(self):
        return random.choice(self.game.free_cells)

    def move(self):
        print(f'Making move level "{self.name}"')

        start_time = time.monotonic()
        coords = self.calc_coords()
        finish_time = time.monotonic()

        thinking_time = finish_time - start_time
        sleep_time = 0.9
        if thinking_time < sleep_time:
            time.sleep(sleep_time - thinking_time)
        return coords


class Medium(Easy):
    name = 'medium'

    def search_win(self, symbol):
        for i, j in self.game.free_cells:
            self.game.state_table[i - 1][j - 1] = symbol
            if self.game.check_win(symbol):
                self.game.state_table[i - 1][j - 1] = ' '
                return i, j
            else:
                self.game.state_table[i - 1][j - 1] = ' '

    def calc_coords(self):
        other_symbol = next(s for s in symbols if s != self.symbol)

        win_medium = self.search_win(self.symbol)
        not_lose_medium = self.search_win(other_symbol)

        return win_medium or not_lose_medium or random.choice(self.game.free_cells)


class Hard(Easy):
    name = 'hard'

    def score(self, depth):
        if self.game.check_win(self.symbol):
            return POINTS - depth

        other_symbol = next(s for s in symbols if s != self.symbol)
        if self.game.check_win(other_symbol):
            return depth - POINTS

        return 0

    def minimax(self, depth):
        if self.game.is_end():
            return self.score(depth), None

        scores = []

        free_cells_original = self.game.free_cells
        for cell in free_cells_original:
            self.game.state_table[cell[0] - 1][cell[1] - 1] = symbols[(len(free_cells_original) + 1) % 2]

            new_free_cells = free_cells_original.copy()
            new_free_cells.remove(cell)
            self.game.free_cells = new_free_cells

            cur_score, _ = self.minimax(depth + 1)
            scores.append(cur_score)

            self.game.free_cells = free_cells_original
            self.game.state_table[cell[0] - 1][cell[1] - 1] = ' '

        if symbols[(len(free_cells_original) + 1) % 2] == self.symbol:
            max_score = max(scores)
        else:
            max_score = min(scores)

        max_indices = [idx for idx in range(len(scores)) if scores[idx] == max_score]
        coords = free_cells_original[random.choice(max_indices)]

        return max_score, coords

    def calc_coords(self):
        if len(self.game.free_cells) == 9:
            coords = random.choice(self.game.free_cells)
        else:
            _, coords = self.minimax(0)

        return coords


def create_player(name, symbol, game):
    return available_players[name](symbol, game)


def first_command(game):
    import sys

    while True:
        command = input('Input command: ').lower()

        if command == 'exit':
            sys.exit()

        command = command.split()
        if len(command) == 3 and command[0] == 'start':
            names = command[1:3]
            if all(n in available_players for n in names):
                return list(map(
                    lambda n, s: create_player(n, s, game),
                    names, symbols))

        print('Bad parameters!')


def create_list(state):
    state_list = [[' '] * SIZE for _ in range(SIZE)]
    for i in range(SIZE):
        for j in range(SIZE):
            if state[i * SIZE + j] != '_':
                state_list[i][j] = state[i * SIZE + j]
    return state_list


SIZE = 3
POINTS = 10
available_players = {'user': User, 'easy': Easy, 'medium': Medium, 'hard': Hard}
symbols = ['X', 'O']


def main():
    while True:
        game = GameState()
        players = first_command(game)

        game.play(players)


if __name__ == '__main__':
    main()
