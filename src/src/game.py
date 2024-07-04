from manager import Manager
from node import Node
from solvers.solver import Solver
from state import State


class Game:
    def __init__(self, compiler, limit):
        self.state = State(compiler.maze, compiler.level, compiler.start, compiler.escape, compiler.traps)
        self.ex = 0
        self.solver = Solver(limit)

    def _get_move(self) -> int:
        """
        Support method for Game.play() taking input for next move.
        :return: int 1: left, 2: right, 3: up, 4: down
        """
        while True:
            try:
                move = int(input("Move direction: 1-L, 2-R, 3-U, 4-D >> "))
                if move in range(1, 5):
                    return move
            except ValueError:
                print("Number must be 1-4..")
            except Exception as e:
                print(e)

    def _apply_move(self, move: int, n: int = 1) -> None:
        """
        Support method for Game.play() responsible for applying arg move to current state for game progression.
        :param move: int 1: left, 2: right, 3: up, 4: down
        :param n: int for amount of moves to make in selected direction, default = 1
        :return: None
        """
        directions = {1: (0, -n), 2: (0, n), 3: (-n, 0), 4: (n, 0)}
        dx, dy = directions[move]
        m = Manager(dx, dy)
        if m.is_applicable(self.state):
            self.state = m.apply_state(self.state)
            self.ex = 0
        else:
            print("Bad move. Please try again.")

    def play(self) -> None:
        """
        Provides continuous game-play for user-based traversal of the maze.
        :return: None
        """
        while not self.state.is_target_state():
            print(self.state)
            move = self._get_move()
            try:
                # n = int(input("How many moves >> "))
                # self._apply_move(move, n)
                self._apply_move(move)
            except Exception as e:
                print(e)
                self.ex += 1
                if self.ex > 5:
                    raise SystemExit("Stopping execution due to possible loop")
        print("Congratulations!")

    def ai_play(self, visualize: bool) -> str:
        """
        Breadth first solver's solve method wrapper utilized by game class.
        :param visualize: bool for showing states
        :return: str of moves performed in state log
        """
        result = self.solver.solve(self.state)

        if result is None:
            raise ValueError("No solution found!")
        else:
            self.display_path(result, visualize)
            return result.state.log

    def display_path(self, node: Node, visualize: bool) -> None:
        """
        Displays the path taken by the solver across states based on arg settings.
        :param node: node of decision tree utilized by solver
        :param visualize: bool for showing states
        :return: None
        """
        if node is None:
            return
        else:
            self.display_path(node.parent, visualize)
            if visualize:
                print(node.state)
