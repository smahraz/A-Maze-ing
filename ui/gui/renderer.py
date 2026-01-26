from mazegen import Maze, Cell
from .color import Color
from .image import Image


class Renderer:
    def __init__(self, maze: Maze, cell_size: int, stroke: int, border: int):
        self.maze = maze
        self.cell_size = cell_size
        self.stroke = stroke
        self.border = border
        self._maze_image: Image = None
        self._bg_image: Image = None
        self._mlx = None
        self._mlx_ptr = None
        self._window = None
        self._bg_color = Color.BG
        self._wall_color = Color.WHITE
        self._cursor_color = Color.RED
        self._pattern_color = Color.BLUE
        self.width = cell_size * maze.width + border * 2 + stroke
        self.height = cell_size * maze.height + border * 2 + stroke
        self.cursors = []

    def init_mlx(self, mlx, mlx_ptr, window):
        self._mlx = mlx
        self._mlx_ptr = mlx_ptr
        self._window = window

    def init_images(self):
        self._maze_image = Image(
            self._mlx,
            self._mlx_ptr,
            self.width - self.border * 2,
            self.height - self.border * 2
        )
        self._bg_image = Image(
            self._mlx,
            self._mlx_ptr,
            self.width,
            self.height
        )

    def render_bg(self):
        for x in range(self.width):
            for y in range(self.height):
                self._bg_image.put_pixel(x, y, self._bg_color)
        self._mlx.mlx_put_image_to_window(
            self._mlx_ptr,
            self._window,
            self._bg_image.image,
            0, 0
        )

    def render_wall(self, x, y, dir: str, clear: bool = False):
        color = self._wall_color if not clear else self._bg_color
        base_x = x * self.cell_size
        base_y = y * self.cell_size
        cs = self.cell_size
        st = self.stroke
        color_fmt = color.big() if not self._maze_image.form else (
            color.little()
        )
        stride = self._maze_image.sl
        bpp_bytes = self._maze_image.bpp // 8
        data = self._maze_image.data

        match dir:
            case 'E':
                for stroke in range(st):
                    for length in range(cs - st):
                        px = base_x + stroke + cs
                        py = base_y + length + st
                        offset = py * stride + px * bpp_bytes
                        data[offset:].cast("I")[0] = color_fmt
            case 'S':
                for stroke in range(st):
                    for length in range(cs - st):
                        px = base_x + length + st
                        py = base_y + stroke + cs
                        offset = py * stride + px * bpp_bytes
                        data[offset:].cast("I")[0] = color_fmt
            case 'N':
                for stroke in range(st):
                    for length in range(cs - st):
                        px = base_x + length + st
                        py = base_y + stroke
                        offset = py * stride + px * bpp_bytes
                        data[offset:].cast("I")[0] = color_fmt
            case 'W':
                for stroke in range(st):
                    for length in range(cs - st):
                        px = base_x + stroke
                        py = base_y + length + st
                        offset = py * stride + px * bpp_bytes
                        data[offset:].cast("I")[0] = color_fmt

    def render_corner(self, cell: Cell, pos: str, clear: bool = False):
        color = self._wall_color if not clear else self._bg_color
        base_x = cell.x * self.cell_size
        base_y = cell.y * self.cell_size
        cs = self.cell_size
        st = self.stroke
        color_fmt = color.big() if not self._maze_image.form else (
            color.little()
        )
        stride = self._maze_image.sl
        bpp_bytes = self._maze_image.bpp // 8
        data = self._maze_image.data

        match pos:
            case 'NW':
                for stroke in range(st):
                    for length in range(st):
                        px, py = base_x + stroke, base_y + length
                        offset = py * stride + px * bpp_bytes
                        data[offset:].cast("I")[0] = color_fmt
            case 'SW':
                for stroke in range(st):
                    for length in range(st):
                        px, py = base_x + stroke, base_y + length + cs
                        offset = py * stride + px * bpp_bytes
                        data[offset:].cast("I")[0] = color_fmt
            case 'NE':
                for stroke in range(st):
                    for length in range(st):
                        px = base_x + stroke + cs
                        py = base_y + length
                        offset = py * stride + px * bpp_bytes
                        data[offset:].cast("I")[0] = color_fmt
            case 'SE':
                for stroke in range(st):
                    for length in range(st):
                        px = base_x + stroke + cs
                        py = base_y + length + cs
                        offset = py * stride + px * bpp_bytes
                        data[offset:].cast("I")[0] = color_fmt

    def color_cell(self, cell: Cell, color: Color):
        base_x = cell.x * self.cell_size
        base_y = cell.y * self.cell_size
        cs = self.cell_size
        color_fmt = color.big() if not self._maze_image.form else (
            color.little()
        )
        stride = self._maze_image.sl
        bpp_bytes = self._maze_image.bpp // 8
        data = self._maze_image.data

        for w in range(cs):
            for h in range(cs):
                px, py = base_x + w, base_y + h
                offset = py * stride + px * bpp_bytes
                data[offset:].cast("I")[0] = color_fmt

    def color_cells(self, color: Color):
        for cell in self.maze.cell_iterator():
            if cell.is_protected:
                continue
            self.color_cell(cell, color)

    def render_protected(self, cell: Cell):
        self.color_cell(cell, self._pattern_color)
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
        elif cell.west.is_closed:
            self.render_wall(cell.x, cell.y, 'W')
        else:
            self.render_wall(cell.x, cell.y, 'W', clear=True)
        if cell.y == 0:
            self.render_wall(cell.x, 0, 'N')
            self.render_corner(cell, 'NW')
        elif cell.north.is_closed:
            self.render_wall(cell.x, cell.y, 'N')
        else:
            self.render_wall(cell.x, cell.y, 'N', clear=True)
        if cell.east.is_closed or cell.x == self.maze.width - 1:
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
        if cell.south.is_closed or cell.y == self.maze.height - 1:
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
        color = self._cursor_color if not clear else self._bg_color
        base_x = cell.x * self.cell_size + self.stroke
        base_y = cell.y * self.cell_size + self.stroke
        cs = self.cell_size - self.stroke
        color_fmt = color.big() if not self._maze_image.form else (
            color.little()
        )
        stride = self._maze_image.sl
        bpp_bytes = self._maze_image.bpp // 8
        data = self._maze_image.data

        for w in range(cs):
            for h in range(cs):
                px, py = base_x + w, base_y + h
                offset = py * stride + px * bpp_bytes
                data[offset:].cast("I")[0] = color_fmt

    def render_maze(self):
        for cell in self.maze.cell_iterator():
            self.render_cell(cell)

        self._mlx.mlx_put_image_to_window(
            self._mlx_ptr,
            self._window,
            self._maze_image.image,
            self.border, self.border
        )

    def render_animation_step(self, steps):
        if not steps:
            return True
        step = steps[0]
        self.maze.apply_step(step.x, step.y, step.wall)
        self.render_cell(self.maze.map[step.y][step.x])
        for s in steps[:5]:
            self.render_cursor(self.maze.map[s.y][s.x])
            self.cursors.append(self.maze.map[s.y][s.x])
        self.render_cursor(self.maze.map[step.y][step.x], clear=True)

        self._mlx.mlx_put_image_to_window(
            self._mlx_ptr,
            self._window,
            self._maze_image.image,
            self.border, self.border
        )
        return False

    def clear_cursors(self):
        for cursor in self.cursors:
            self.render_cursor(cursor, clear=True)
        self.cursors = []
