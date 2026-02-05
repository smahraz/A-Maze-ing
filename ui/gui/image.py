from mlx import Mlx
from .color import Color
from typing import Any


class Image:
    """
    Represent an image buffer for rendering with MLX.

    This class wraps an MLX image and provides methods for
    pixel manipulation and displaying the image in a window.

    Attributes:
        width (int): The width of the image in pixels.
        height (int): The height of the image in pixels.
        image: The MLX image handle.
        data: The raw pixel data buffer.
        bpp (int): Bits per pixel.
        sl (int): Size of a line in bytes.
        form: Byte order format.
    """

    def __init__(self, mlx: Mlx, mlx_ptr: Any, width: int, height: int):
        """
        Initialize a new Image.

        Args:
            mlx (Mlx): The MLX library instance.
            mlx_ptr: The MLX context pointer.
            width (int): The width of the image in pixels.
            height (int): The height of the image in pixels.
        """
        self._mlx = mlx
        self._mlx_ptr = mlx_ptr
        self.width = width
        self.height = height
        self.image = self._mlx.mlx_new_image(
            mlx_ptr,
            width,
            height
        )
        self.data, self.bpp, self.sl, self.form = (
            self._mlx.mlx_get_data_addr(self.image)
        )

    def put_pixel(self, x: int, y: int, color: Color) -> None:
        """
        Set the color of a pixel in the image.

        Args:
            x (int): The x coordinate of the pixel.
            y (int): The y coordinate of the pixel.
            color (Color): The color to set.
        """
        color_format = color.big() if not self.form else color.little()
        offset = y * self.sl + x * (self.bpp // 8)
        data_view = self.data[offset:].cast("I")
        data_view[0] = color_format

    def put_to_win(self, win: Any, x: int, y: int) -> None:
        """
        Display the image in a window at the specified position.

        Args:
            win: The window handle.
            x (int): The x position in the window.
            y (int): The y position in the window.
        """
        self._mlx.mlx_put_image_to_window(
            self._mlx_ptr,
            win,
            self.image,
            x, y
        )

    def clear(self, color: Color) -> None:
        """
        Fill the entire image with a single color.

        Args:
            color (Color): The color to fill the image with.
        """
        for y in range(self.height):
            for x in range(self.width):
                self.put_pixel(x, y, color)
