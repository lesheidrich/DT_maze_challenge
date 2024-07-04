from state import State


class Node:
    """
    Nodes of solver's decision tree, each containing the current state of the maze.
    """
    def __init__(self, state: State, parent=None):
        self.state = state
        self.parent = parent
        self.operator_index = 0
        self.depth = self._set_depth()

    def _set_depth(self) -> int:
        """
        Sets depth of node to None if it's root node, otherwise increments parent's depth.
        :return: int of node depth
        """
        return 0 if self.parent is None else self.parent.depth + 1

    def is_target_state(self) -> bool:
        """
        Extends attribute state's is_target_state() returning True if state's current position is the
        escape character.
        :return: True if node's position is Escape
        """
        return self.state.is_target_state()

    def has_loop(self) -> bool:
        """
        Checks if parent state matches child state.
        :return: True if parent == child state
        """
        ancestor = self.parent

        while ancestor is not None:
            if ancestor == self:
                return True
            ancestor = ancestor.parent

        return False

    def __str__(self) -> str:
        result = ""

        if self.parent is not None:
            result += self.parent
            result += "\n *** \n"
        result += f"Depth: {self.depth}\n{self.state}"

        return result

    def __eq__(self, other) -> bool:
        if other is None or not isinstance(other, Node):
            return False

        return self.state == other.state
