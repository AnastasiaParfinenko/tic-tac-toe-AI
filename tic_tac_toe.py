# # size = int(input('Size of field?'))
#
# def create_list(state, size = 3):
#     state_list = [[0] * size for _ in range(size)]
#     for i in range(size):
#         for j in range(size):
#             if state[i * size + j] == '_':
#                 state_list[i][j] = ' '
#             else:
#                 state_list[i][j] = state[i * size + j]
#     return state_list
#
# def illustrate(state_table, size = 3):
#     print('---' * size)
#     for i in range(size):
#         print('|', end=' ')
#         for j in range(size):
#             print(state_table[i][j], end=' ')
#         print('|')
#     print('---' * size)
#
#
# def win(state, symbol):
#     for i in [0, 3, 6]:
#         if state[i] == state[i + 1] == state[i + 2] == symbol:
#             return True
#     for j in [0, 1, 2]:
#         if state[j] == state[j + 3] == state[j + 6] == symbol:
#             return True
#     if state[0] == state[4] == state[8] == symbol:
#         return True
#     if state[2] == state[4] == state[6] == symbol:
#         return True
#     return False
#
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
# def move(coordinates):
#     try:
#         x, y = map(int, coordinates.split())
#     except Exception:
#         print('You should enter numbers!')
#     else:
#         if not (x in [1, 2, 3] and y in [1, 2, 3]):
#             print('Coordinates should be from 1 to 3!')
#         elif state_table[x - 1][y - 1] == ' ':
#             state_table[x - 1][y - 1] = 'X'
#             illustrate(state_table)
#             return True
#         else:
#             print('This cell is occupied! Choose another one!')
#
# state = input()
# state_table = create_list(state)
# illustrate(state_table)
#
# coordinates = input()
# while not move(coordinates):
#     coordinates = input()
#
#

def illustrate(state_table, size=3):
    print('---' * size)
    for i in range(size):
        print('|', end=' ')
        for j in range(size):
            print(state_table[i][j], end=' ')
        print('|')
    print('---' * size)


def move(coordinates, symbol):
    try:
        x, y = map(int, coordinates.split())
    except Exception:
        print('You should enter numbers!')
    else:
        if not (x in [1, 2, 3] and y in [1, 2, 3]):
            print('Coordinates should be from 1 to 3!')
        elif state_table[x - 1][y - 1] == ' ':
            state_table[x - 1][y - 1] = symbol
            illustrate(state_table)
            return True
        else:
            print('This cell is occupied! Choose another one!')


def win(state_table, symbol):
    if any(all(state_table[i][j] == symbol for j in range(3)) for i in range(3)):
        return True
    if any(all(state_table[i][j] == symbol for i in range(3)) for j in range(3)):
        return True
    if all(state_table[i][i] == symbol for i in range(3)):
        return True
    if all(state_table[i][3 - i - 1] == symbol for i in range(3)):
        return True

    return False


state_table = [[' '] * 3 for _ in range(3)]
illustrate(state_table)

game = True
count = 0

while game:
    for symbol in ['X', 'O']:
        coordinates = input(f"{symbol}'s turn: ")
        while not move(coordinates, symbol):
            coordinates = input()
        count += 1

        won = win(state_table, symbol)
        if won or count == 3 ** 2:
            if won:
                print(f'{symbol} wins!')
            else:
                print('Draw!')
            game = False
            break
