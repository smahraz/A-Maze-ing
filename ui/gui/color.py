from random import randint


class Color:

    def __init__(self, red: int, green: int, blue: int,  alpha: int = 255):
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha
        self._big = None
        self._little = None

    def big(self) -> int:
        if self._big is None:
            self._big = (
                self.alpha << 24 | self.red << 16 |
                self.green << 8 | self.blue
            )
        return self._big

    def little(self) -> int:
        if self._little is None:
            self._little = (
                self.blue << 24 | self.green << 16 |
                self.red << 8 | self.alpha
            )
        return self._little

    @classmethod
    def get_random(cls):
        red = randint(0, 255)
        green = randint(0, 255)
        blue = randint(0, 255)
        return cls(red, green, blue)

    @classmethod
    def _init_constants(cls):
        cls.TRANSPARENT = cls(0, 0, 0, 0)
        cls.WHITE = cls(255, 255, 255)
        cls.BG = cls(45, 42, 64)
        cls.RED = cls(255, 0, 0)
        cls.BLUE = cls(0, 0, 255)


Color._init_constants()
