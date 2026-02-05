class Step:
    """
    Represent a single step in the maze generation process.

    Each step records a cell position and optionally the wall
    that was opened during that step.

    Attributes:
        x (int): The x coordinate of the cell.
        y (int): The y coordinate of the cell.
        wall (str | None): The wall that was opened ('W', 'E', 'N', 'S')
            or None if no wall was opened.
    """

    def __init__(self, x: int, y: int, wall: str | None) -> None:
        """
        Initialize a new step.

        Args:
            x (int): The x coordinate of the cell.
            y (int): The y coordinate of the cell.
            wall (str | None): The wall direction ('W', 'S', 'E', 'N')
                or None if no wall was opened.
        """
        assert wall in {"W", "S", "E", "N", None}, \
            "wall should be {W, S, E, N}"
        self.x = x
        self.y = y
        self.wall = wall
