import copy
from typing import List, Tuple


class State:
    """
    Represents each state of the maze between moves.
    """
    def __init__(self, maze: List[List[str]], level: int, start: Tuple[int, int], escape: Tuple[int, int], traps):
        self.maze = maze
        self.level = level
        self.row = start[0]
        self.col = start[1]
        self.start = start
        self.escape = escape
        self.quad_start = {
            1: [1, 1],
            2: [1, 6],
            3: [1, 11],
            4: [6, 1],
            5: [6, 6],
            6: [6, 11],
            7: [11, 1],
            8: [11, 6],
            9: [11, 11]}
        self.log = ""
        self.traps = traps

    def is_target_state(self) -> bool:
        """
        Checks if current state is 'Escape'/maze exit.
        :return: True if current position matches escape coordinates
        """
        if self.maze[self.row][self.col] == "E":
            return True
        return False

    def clone(self) -> "State":
        """
        Returns deep copy of current state to apply move on.
        :return: cloned state
        """
        new_state = State(
            copy.deepcopy(self.maze),
            self.level,
            (copy.deepcopy(self.row), copy.deepcopy(self.col)),
            copy.deepcopy(self.escape),
            self.traps
        )
        return new_state

    def _rotate_right(self, quad_size, rotated_quad, start_row, start_col) -> None:
        """
        Auxiliary function assisting State.rotate_quadrant (all args autofilled by it).
        Responsible for rotating the selected 5x5 quadrant right.
        """
        for i in range(quad_size):
            for j in range(quad_size):
                rotated_quad[j][quad_size - 1 - i] = self.maze[start_row + i][start_col + j]

    def _rotate_left(self, quad_size, rotated_quad, start_row, start_col) -> None:
        """
        Auxiliary function assisting State.rotate_quadrant (all args autofilled by it).
        Responsible for rotating the selected 5x5 quadrant left.
        """
        for i in range(quad_size):
            for j in range(quad_size):
                rotated_quad[quad_size - 1 - j][i] = self.maze[start_row + i][start_col + j]

    def rotate_quadrant(self, quadrant: int, direction: str, quad_size: int = 5) -> None:
        """
        Rotates the selected quadrant in the specified direction once.
        :param quadrant: int of quadrant to rotate (1-9)
        :param direction: "left" or "right" for clockwise or counter-clockwise
        :param quad_size: defaults to 5
        :return:
        """
        if quadrant not in range(1, 10):
            raise ValueError(f"Quadrant must be an int between 1-9. {quadrant} is not a correct value!")

        start_row = self.quad_start[quadrant][0]
        start_col = self.quad_start[quadrant][1]

        # check position in quadrant
        if self.row in range(start_row, start_row + 5) and self.col in range(start_col, start_col + 5):
            raise ValueError("Cannot rotate a district that you are currently in!")

        if direction not in [1, 2]:
            raise ValueError(f"Rotate direction can only be 'right' or 'left', not {direction}!")

        rotated_quad = [[''] * quad_size for _ in range(quad_size)]

        if direction == 1:
            self._rotate_left(quad_size, rotated_quad, start_row, start_col)
        elif direction == 2:
            self._rotate_right(quad_size, rotated_quad, start_row, start_col)

        # insert rotated quadrant
        for i in range(quad_size):
            for j in range(quad_size):
                self.maze[start_row + i][start_col + j] = rotated_quad[i][j]

    def _draw(self, size: int = 17) -> str:
        """
        Returns console printable colored maze.
        :param size: maze length, default so 17
        :return: str of maze
        """
        pic = ""
        for row in range(size):
            for col in range(size):
                if self.maze[row][col] == "S":
                    pic += "\033[92m S \033[0m"
                elif self.row == row and self.col == col:
                    pic += "\033[92m o \033[0m"
                elif self.maze[row][col] == "E":
                    pic += "\033[91m E \033[0m"
                elif self.maze[row][col] == "H":
                    pic += "\033[93m H \033[0m"
                else:
                    pic += f" {self.maze[row][col]} "
            pic += "\n"
        return pic

    def __eq__(self, other) -> bool:
        if other is None or not isinstance(other, State):
            return False
        if self.maze != other.maze or self.row != other.row or self.col != other.col:
            return False
        return True

    def __str__(self) -> str:
        return self._draw()
