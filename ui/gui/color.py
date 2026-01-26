from random import randint
from typing import TypeVar, Type

T = TypeVar("T", bound="Color")


class Color:

    def __init__(self, red: int, green: int, blue: int,  alpha: int = 255):
        self.red: int = red
        self.green: int = green
        self.blue: int = blue
        self.alpha: int = alpha
        self._big: int = 0
        self._little: int = 0

    def big(self) -> int:
        if not self._big:
            self._big = (
                self.alpha << 24 | self.red << 16 |
                self.green << 8 | self.blue
            )
        return self._big

    def little(self) -> int:
        if not self._little:
            self._little = (
                self.blue << 24 | self.green << 16 |
                self.red << 8 | self.alpha
            )
        return self._little

    @classmethod
    def get_random(cls: Type[T]) -> T:
        red = randint(0, 255)
        green = randint(0, 255)
        blue = randint(0, 255)
        return cls(red, green, blue)
