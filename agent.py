from game import DEFAULT_STATE, Player, TokenType
from connect3 import State, Action
import random
import sys


class RandomPlayer(Player):

    def __init__(
        self,
        token: TokenType = TokenType.XTOKEN,
        state: State = State(DEFAULT_STATE),
    ) -> None:
        super().__init__(token, state)

    def choose_action(self, state: State) -> Action:
        """Chooses what action should be taken at random

        Args:
            state: a State representing the current board state

        Returns:
            an Action representing the chosen action
        """
        actions = state.get_actions(self.get_token().value)
        return actions[random.randint(0, len(actions) - 1)]


class MinimaxPlayer(Player):

    def __init__(
        self,
        token: TokenType = TokenType.XTOKEN,
        state: State = State(DEFAULT_STATE),
    ) -> None:
        super().__init__(token, state)

    def choose_action(self, state: State) -> Action:
        best_action = None
        value = -sys.maxsize - 1
