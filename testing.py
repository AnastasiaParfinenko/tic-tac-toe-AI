import random
import traceback

import tic_tac_toe

random_numbers = [-827510]
# [random.randint(-10 ** 6, 10 ** 6) for _ in range(100)]

for i in random_numbers:
    random.seed(i)

    try:
        game = tic_tac_toe.GameState()
        players = [tic_tac_toe.Hard('X'), tic_tac_toe.Medium('O')]

        while game.on:
            player = players[(len(game.free_cells) + 1) % 2]

            coordinates = player.move()
            game.on = tic_tac_toe.check_move(coordinates, player.symbol)

        if tic_tac_toe.win(game.state_table, 'O'):
            raise ValueError("hard lost")

    except Exception as e:
        print("WIR HABEN EIN PROBLEM", i)
        traceback.print_exception(e)
