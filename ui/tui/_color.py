import random




class Color:
    BLACK_BG = "\033[40m"
    RED_BG = "\033[41m"
    WHITE_BG = "\033[47m"
    GREEN_BG = "\033[42m"

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
        color = random.choice(cls._color_range)
        cls.wall = f"\033[{color}m"
        cls.new_cell_bg = f"\033[{color % 10 + 40}m"
