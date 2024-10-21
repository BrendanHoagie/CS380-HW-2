from enum import Enum
from connect3 import State, Action

DEFAULT_STATE = "    | XXX|OOXO"


class TokenType(Enum):
    XTOKEN = "X"
    OTOKEN = "O"


class Player:

    def __init__(
        self, token: TokenType = TokenType.XTOKEN, state: State = State(DEFAULT_STATE)
    ) -> None:
        self._token = token
        self._state = state

    def choose_action(self, state: State) -> Action:
        """Choose what action should be taken

        Args:
            state: a State representing the current board state

        Returns:
            an Action representing the chosen action
        """
        pass

    def set_state(self, new_state: State) -> None:
        """Sets the new board state

        Args:
            new_state: a State representing the new board state
        """
        self._state = new_state

    def get_state(self) -> State:
        """Gets the current board state

        Returns:
            a State representing the board state
        """
        return self._state

    def set_token(self, new_token: TokenType) -> None:
        """Sets the new token type

        Args:
            new_token: a TokenType representing the token this player will use
        """
        self._token = new_token

    def get_token(self) -> TokenType:
        """Gets the current token

        Returns:
            a TokenType representing the player's current token
        """
        return self._token


class Game:

    def __init__(self, player_one: Player, player_two: Player, state: State) -> None:
        self._player_one = player_one
        self._player_two = player_two
        self._game_state = state

    def play(self) -> None:
        """Simulates a game between two players.
        Runs until the game is over and prints out the winner if there is one
        """
        while not self._game_state.is_game_over():
            self._game_state.execute(self._player_one.choose_action(self._game_state))
            self._game_state.execute(self._player_two.choose_action(self._game_state))
        winner = self._game_state.get_winner()
        if winner:
            print(f"{winner} is the winner!")
            return
        print(f"Draw!")
