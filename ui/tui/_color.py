import random


class Color:
    """
    Provide ANSI escape codes for colored terminal output.

    This class defines constants for foreground and background
    colors, including default values for walls, protected cells,
    and new cell backgrounds. It also allows changing the wall and
    new cell background colors dynamically using the `change` method.

    Attributes:
        BLACK_BG (str): ANSI code for black background.
        RED_BG (str): ANSI code for red background.
        WHITE_BG (str): ANSI code for white background.
        GREEN_BG (str): ANSI code for green background.

        BLACK (str): ANSI code for black text.
        WHITE (str): ANSI code for white text.
        GREEN (str): ANSI code for green text.
        PURPLE (str): ANSI code for purple text.
        RED (str): ANSI code for red text.

        DEFAULT (str): ANSI code to reset all formatting.

        protected_cell (str): Default background for protected cells.
        wall (str): Default color for walls.
        bg (str): Default background color.
        new_cell_bg (str): Default background for newly created cells.
    """
    BLACK_BG = "\033[40m"
    RED_BG = "\033[41m"
    WHITE_BG = "\033[47m"
    GREEN_BG = "\033[42m"

    BLACK = "\033[30m"
    WHITE = "\033[37m"
    GREEN = "\033[32m"
    PURPLE = "\033[35m"
    RED = "\033[31m"

    DEFAULT = "\033[0m"

    protected_cell = RED_BG
    wall = WHITE
    bg = BLACK_BG
    new_cell_bg = WHITE_BG

    _color_range = list(range(31, 38)) + list(range(91, 98))

    @classmethod
    def change(cls) -> None:
        """
        Randomly change the wall and new cell background colors.

        This method selects a random color from the ANSI range
        defined in `_color_range` and updates `wall` and `new_cell_bg`
        accordingly.
        """
        color = random.choice(cls._color_range)
        cls.wall = f"\033[{color}m"
        cls.new_cell_bg = f"\033[{color % 10 + 40}m"
