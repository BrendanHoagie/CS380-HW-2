from game import DEFAULT_STATE, Player, TokenType
from connect3 import State, Action
import random
import sys
import util
from enum import IntEnum


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


class Node:

    DEFAULT_VALUE = 0

    def __init__(
        self,
        state: State = None,
        parent=None,
        children: list = [],
        value: int = DEFAULT_VALUE,
    ) -> None:
        self._state = state
        # parents aren't type annotated, not allowed outside libraries incl. Self type from typing_extensions
        # a parent is either Node | None
        self._children = children
        self._parent = parent
        self._value = value

    def get_state(self) -> State:
        """Gets the node's current state

        Returns:
            a State representing the current board state
        """
        return self._state

    def get_children(self) -> list:
        """Gets the node's children list

        Returns:
            a List that contains all direct children of a node
        """
        return self._children

    def get_all_children(self) -> list:
        """Gets all children of a node

        Returns:
            a List that contains all children (incl. grandchildren, great-grandchildren, etc) of a node in BFS order
        """
        if not self._children:
            return None
        all_children = []
        queue = self._children
        while queue:
            cur = queue.pop(0)
            all_children.append(cur)
            queue.extend(cur.get_children())
        return all_children

    def set_children(self, new_children: list) -> None:
        """Sets the node's children list

        Args:
            new_chidlren: a list containing nodes that should be children of this node
        """
        self._children = new_children

    def get_value(self) -> int:
        """Gets the node's value

        Returns:
            an int representing the node's current value
        """
        return self._value

    def set_value(self, new_value: int) -> None:
        """Sets the node's current value

        Args:
            new_value: an int representing the current value of the node
        """
        self._value = new_value


class PlayerType(IntEnum):
    MAXIMIZING = 0
    MINIMIZING = 1


class MinimaxPlayer(Player):

    def __init__(
        self,
        token: TokenType = TokenType.XTOKEN,
        state: State = State(DEFAULT_STATE),
    ) -> None:
        super().__init__(token, state)

    def choose_action(self, state: State) -> Action:
        """Chooses what action should be taken using an implementation of the minimax algorithm

        Args:
            state: a State representing the current board state

        Returns:
            an Action representing the chosen action
        """

        def _minimax(tree: Node, depth: int, player_type: PlayerType):
            """An implementation of the minimax algorithm

            Args:
                tree: a Node to be treated as the root of an existing Node tree
                depth: an Int representing the maximum depth. Will return early if it reaches 0
                player_type: a PlayerType enum representing if the iteration is a minimizer or maximizer

            Returns:
                an Int representing the node with the best expected value
            """
            state = tree.get_state()
            if state.is_game_over():
                return 100 * (
                    1
                    if state.get_winner() == self._token.value
                    else 0 if not state.get_winner() else -1
                )

            if depth == 0:
                # number of future states?
                return len(tree.get_all_children()) + tree.get_state().count_empties()

            if player_type == PlayerType.MAXIMIZING:
                max_eval = -sys.maxsize - 1  # -inf
                for child_node in tree.get_children():
                    cur_eval = _minimax(child_node, depth - 1, PlayerType.MINIMIZING)
                    child_node.set_value(cur_eval)
                    max_eval = max(max_eval, cur_eval)
                return max_eval

            min_eval = sys.maxsize  # +inf
            for child_node in tree.get_children():
                cur_eval = _minimax(child_node, depth - 1, PlayerType.MAXIMIZING)
                child_node.set_value(cur_eval)
                min_eval = min(min_eval, cur_eval)
            return min_eval

        max_depth = 4
        depth = 1

        # build tree
        root = Node(state=state, parent=None)
        move_type = self._token
        last_on_level = cur = root
        fringe = [root]
        while depth < max_depth:
            # found all states
            if not fringe:
                break
            cur = fringe.pop(0)
            cur_children = []
            for action in cur.get_state().get_actions(move_type.value):
                child_node = Node(state=cur.get_state().execute(action), parent=cur)
                cur_children.append(child_node)
            cur.set_children(cur_children)
            fringe = fringe + cur_children
            if last_on_level.get_state() == cur.get_state():
                depth += 1
                last_on_level = child_node
                for token in TokenType:
                    if token != move_type:
                        move_type = token
                        break

        # make minimax choice
        choice = _minimax(root, max_depth, PlayerType.MAXIMIZING)

        # find choice in tree
        chosen_child = None
        for child in root.get_children():
            if child.get_value() == choice:
                chosen_child = child

        if not chosen_child:
            print("Error! Did not find choice in minimax tree")
            exit(3)

        # get the action
        for action in state.get_actions(self._token.value):
            if str(state.execute(action)) == str(chosen_child.get_state()):
                return action

        print("Error! Did not find the action!")
        exit(4)
