from enum import Enum
from connect3 import State, Action
import util

DEFAULT_STATE = "   |   |   "


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

    def __init__(self, player_one: Player | None, player_two: Player | None) -> None:
        self._player_one = player_one
        self._player_two = player_two
        self._game_state = State(DEFAULT_STATE)
        self._moves = []

    def set_player_one(self, p1: Player) -> None:
        """Sets the player for player one

        Args:
            p1: a Player representing player one
        """
        self._player_one = p1

    def get_player_one(self) -> Player:
        """Gets the player one player

        Returns:
            a Player representing player one
        """
        return self._player_one

    def set_player_two(self, p2: Player) -> None:
        """Sets the player for player two

        Args:
            p2: a Player representing player two
        """
        self._player_two = p2

    def get_player_two(self) -> Player:
        """Gets the player two player

        Returns:
            a Player representing player two
        """
        return self._player_two

    def play(self) -> tuple:
        """Simulates a game between two players.
        Runs until the game is over, printing the board state at every step

        Returns:
            a Tuple (Str, List) where the Str represents the outcome and the List
            is a record of all played moves
        """
        player1_action = player2_action = last_action = None
        util.pprint(self._game_state)
        while not self._game_state.is_game_over():
            player1_action = self._player_one.choose_action(self._game_state)
            self._game_state = self._game_state.execute(player1_action)
            util.pprint(self._game_state)
            self._moves.append(self._game_state)
            if self._game_state.is_game_over():
                last_action = player1_action
                break
            player2_action = self._player_two.choose_action(self._game_state)
            self._game_state = self._game_state.execute(player2_action)
            util.pprint(self._game_state)
            self._moves.append(self._game_state)
            last_action = player2_action
        winner = self._game_state.get_winner()
        print(winner)
        if winner:
            if last_action == player1_action:
                return ("Player One", self._moves)
            return ("Player Two", self._moves)
        return (None, self._moves)
