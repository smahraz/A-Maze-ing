from mlx import Mlx
from map import Map, _Cell


class Color:
    def __init__(self, red: int, green: int, blue: int):
        self.red = red
        self.green = green
        self.blue = blue

    def big(self) -> int:
        return 255 << 24 | self.red << 16 | self.green << 8 | self.blue

    def little(self) -> int:
        return self.blue << 24 | self.green << 16 | self.red << 8 | 255


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
        self.data = None

    def _get_data(self) -> tuple[memoryview, int, int, int]:
        if not self.data:
            self.data = self._mlx.mlx_get_data_addr(self.image)
        return self.data

    def put_pixel(self, x: int, y: int, color: Color):
        data, bpp, sl, form = self._get_data()
        color_format = color.big() if not form else color.little()
        data_format = data[y * sl + x * (bpp // 8):].cast("I")
        data_format[0] = color_format

    def put_to_win(self, win: any, x: int, y: int):
        self._mlx.mlx_put_image_to_window(
            self._mlx_ptr,
            win,
            self.image,
            x, y
        )

    def clear(self):
        for x in range(self.width):
            for y in range(self.height):
                self.put_pixel(x, y, Color(0, 0, 0))


class Gui:
    border = 30
    cell_size = 30
    stroke = 3

    def __init__(self, map: Map):
        self.map = map
        self.width = self.cell_size * map.width\
            + self.border * 2 + self.stroke
        self.height = self.cell_size * map.height\
            + self.border * 2 + self.stroke

        self._mlx = Mlx()
        self._mlx_ptr = None
        self._window = None
        self._maze: Image = None
        self._bg: Image = None
        self._bg_color = Color(
            45,
            42,
            64
        )
        self._wall_color = Color(
            255,
            255,
            255
        )

    def quit_gui(self, param):
        self._mlx.mlx_loop_exit(self._mlx_ptr)

    def init_mlx(self):
        if not self._mlx_ptr:
            self._mlx_ptr = self._mlx.mlx_init()
        self._window = self._mlx.mlx_new_window(
            self._mlx_ptr,
            self.width,
            self.height,
            "A-Maze-ing"
        )

        self._mlx.mlx_hook(self._window, 33, 0, self.quit_gui, None)

        self._maze = Image(
            self._mlx,
            self._mlx_ptr,
            self.width - self.border * 2,
            self.height - self.border * 2
        )
        self._bg = Image(
            self._mlx,
            self._mlx_ptr,
            self.width,
            self.height
        )

    def render_bg(self):
        for x in range(self.width):
            for y in range(self.height):
                self._bg.put_pixel(x, y, self._bg_color)
        self._mlx.mlx_put_image_to_window(
            self._mlx_ptr,
            self._window,
            self._bg.image,
            0, 0
        )

    def render_wall(self, x, y, dir: str):
        offset = self.cell_size
        if dir == 'E':
            for stroke in range(self.stroke):
                for length in range(self.cell_size + self.stroke):
                    self._maze.put_pixel(
                        x * self.cell_size + stroke + offset,
                        y * self.cell_size + length,
                        self._wall_color
                    )
        if dir == 'S':
            for stroke in range(self.stroke):
                for length in range(self.cell_size + self.stroke):
                    self._maze.put_pixel(
                        x * self.cell_size + length,
                        y * self.cell_size + stroke + offset,
                        self._wall_color
                    )
        if dir == 'N':
            for stroke in range(self.stroke):
                for length in range(self.cell_size + self.stroke):
                    self._maze.put_pixel(
                        x * self.cell_size + length - self.stroke,
                        y * self.cell_size + stroke,
                        self._wall_color
                    )
        if dir == 'W':
            for stroke in range(self.stroke):
                for length in range(self.cell_size + self.stroke):
                    self._maze.put_pixel(
                        x * self.cell_size + stroke,
                        y * self.cell_size + length - self.stroke,
                        self._wall_color
                    )

    def clear_wall(self, x, y, dir: str):
        offset = self.cell_size
        if dir == 'E':
            for stroke in range(self.stroke):
                for length in range(self.cell_size - self.stroke):
                    self._maze.put_pixel(
                        x * self.cell_size + stroke + offset,
                        y * self.cell_size + length + self.stroke,
                        self._bg_color
                    )
        if dir == 'S':
            for stroke in range(self.stroke):
                for length in range(self.cell_size - self.stroke):
                    self._maze.put_pixel(
                        x * self.cell_size + length + self.stroke,
                        y * self.cell_size + stroke + offset,
                        self._bg_color
                    )

    def render_cell(self, cell: _Cell):
        if cell.x == 0:
            self.render_wall(0, cell.y, 'W')
        if cell.y == 0:
            self.render_wall(cell.x, 0, 'N')
        if cell.east.is_closed or cell.x == self.map.width - 1:
            self.render_wall(cell.x, cell.y, 'E')
        else:
            self.clear_wall(cell.x, cell.y, 'E')
        if cell.south.is_closed or cell.y == self.map.height - 1:
            self.render_wall(cell.x, cell.y, 'S')
        else:
            self.clear_wall(cell.x, cell.y, 'S')

    def render_maze(self):
        for row in self.map.map:
            for cell in row:
                self.render_cell(cell)

        self._mlx.mlx_put_image_to_window(
            self._mlx_ptr,
            self._window,
            self._maze.image,
            self.border, self.border
        )

    def display(self):
        if not self._window:
            self.init_mlx()
        self.render_bg()
        self.render_maze()
        self._mlx.mlx_loop(self._mlx_ptr)
