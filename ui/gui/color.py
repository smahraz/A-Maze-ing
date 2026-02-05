from random import randint


class Color:
    """
    Represent an RGBA color for rendering.

    This class stores color components and provides methods
    to convert the color to different byte order formats
    for image rendering.

    Attributes:
        red (int): The red component (0-255).
        green (int): The green component (0-255).
        blue (int): The blue component (0-255).
        alpha (int): The alpha component (0-255).
    """

    def __init__(self, red: int, green: int, blue: int,  alpha: int = 255):
        """
        Initialize a new Color.

        Args:
            red (int): The red component (0-255).
            green (int): The green component (0-255).
            blue (int): The blue component (0-255).
            alpha (int, optional): The alpha component. Defaults to 255.
        """
        self.red: int = red
        self.green: int = green
        self.blue: int = blue
        self.alpha: int = alpha
        self._big: int = 0
        self._little: int = 0

    def big(self) -> int:
        """
        Get the color as a big-endian integer.

        Returns:
            int: The color in ARGB format for big-endian systems.
        """
        if not self._big:
            self._big = (
                self.alpha << 24 | self.red << 16 |
                self.green << 8 | self.blue
            )
        return self._big

    def little(self) -> int:
        """
        Get the color as a little-endian integer.

        Returns:
            int: The color in BGRA format for little-endian systems.
        """
        if not self._little:
            self._little = (
                self.blue << 24 | self.green << 16 |
                self.red << 8 | self.alpha
            )
        return self._little

    @classmethod
    def get_random(cls) -> "Color":
        """
        Generate a random color.

        Returns:
            Color: A new Color instance with random RGB values.
        """
        red = randint(0, 255)
        green = randint(0, 255)
        blue = randint(0, 255)
        return cls(red, green, blue)
