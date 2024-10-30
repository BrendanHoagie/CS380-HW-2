from game import Game, TokenType, DEFAULT_STATE
from agent import RandomPlayer, MinimaxPlayer, MinimaxAlphaBetaPlayer
from human import HumanPlayer
import util

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
    "minimaxalphabeta": [
        MinimaxAlphaBetaPlayer,
        "A computer player that uses the minimax algorithm with alpha beta pruning to make decisions.",
    ],
}


def handle_cli_error(s: str = None) -> None:
    """Fail gracefully if you get a CLI error

    Args:
        s: a String representing the incorrectly input player type.
        If s is None, it means there was an incorrect usage (eg python main.py)
    """
    if s != None:
        print(f"Error - {s} is not a valid player type")
    else:
        print(f"Unrecognized use. Usage: python main.py <player1> <player2>")
    print("All valid player types:")
    for k, v in players.items():
        print(f"{k:17}{'-':4}{v[1]}")
    exit(1)


if __name__ == "__main__":
    if not (p1_arg := util.get_arg(1)) or not (p2_arg := util.get_arg(2)):
        handle_cli_error()
    try:
        p1_controller = players[p1_arg.lower()][0]
    except KeyError:
        handle_cli_error(p1_arg)

    try:
        p2_controller = players[p2_arg.lower()][0]
    except KeyError:
        handle_cli_error(p2_arg)

    game = Game(
        p1_controller(TokenType.XTOKEN, DEFAULT_STATE),
        p2_controller(TokenType.OTOKEN, DEFAULT_STATE),
    )
    winner, moves = game.play()
    if not winner:
        print(f"The game is a draw!")
        util.pprint(moves)
        exit(0)
    print(f"{winner} wins the game!")
    util.pprint(moves)
