

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

    _color_op: int = 1

    @classmethod
    def change(cls) -> None:
        if cls._color_op > 3:
            cls._color_op = 0

        cls.wall = [
            Color.WHITE,
            Color.GREEN,
            Color.RED,
            Color.PURPLE
        ][cls._color_op]
        cls._color_op += 1
