from mlx import Mlx
from .color import Color


class Image:
    def __init__(self, mlx: Mlx, mlx_ptr: any, width: int, height: int):
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

    def put_pixel(self, x: int, y: int, color: Color):
        color_format = color.big() if not self.form else color.little()
        offset = y * self.sl + x * (self.bpp // 8)
        data_view = self.data[offset:].cast("I")
        data_view[0] = color_format

    def put_to_win(self, win: any, x: int, y: int):
        self._mlx.mlx_put_image_to_window(
            self._mlx_ptr,
            win,
            self.image,
            x, y
        )
