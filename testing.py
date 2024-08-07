import random
import traceback

import tic_tac_toe

random_numbers = [random.randint(-10 ** 6, 10 ** 6) for _ in range(3)]

for i in random_numbers:
    random.seed(i)

    try:
        game = tic_tac_toe.GameState()
        game.running = False
        players = [tic_tac_toe.Medium('X', game), tic_tac_toe.Medium('O', game)]

        game.play(players)

        if game.win('O'):
            raise ValueError("hard lost")

    except Exception:
        print("WIR HABEN EIN PROBLEM", i)
        print(traceback.format_exc())
        break

else:
    print('Kein Problem')
