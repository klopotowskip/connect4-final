from AIPlayer import AIPlayer

from game import Game


def announce_game(game_count):
    print("----------------------")
    print("Game {}".format(game_count))
    print("----------------------")


if __name__ == '__main__':

    game_cnt = 1
    announce_game(game_cnt)

    g = Game()
    ai = AIPlayer()

    while True:
        choice = input()
        if choice == "q":
            break
        if not choice.isdigit():
            print("Invalid move: \'" + choice + "\' (even not an int!) Try again!")
            continue

        legal = g.showLegalMoves()
        choice = int(choice)
        if legal.__contains__(choice):
            result = g.makeAMove(choice)
            if result:
                game_cnt += 1
                announce_game(game_cnt)
                g = Game()
                continue
        else:
            print("Invalid move! Try again!")
            continue

        result = ai.makeAMove(g)

        if result:
            game_cnt += 1
            announce_game(game_cnt)
            g = Game()
