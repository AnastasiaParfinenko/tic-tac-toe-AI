def create_table(state):
    global count_moves, size

    state_table = [[' '] * size for _ in range(size)]

    for i in range(size):
        for j in range(size):
            if state[i * size + j] != '_':
                state_table[i][j] = state[i * size + j]
                count_moves += 1

    return state_table


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


def illustrate(state_table):
    print('---' * size)
    for i in range(size):
        print('|', end=' ')
        for j in range(size):
            print(state_table[i][j], end=' ')
        print('|')
    print('---' * size)


def move(coordinates, symbol):
    global count_moves

    try:
        x, y = map(int, coordinates.split())
    except Exception:
        print('You should enter numbers!')
    else:
        if not (x in range(1, size + 1) and y in range(1, size + 1)):
            print(f'Coordinates should be from 1 to {size}!')
        elif state_table[x - 1][y - 1] == ' ':
            state_table[x - 1][y - 1] = symbol
            illustrate(state_table)

            count_moves += 1
            free_cells.remove(f'{x} {y}')

            return True
        else:
            print('This cell is occupied! Choose another one!')


def easy_move(symbol):
    import random
    import time

    coordinates = random.choice(free_cells)
    print('Making move level "easy"')
    time.sleep(0.9)
    move(coordinates, symbol)


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


size = 3

count_moves = 0

initial_state = '_' * size ** 2
free_cells = [f'{i + 1} {j + 1}' for i in range(size) for j in range(size)]

state_table = create_table(initial_state)
illustrate(state_table)

game = True

while game:
    symbol = 'X' if count_moves % 2 == 0 else 'O'

    if symbol == 'X':
        coordinates = input('Enter the coordinates: ')
        while not move(coordinates, symbol):
            coordinates = input('Enter the coordinates: ')
    else:
        easy_move(symbol)

    won = win(state_table, symbol)
    if won or count_moves == size ** 2:
        if won:
            print(f'{symbol} wins')
        else:
            print('Draw')
        game = False
        break
