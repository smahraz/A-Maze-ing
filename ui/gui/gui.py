from mlx import Mlx
from mazegen import MazeGenerator, Maze, Cell


class Color:
    def __init__(self, red: int, green: int, blue: int,  alpha: int = 255):
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

    def big(self) -> int:
        return self.alpha << 24 | self.red << 16 | self.green << 8 | self.blue

    def little(self) -> int:
        return self.blue << 24 | self.green << 16 | self.red << 8 | self.alpha


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
            return self._mlx.mlx_get_data_addr(self.image)
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

    def clear(self, color: Color = Color(0, 0, 0, 0)):
        for x in range(self.width):
            for y in range(self.height):
                self.put_pixel(x, y, color)


class Gui:
    def __init__(self, maze_gen: MazeGenerator):
        self.maze_gen = maze_gen
        self.map = maze_gen.generate_maze()
        self._init_params(self.map)
        self.width = self.cell_size * self.map.width\
            + self.border * 2 + self.stroke
        self.height = self.cell_size * self.map.height\
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

        self.animate = False
        self.start_animation = False
        self.cursors = []

    def _init_params(self, map: Maze):
        if map.width <= 50 and map.height <= 25:
            self.border = 40
            self.cell_size = 32
            self.stroke = 8
        elif map.width <= 100 and map.height <= 50:
            self.border = 20
            self.cell_size = 16
            self.stroke = 4
        elif map.width <= 200 and map.height <= 100:
            self.border = 10
            self.cell_size = 8
            self.stroke = 2
        elif map.width <= 400 and map.height <= 200:
            self.border = 5
            self.cell_size = 4
            self.stroke = 1
        else:
            self.border = 0
            self.cell_size = 2
            self.stroke = 1

    def quit_gui(self, param=None):
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
        self._maze.clear()

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

    def render_wall(self, x, y, dir: str, clear: bool = False):
        color = self._wall_color if not clear else self._bg_color
        offset = self.cell_size
        match dir:
            case 'E':
                for stroke in range(self.stroke):
                    for length in range(self.cell_size - self.stroke):
                        self._maze.put_pixel(
                            x * self.cell_size + stroke + offset,
                            y * self.cell_size + length + self.stroke,
                            color
                        )
            case 'S':
                for stroke in range(self.stroke):
                    for length in range(self.cell_size - self.stroke):
                        self._maze.put_pixel(
                            x * self.cell_size + length + self.stroke,
                            y * self.cell_size + stroke + offset,
                            color
                        )
            case 'N':
                for stroke in range(self.stroke):
                    for length in range(self.cell_size - self.stroke):
                        self._maze.put_pixel(
                            x * self.cell_size + length + self.stroke,
                            y * self.cell_size + stroke,
                            color
                        )
            case 'W':
                for stroke in range(self.stroke):
                    for length in range(self.cell_size - self.stroke):
                        self._maze.put_pixel(
                            x * self.cell_size + stroke,
                            y * self.cell_size + length + self.stroke,
                            color
                        )

    def render_corner(self, cell: Cell, pos: str, clear: bool = False):
        color = self._wall_color if not clear else self._bg_color
        offset = self.cell_size
        match pos:
            case 'NW':
                for stroke in range(self.stroke):
                    for length in range(self.stroke):
                        self._maze.put_pixel(
                            cell.x * self.cell_size + stroke,
                            cell.y * self.cell_size + length,
                            color
                        )
            case 'SW':
                for stroke in range(self.stroke):
                    for length in range(self.stroke):
                        self._maze.put_pixel(
                            cell.x * self.cell_size + stroke,
                            cell.y * self.cell_size + length + offset,
                            color
                        )
            case 'NE':
                for stroke in range(self.stroke):
                    for length in range(self.stroke):
                        self._maze.put_pixel(
                            cell.x * self.cell_size + stroke + offset,
                            cell.y * self.cell_size + length,
                            color
                        )
            case 'SE':
                for stroke in range(self.stroke):
                    for length in range(self.stroke):
                        self._maze.put_pixel(
                            cell.x * self.cell_size + stroke + offset,
                            cell.y * self.cell_size + length + offset,
                            color
                        )

    def color_cell(self, cell: Cell, color: Color):
        for w in range(self.cell_size):
            for h in range(self.cell_size):
                self._maze.put_pixel(
                    cell.x * self.cell_size + w,
                    cell.y * self.cell_size + h,
                    color
                )

    def color_cells(self, color: Color):
        for cell in self.map.cell_iterator():
            self.color_cell(cell, color)

    def render_protected(self, cell: Cell):
        self.color_cell(cell, Color(255, 0, 0))
        self.render_wall(cell.x, cell.y, 'N')
        self.render_wall(cell.x, cell.y, 'E')
        self.render_wall(cell.x, cell.y, 'W')
        self.render_wall(cell.x, cell.y, 'S')
        self.render_corner(cell, 'NW')
        self.render_corner(cell, 'SW')
        self.render_corner(cell, 'NE')
        self.render_corner(cell, 'SE')

    def render_cell(self, cell: Cell):
        if cell.is_protected:
            self.render_protected(cell)
            return
        if cell.x == 0:
            self.render_wall(0, cell.y, 'W')
            self.render_corner(cell, 'SW')
        if cell.y == 0:
            self.render_wall(cell.x, 0, 'N')
            self.render_corner(cell, 'NW')
        if cell.east.is_closed or cell.x == self.map.width - 1:
            self.render_wall(cell.x, cell.y, 'E')
            self.render_corner(cell, 'NE')
            self.render_corner(cell, 'SE')
        else:
            self.render_wall(cell.x, cell.y, 'E', clear=True)
            if cell.above_cell and cell.right_cell:
                if not cell.north.is_closed\
                    and not cell.above_cell.east.is_closed\
                        and not cell.right_cell.north.is_closed:
                    self.render_corner(cell, 'NE', clear=True)
            if cell.below_cell and cell.right_cell:
                if not cell.south.is_closed\
                    and not cell.below_cell.east.is_closed\
                        and not cell.right_cell.south.is_closed:
                    self.render_corner(cell, 'SE', clear=True)
        if cell.south.is_closed or cell.y == self.map.height - 1:
            self.render_wall(cell.x, cell.y, 'S')
            self.render_corner(cell, 'SW')
            self.render_corner(cell, 'SE')
        else:
            self.render_wall(cell.x, cell.y, 'S', clear=True)
            if cell.below_cell and cell.left_cell:
                if not cell.west.is_closed\
                    and not cell.below_cell.west.is_closed\
                        and not cell.left_cell.south.is_closed:
                    self.render_corner(cell, 'SW', clear=True)
            if cell.below_cell and cell.right_cell:
                if not cell.east.is_closed\
                    and not cell.below_cell.east.is_closed\
                        and not cell.right_cell.south.is_closed:
                    self.render_corner(cell, 'SE', clear=True)

    def render_cursor(self, cell: Cell, clear: bool = False):
        color = Color(0, 255, 0, 50) if not clear else self._bg_color
        for w in range(self.cell_size - self.stroke):
            for h in range(self.cell_size - self.stroke):
                self._maze.put_pixel(
                    cell.x * self.cell_size + w + self.stroke,
                    cell.y * self.cell_size + h + self.stroke,
                    color
                )

    def render_maze(self):
        for cell in self.map.cell_iterator():
            self.render_cell(cell)

        self._mlx.mlx_put_image_to_window(
            self._mlx_ptr,
            self._window,
            self._maze.image,
            self.border, self.border
        )

    def animate_maze(self):
        if not self.steps:
            # print("done")
            self.start_animation = False
            return
        step = self.steps[0]
        self.steps = self.steps[1:]
        self.map.apply_step(step.x, step.y, step.wall)
        self.render_cell(self.map.map[step.y][step.x])
        for s in self.steps[:5]:
            self.render_cursor(self.map.map[s.y][s.x])
            self.cursors.append(self.map.map[s.y][s.x])
        self.render_cursor(self.map.map[step.y][step.x], clear=True)

        self._mlx.mlx_put_image_to_window(
            self._mlx_ptr,
            self._window,
            self._maze.image,
            self.border, self.border
        )

    def key_hook(self, keycode: int, param: any):
        match keycode:
            case 0xff1b:
                self.quit_gui()
            case 0x72:
                self.maze_gen.reseed()
                if self.start_animation:
                    self.start_animation = False
                    for cursor in self.cursors:
                        self.render_cursor(cursor, clear=True)
                    self.cursors = []
                if not self.animate:
                    self.map = self.maze_gen.generate_maze()
                    self.render_maze()
                else:
                    self.steps = self.maze_gen.generate_steps()
                    self.map = Maze(self.map.width, self.map.height)
                    # self.color_cells(Color(255, 255, 255, 50))
                    self.color_cells(Color(255, 255, 255))
                    print("coloring...")
                    self.start_animation = True
                    # self._maze.clear(Color(255, 255, 255))

            case 0x61:
                if not self.animate:
                    self.animate = True
                else:
                    self.animate = False
                # print(self.animate)
            case _:
                print(f"keycode: {hex(keycode)}")

    def expose_hook(self, param):
        self.render_bg()
        self.render_maze()

    def loop_hook(self, param):
        if self.start_animation:
            self.animate_maze()
            # print("animating...")

    def display(self):
        self.init_mlx()
        self._mlx.mlx_hook(self._window, 33, 0, self.quit_gui, None)
        self._mlx.mlx_key_hook(self._window, self.key_hook, None)
        self._mlx.mlx_expose_hook(self._window, self.expose_hook, None)
        self._mlx.mlx_loop_hook(self._mlx_ptr, self.loop_hook, None)
        self._mlx.mlx_loop(self._mlx_ptr)
