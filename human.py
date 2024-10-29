from game import DEFAULT_STATE, Player, TokenType
from connect3 import State, Action


class HumanPlayer(Player):

    def __init__(
        self,
        token: TokenType = TokenType.XTOKEN,
        state: State = State(DEFAULT_STATE),
    ) -> None:
        super().__init__(token, state)

    def choose_action(self, state: State) -> Action:
        """Choose what action should be taken.
        Presents the user with a set of choices based on the current board state
        and polls them to choose a valid state from that list

        Args:
            state: a State representing the current board state

        Returns:
            an Action representing the chosen action
        """
        ret = 0
        actions = state.get_actions(self.get_token().value)
        for i, action in enumerate(actions):
            print(f"{i}: {action}")
        while True:
            try:
                ret = input(f"Please choose an action (a number 0-{i}): ")
            except EOFError:
                print("EOF, exiting.")
                exit(2)
            except KeyboardInterrupt:
                print("Keyboard Interrupt, exiting.")
                exit(2)
            if str.isnumeric(ret) and 0 <= int(ret) and int(ret) <= i:
                break
            print(f"Error - invalid choice. ", end="")
        return actions[int(ret)]
