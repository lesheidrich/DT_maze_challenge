from state import State


class Manager:
    """
    Responsible for moving between states in the maze.
    """
    def __init__(self, dx: int, dy: int):
        self.dx = dx
        self.dy = dy
        if dx == -1:
            self.dstr = "3"
        elif dx == 1:
            self.dstr = "4"
        elif dy == -1:
            self.dstr = "1"
        elif dy == 1:
            self.dstr = "2"

    def apply_state(self, current_state: State) -> State:
        """
        Applies the desired movement the current state instance, returning a new instance with desired values.
        :param current_state: currents state instance
        :return: new state instance with the move applied and marked on the maze with 'o' as the current position.
        """
        new_state = current_state.clone()
        new_state.start = current_state.start

        new_state.row += self.dx
        new_state.col += self.dy

        # trap
        row, col = new_state.row, new_state.col
        if new_state.maze[row][col] == "H":
            new_state.maze[row][col] = " "
            new_state.row, new_state.col = new_state.start

        new_state.log = current_state.log + self.dstr + "\n"
        return new_state

    def is_applicable(self, state: State) -> bool:
        """
        Checks if the next move is legal (if it's not a wall).
        :param state: current state instance of the maze
        :return: True if move is allowed, else False
        """
        if state is None:
            return False

        new_x = state.row + self.dx
        new_y = state.col + self.dy

        if new_x < 0 or new_y < 0 or new_x > 16 or new_y > 16:
            return False

        return state.maze[new_x][new_y] != "X" and state.maze[new_x][new_y] != "S"


class RotationManager:
    def __init__(self, region: int, direction):
        self.region = region
        self.direction = direction

    def apply_state(self, current_state: State) -> State:
        new_state = current_state.clone()
        new_state.start = current_state.start

        new_state.rotate_quadrant(self.region, self.direction)
        new_state.log = current_state.log + f"r {self.region} {self.direction}\n"
        return new_state

    def is_in(self, state, row, col) -> bool:
        min_x, min_y = state.quad_start[self.region]
        return min_x <= row < min_x + 5 and min_y <= col < min_y + 5

    def is_applicable(self, state: State) -> bool:
        if state is None or state.level < 3:
            return False

        row = state.row
        col = state.col

        return not self.is_in(state, row, col) #and self.has_trap(state)

    def has_trap(self, state) -> bool:
        for trap in state.traps:
            if self.is_in(state, trap[0], trap[1]):
                return True

        return False
