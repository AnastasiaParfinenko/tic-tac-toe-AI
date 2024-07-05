# def state_analyze(state):
#     if abs(state.count('X') - state.count('O')) > 1 or (win(state, 'O') and win(state, 'X')):
#         print('Impossible')
#     elif win(state, 'O'):
#         print('O wins')
#     elif win(state, 'X'):
#         print('X wins')
#     elif state.count('_') == 0:
#         print('Draw')
#     else:
#         print('Game not finished')
#

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
                if not (x in range(1, size + 1) and y in range(1, size + 1)):
                    print(f'Coordinates should be from 1 to {size}!')
                elif state_table[x - 1][y - 1] == ' ':
                    return x, y
                else:
                    print('This cell is occupied! Choose another one!')


class Easy:
    name = 'Easy'

    def move(self):
        import random
        import time

        print('Making move level "easy"')
        time.sleep(0.9)

        return random.choice(free_cells)


def create_table(state):
    global count_moves

    state_table = [[' '] * size for _ in range(size)]

    for i in range(size):
        for j in range(size):
            if state[i * size + j] != '_':
                state_table[i][j] = state[i * size + j]
                count_moves += 1

    return state_table


def illustrate(state_table):
    print('---' * size)
    for i in range(size):
        print('|', end=' ')
        for j in range(size):
            print(state_table[i][j], end=' ')
        print('|')
    print('---' * size)


# def easy_move(symbol):
#     import random
#     import time
#
#     coordinates = random.choice(free_cells)
#     print('Making move level "easy"')
#     time.sleep(0.9)
#     move(coordinates, symbol)

def check_move(coordinates, symbol):
    global count_moves
    count_moves += 1

    x, y = coordinates
    state_table[x - 1][y - 1] = symbol
    free_cells.remove([x, y])

    illustrate(state_table)

    won = win(state_table, symbol)
    if won or count_moves == size ** 2:
        if won:
            print(f'{symbol} wins')
        else:
            print('Draw')

        return False

    return True


def win(state_table, symbol):
    if any(all(state_table[i][j] == symbol for j in range(size)) for i in range(size)):
        return True
    if any(all(state_table[i][j] == symbol for i in range(size)) for j in range(size)):
        return True
    if all(state_table[i][i] == symbol for i in range(size)):
        return True
    if all(state_table[i][size - i - 1] == symbol for i in range(size)):
        return True

    return False


def first_command():
    import sys

    while True:
        command = input('Input command: ').lower()

        if command == 'exit':
            sys.exit()

        command = command.split()
        if len(command) == 3 and command[0] == 'start' and \
                command[1] in available_players and command[2] in available_players:
            return [create_player(command[i + 1]) for i in range(2)]
        else:
            print('Bad parameters!')


def create_player(name):
    if name == 'user':
        return User()
    if name == 'easy':
        return Easy()


size = 3
available_players = {'user', 'easy'}
symbols = ['X', 'O']

count_moves = 0

initial_state = '_' * size ** 2
free_cells = [[i + 1, j + 1] for i in range(size) for j in range(size)]

state_table = create_table(initial_state)

game = True

if __name__ == '__main__':
    while True:
        players = first_command()  # start user easy
        print(type(players[0]))
        print(type(players[1]))

        while game:
            for i in range(2):
                coordinates = players[i].move()
                symbol = symbols[i]
                game = check_move(coordinates, symbol)
