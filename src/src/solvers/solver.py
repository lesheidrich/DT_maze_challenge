from typing import Union
from manager import Manager, RotationManager
from node import Node
from state import State
from time import time


class Solver:
    def __init__(self, limit):
        self.current_node = None
        self.path = None
        self.depth_limit = limit
        self.managers = []
        self.generate_managers()
        self.output = ""

    def generate_managers(self) -> None:
        """
        Initializes state managers responsible for left, right, up, down movement.
        :return: None
        """
        del self.managers[:]

        for d in [-1, 1]:
            self.managers.append(Manager(0, d))
            self.managers.append(Manager(d, 0))

    def select_manager(self) -> Union[Manager, None]:
        """
        Selects next valid move from state managers list utilizing operator_index.
        :return: selected manager | None
        """
        while self.current_node.operator_index < len(self.managers):
            m = self.managers[self.current_node.operator_index]
            self.current_node.operator_index += 1

            if m.is_applicable(self.current_node.state):
                return m

        return None

    def next_move(self) -> None:
        """
        Determines next move from current state.
        Updates current node, handles backtracking, loop detection, target checkinga and the depth limit.
        :return: None
        """
        m = self.select_manager()

        if m is None:
            self.current_node = self.current_node.parent
        else:
            new_state = m.apply_state(self.current_node.state)
            self.current_node = Node(new_state, self.current_node)

            if self.current_node.has_loop():
                self.current_node = self.current_node.parent
            elif self.current_node.is_target_state():
                if self.path is None or self.path.depth > self.current_node.depth:
                    self.path = self.current_node
                    self.depth_limit = self.path.depth

                self.current_node = self.current_node.parent

            elif self.current_node.depth > self.depth_limit:
                self.current_node = self.current_node.parent

    def solve(self, start_state: State) -> Node:
        """
        Iterates over state applying managers until solution or branch limit is reached.
        For level 3 mazes, it generates rotated maze instances before solving for best solution breadth first.
        :param start_state: state with position at starting coordinates
        :return: Node with solution to E
        """
        self.generate_managers()
        starting_states = []
        starting_states.append(start_state)

        if start_state.level == 3:
            for r in range(1, 10):
                m = RotationManager(r, 1)

                if m.is_applicable(start_state):
                    new_state = m.apply_state(start_state)
                    starting_states.append(new_state)
                    starting_states.append(m.apply_state(new_state))

                m = RotationManager(r, 2)

                if m.is_applicable(start_state):
                    new_state = m.apply_state(start_state)
                    starting_states.append(new_state)

        start_time = time()
        for state in starting_states:
            self.current_node = Node(state)
            while self.current_node is not None and start_time + 60 > time():
                self.next_move()

        return self.path
