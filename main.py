from game import Game, TokenType
from agent import RandomPlayer, MinimaxPlayer
from human import HumanPlayer
import util

game = Game(None, None)
players = {
    "human": [
        HumanPlayer,
        "A human player. Will prompt for input given available moves and take input from stdin as an integer",
    ],
    "random": [
        RandomPlayer,
        "A computer player that choose a move at random to play.",
    ],
    "minimax": [
        MinimaxPlayer,
        "A computer player that uses the minimax algorithm to make decisions.",
    ],
}


def handle_cli_error(s: str = None):
    if s != None:
        print(f"Error - {s} is not a valid player type")
    else:
        print(f"Unrecognized use. Usage: python main.py <player1> <player2>")
    print("All valid player types:")
    for k, v in players.items():
        print(f"{k:9}{'-':4}{v[1]}")
    exit(1)


if __name__ == "__main__":
    if not (p1_arg := util.get_arg(1)) or not (p2_arg := util.get_arg(2)):
        handle_cli_error()
    try:
        p1_controller = players[p1_arg.lower()]
    except KeyError:
        handle_cli_error(p1_arg)

    try:
        p2_controller = players[p2_arg.lower()]
    except KeyError:
        handle_cli_error(p2_arg)

    game.set_player_one(p1_controller[0](TokenType.XTOKEN))
    game.set_player_two(p2_controller[0](TokenType.OTOKEN))
    winner, moves = game.play()
    if not winner:
        print(f"The game is a draw!")
        util.pprint(moves)
        exit(0)
    print(f"{winner} wins the game!")
    util.pprint(moves)
