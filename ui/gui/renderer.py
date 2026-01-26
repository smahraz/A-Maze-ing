from mlx import Mlx
from mazegen import Maze, Cell, Step
from .color import Color
from .image import Image
from typing import Any


class Renderer:
    def __init__(self, maze: Maze, cell_size: int, stroke: int, border: int):
        self.maze = maze
        self.cell_size = cell_size
        self.stroke = stroke
        self.border = border
        self._maze_image: Image
        self._bg_image: Image
        self._mlx: Mlx
        self._mlx_ptr = None
        self._window = None
        self._bg_color = Color(45, 42, 64)
        self._wall_color = Color(255, 255, 255)
        self._cursor_color = Color(255, 0, 0)
        self._pattern_color = Color(0, 0, 255)
        self._unvisited_color = Color(142, 135, 191)
        self.width = cell_size * maze.width + border * 2 + stroke
        self.height = cell_size * maze.height + border * 2 + stroke
        self.cursors: list[Cell] = []
        self.protected_cells: list[Cell] = []

    def init_mlx(self, mlx: Any, mlx_ptr: Any, window: Any) -> None:
        self._mlx = mlx
        self._mlx_ptr = mlx_ptr
        self._window = window

    def init_images(self) -> None:
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

    def render_bg(self) -> None:
        for x in range(self.width):
            for y in range(self.height):
                self._bg_image.put_pixel(x, y, self._bg_color)
        self._mlx.mlx_put_image_to_window(
            self._mlx_ptr,
            self._window,
            self._bg_image.image,
            0, 0
        )

    def render_wall(self, cell: Cell, dir: str, clear: bool = False) -> None:
        color = self._wall_color if not clear else self._bg_color
        x = cell.x * self.cell_size
        y = cell.y * self.cell_size

        length = self.cell_size - self.stroke
        offset = self.cell_size

        match dir:
            case 'E':
                for w in range(self.stroke):
                    for h in range(length):
                        self._maze_image.put_pixel(
                            x + w + offset,
                            y + h + self.stroke,
                            color
                        )
            case 'S':
                for w in range(self.stroke):
                    for h in range(length):
                        self._maze_image.put_pixel(
                            x + h + self.stroke,
                            y + w + offset,
                            color
                        )
            case 'N':
                for w in range(self.stroke):
                    for h in range(length):
                        self._maze_image.put_pixel(
                            x + h + self.stroke,
                            y + w,
                            color
                        )
            case 'W':
                for w in range(self.stroke):
                    for h in range(length):
                        self._maze_image.put_pixel(
                            x + w,
                            y + h + self.stroke,
                            color
                        )

    def render_corner(self, cell: Cell, pos: str, clear: bool = False) -> None:
        color = self._wall_color if not clear else self._bg_color
        x = cell.x * self.cell_size
        y = cell.y * self.cell_size
        match pos:
            case 'NW':
                for w in range(self.stroke):
                    for h in range(self.stroke):
                        self._maze_image.put_pixel(
                            x + w,
                            y + h,
                            color
                        )
            case 'SW':
                for w in range(self.stroke):
                    for h in range(self.stroke):
                        self._maze_image.put_pixel(
                            x + w,
                            y + h + self.cell_size,
                            color
                        )
            case 'NE':
                for w in range(self.stroke):
                    for h in range(self.stroke):
                        self._maze_image.put_pixel(
                            x + w + self.cell_size,
                            y + h,
                            color
                        )
            case 'SE':
                for w in range(self.stroke):
                    for h in range(self.stroke):
                        self._maze_image.put_pixel(
                            x + w + self.cell_size,
                            y + h + self.cell_size,
                            color
                        )

    def color_cell(self, cell: Cell, color: Color) -> None:
        x = cell.x * self.cell_size
        y = cell.y * self.cell_size

        for w in range(self.cell_size + self.stroke):
            for h in range(self.cell_size + self.stroke):
                self._maze_image.put_pixel(x + w, y + h, color)

    def color_cells(self, color: Color) -> None:
        for cell in self.maze.cell_iterator():
            if cell.is_protected:
                continue
            self.color_cell(cell, color)

    def render_protected(self) -> None:
        for cell in self.protected_cells:
            self.color_cell(cell, self._pattern_color)
            self.render_wall(cell, 'N')
            self.render_wall(cell, 'E')
            self.render_wall(cell, 'W')
            self.render_wall(cell, 'S')
            self.render_corner(cell, 'NW')
            self.render_corner(cell, 'SW')
            self.render_corner(cell, 'NE')
            self.render_corner(cell, 'SE')

    def render_cell(self, cell: Cell) -> None:
        if cell.is_protected and len(self.protected_cells) < 18:
            self.protected_cells.append(cell)
            return
        if cell.north.is_closed or not cell.above_cell:
            self.render_wall(cell, 'N')
        else:
            self.render_wall(cell, 'N', clear=True)
        if cell.east.is_closed or not cell.right_cell:
            self.render_wall(cell, 'E')
        else:
            self.render_wall(cell, 'E', clear=True)
        if cell.south.is_closed or not cell.below_cell:
            self.render_wall(cell, 'S')
        else:
            self.render_wall(cell, 'S', clear=True)
        if cell.west.is_closed or not cell.left_cell:
            self.render_wall(cell, 'W')
        else:
            self.render_wall(cell, 'W', clear=True)

        if (cell.north.is_closed or
                (cell.right_cell and cell.right_cell.north.is_closed) or
                cell.west.is_closed or
                (cell.above_cell and cell.above_cell.west.is_closed)):
            self.render_corner(cell, 'NW')
        else:
            self.render_corner(cell, 'NW', clear=True)

        if (cell.north.is_closed or
                (cell.left_cell and cell.left_cell.north.is_closed) or
                cell.east.is_closed or
                (cell.above_cell and cell.above_cell.east.is_closed)):
            self.render_corner(cell, 'NE')
        else:
            self.render_corner(cell, 'NE', clear=True)

        if (cell.south.is_closed or
                (cell.right_cell and cell.right_cell.south.is_closed) or
                cell.west.is_closed or
                (cell.below_cell and cell.below_cell.west.is_closed)):
            self.render_corner(cell, 'SW')
        else:
            self.render_corner(cell, 'SW', clear=True)

        if (cell.south.is_closed or
                (cell.left_cell and cell.left_cell.south.is_closed) or
                cell.east.is_closed or
                (cell.below_cell and cell.below_cell.east.is_closed)):
            self.render_corner(cell, 'SE')
        else:
            self.render_corner(cell, 'SE', clear=True)

    def render_cursor(self, cell: Cell, clear: bool = False) -> None:
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

    def render_maze(self) -> None:
        for cell in self.maze.cell_iterator():
            self.render_cell(cell)
        self.render_protected()

        self._mlx.mlx_put_image_to_window(
            self._mlx_ptr,
            self._window,
            self._maze_image.image,
            self.border, self.border
        )

    def render_animation_step(self, steps: list[Step]) -> bool:
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

    def clear_cursors(self) -> None:
        for cursor in self.cursors:
            self.render_cursor(cursor, clear=True)
        self.cursors = []
