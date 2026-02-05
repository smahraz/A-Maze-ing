from mlx import Mlx
from mazegen import Maze, Cell, Step
from .color import Color
from .image import Image
from typing import Any


class Png(Image):
    """
    Load and represent a PNG image for rendering.

    This class extends Image to load a PNG file from disk
    and make it available for rendering in the GUI.

    Attributes:
        image: The MLX image handle.
        height (int): The height of the image in pixels.
        width (int): The width of the image in pixels.
    """

    def __init__(self, mlx: Mlx, mlx_ptr: Any, file_name: str):
        """
        Load a PNG image from a file.

        Args:
            mlx (Mlx): The MLX library instance.
            mlx_ptr: The MLX context pointer.
            file_name (str): Path to the PNG file.
        """
        self._mlx = mlx
        self._mlx_ptr = mlx_ptr
        self.image, self.height, self.width = mlx.mlx_png_file_to_image(
            mlx_ptr, file_name
        )


class Renderer:
    """
    Handle all rendering operations for the maze GUI.

    This class manages the visual representation of the maze,
    including walls, cells, cursors, paths, and UI elements.
    It uses MLX for low-level image manipulation.

    Attributes:
        maze (Maze): The maze being rendered.
        cell_size (int): Size of each cell in pixels.
        stroke (int): Width of wall strokes in pixels.
        border (int): Border size around the maze.
        width (int): Total width of the rendering area.
        height (int): Total height of the rendering area.
        animate (bool): Whether animation mode is active.
        path (bool): Whether path display is active.
    """

    def __init__(self, maze: Maze, cell_size: int, stroke: int, border: int):
        """
        Initialize a Renderer for the given maze.

        Args:
            maze (Maze): The maze to render.
            cell_size (int): Size of each cell in pixels.
            stroke (int): Width of wall strokes in pixels.
            border (int): Border size around the maze.
        """
        self.maze = maze
        self.cell_size = cell_size
        self.stroke = stroke
        self.border = border
        self._maze_image: Image
        self._bg_image: Image
        self._mlx_ptr = None
        self._window = None
        self._bg_color = Color(45, 42, 64)
        self._wall_color = Color(255, 255, 255)
        self._cursor_color = Color(255, 0, 0)
        self._pattern_color = Color(0, 0, 255)
        self._unvisited_color = Color(142, 135, 191)
        self._path_color = Color(255, 0, 255)
        maze_width = cell_size * maze.width + border * 2 + stroke
        min_width = 1000
        self.width = max(maze_width, min_width)
        self.maze_x_offset = (self.width - maze_width) // 2
        self.height = cell_size * maze.height + border * 2 + stroke
        self.cursors: list[Cell] = []
        self.protected_cells: set[Cell] = set()
        self.info_height: int = 100
        self.animate = False
        self.path = False

    def init_mlx(self, mlx: Mlx, mlx_ptr: Any, window: Any) -> None:
        """
        Initialize MLX references for rendering.

        Args:
            mlx (Mlx): The MLX library instance.
            mlx_ptr: The MLX context pointer.
            window: The window handle for rendering.
        """
        self._mlx = mlx
        self._mlx_ptr = mlx_ptr
        self._window = window

    def init_images(self) -> None:
        """
        Initialize all image buffers and load PNG assets.

        This method creates the maze and background images,
        and loads all button and text PNG assets for the UI.
        """
        self._maze_image = Image(
            self._mlx,
            self._mlx_ptr,
            self.width - self.border * 2,
            self.height - self.border * 2
        )
        self._maze_image.clear(self._bg_color)
        self._bg_image = Image(
            self._mlx,
            self._mlx_ptr,
            self.width,
            self.height + self.info_height
        )
        self.button_a = Png(
            self._mlx, self._mlx_ptr, "assets/button_a.png")
        self.button_a_on = Png(
            self._mlx, self._mlx_ptr, "assets/button_a_on.png")
        self.button_r = Png(
            self._mlx, self._mlx_ptr, "assets/button_r.png")
        self.button_c = Png(
            self._mlx, self._mlx_ptr, "assets/button_c.png")
        self.button_p = Png(
            self._mlx, self._mlx_ptr, "assets/button_p.png")
        self.button_p_on = Png(
            self._mlx, self._mlx_ptr, "assets/button_p_on.png")
        self.button_esc = Png(
            self._mlx, self._mlx_ptr, "assets/button_esc.png")
        self.text_exit = Png(
            self._mlx, self._mlx_ptr, "assets/text_exit.png")
        self.text_regen = Png(
            self._mlx, self._mlx_ptr, "assets/text_regen.png")
        self.text_path = Png(
            self._mlx, self._mlx_ptr, "assets/text_path.png")
        self.text_colors = Png(
            self._mlx, self._mlx_ptr, "assets/text_colors.png")
        self.text_animation = Png(
            self._mlx, self._mlx_ptr, "assets/text_animation.png")

    def render_bg(self) -> None:
        """
        Render the background color to the window.

        This method fills the entire background image with the
        background color and displays it in the window.
        """
        for x in range(self.width):
            for y in range(self.height + self.info_height):
                self._bg_image.put_pixel(x, y, self._bg_color)
        self._bg_image.put_to_win(
            self._window,
            0, 0
        )

    def render_wall(self, cell: Cell, dir: str, color: Color) -> None:
        """
        Render a wall of a cell in the specified direction.

        Args:
            cell (Cell): The cell whose wall to render.
            dir (str): The direction of the wall ('N', 'E', 'S', 'W').
            color (Color): The color to render the wall.
        """
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

    def render_corner(self, cell: Cell, pos: str, color: Color) -> None:
        """
        Render a corner of a cell.

        Args:
            cell (Cell): The cell whose corner to render.
            pos (str): The corner position ('NW', 'NE', 'SW', 'SE').
            color (Color): The color to render the corner.
        """
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
        """
        Fill a cell with a solid color.

        Args:
            cell (Cell): The cell to color.
            color (Color): The color to fill the cell with.
        """
        x = cell.x * self.cell_size + self.stroke
        y = cell.y * self.cell_size + self.stroke

        for w in range(self.cell_size - self.stroke):
            for h in range(self.cell_size - self.stroke):
                self._maze_image.put_pixel(x + w, y + h, color)

    def color_cells_walls(self, color: Color) -> None:
        """
        Fill all cells and walls with a single color.

        This method is used to reset the maze display or prepare
        for animation by coloring all cells uniformly.

        Args:
            color (Color): The color to fill all cells and walls.
        """
        for cell in self.maze.cell_iterator():
            if cell != self.maze.entry and cell != self.maze.exit:
                self.color_cell(cell, color)
            self.render_wall(cell, 'N', color)
            self.render_wall(cell, 'S', color)
            self.render_wall(cell, 'E', color)
            self.render_wall(cell, 'W', color)
            self.render_corner(cell, 'NE', color)
            self.render_corner(cell, 'NW', color)
            self.render_corner(cell, 'SE', color)
            self.render_corner(cell, 'SW', color)

    def render_protected(self) -> None:
        """
        Render all protected cells with special coloring.

        Protected cells (the "42" pattern) are rendered with
        the pattern color, and walls between protected cells
        are colored to create a solid pattern appearance.
        """
        for cell in self.protected_cells:
            self.color_cell(cell, self._pattern_color)
            self.render_wall(cell, 'N', self._wall_color)
            self.render_wall(cell, 'S', self._wall_color)
            self.render_wall(cell, 'E', self._wall_color)
            self.render_wall(cell, 'W', self._wall_color)
            self.render_corner(cell, 'NE', self._wall_color)
            self.render_corner(cell, 'NW', self._wall_color)
            self.render_corner(cell, 'SE', self._wall_color)
            self.render_corner(cell, 'SW', self._wall_color)
            if cell.above_cell and cell.above_cell.is_protected:
                self.render_wall(cell, 'N', self._pattern_color)
            if cell.below_cell and cell.below_cell.is_protected:
                self.render_wall(cell, 'S', self._pattern_color)
            if cell.right_cell and cell.right_cell.is_protected:
                self.render_wall(cell, 'E', self._pattern_color)
            if cell.left_cell and cell.left_cell.is_protected:
                self.render_wall(cell, 'W', self._pattern_color)

    def render_cell(self, cell: Cell) -> None:
        """
        Render a single cell with its walls and corners.

        This method draws the walls and corners of a cell based
        on their open/closed state and neighbouring cells.

        Args:
            cell (Cell): The cell to render.
        """
        if cell.is_protected:
            if cell not in self.protected_cells:
                if len(self.protected_cells) >= 18:
                    self.protected_cells = set()
                self.protected_cells.add(cell)
            return
        if cell.north.is_closed or not cell.above_cell:
            self.render_wall(cell, 'N', self._wall_color)
        else:
            self.render_wall(cell, 'N', self._bg_color)
        if cell.east.is_closed or not cell.right_cell:
            self.render_wall(cell, 'E', self._wall_color)
        else:
            self.render_wall(cell, 'E', self._bg_color)
        if cell.south.is_closed or not cell.below_cell:
            self.render_wall(cell, 'S', self._wall_color)
        else:
            self.render_wall(cell, 'S', self._bg_color)
        if cell.west.is_closed or not cell.left_cell:
            self.render_wall(cell, 'W', self._wall_color)
        else:
            self.render_wall(cell, 'W', self._bg_color)

        if (cell.north.is_closed or
                (cell.above_cell and cell.above_cell.west.is_closed) or
                cell.west.is_closed or
                (cell.left_cell and cell.left_cell.north.is_closed)):
            self.render_corner(cell, 'NW', self._wall_color)
        else:
            self.render_corner(cell, 'NW', self._bg_color)

        if (cell.south.is_closed or
                (cell.below_cell and cell.below_cell.west.is_closed) or
                cell.west.is_closed or
                (cell.left_cell and cell.left_cell.south.is_closed)):
            self.render_corner(cell, 'SW', self._wall_color)
        else:
            self.render_corner(cell, 'SW', self._bg_color)

        if (cell.north.is_closed or
                (cell.above_cell and cell.above_cell.east.is_closed) or
                cell.east.is_closed or
                (cell.right_cell and cell.right_cell.north.is_closed)):
            self.render_corner(cell, 'NE', self._wall_color)
        else:
            self.render_corner(cell, 'NE', self._bg_color)

        if (cell.south.is_closed or
                (cell.below_cell and cell.below_cell.east.is_closed) or
                cell.east.is_closed or
                (cell.right_cell and cell.right_cell.south.is_closed)):
            self.render_corner(cell, 'SE', self._wall_color)
        else:
            self.render_corner(cell, 'SE', self._bg_color)

    def render_cursor(self, cell: Cell, clear: bool = False) -> None:
        """
        Render or clear a cursor highlight on a cell.

        Args:
            cell (Cell): The cell to render the cursor on.
            clear (bool, optional): If True, clears the cursor.
                Defaults to False.
        """
        if cell == self.maze.entry or cell == self.maze.exit:
            return
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
        """
        Render the complete maze to the display.

        This method iterates through all cells, renders them,
        highlights protected cells and entry/exit points,
        and displays the result.
        """
        for cell in self.maze.cell_iterator():
            self.render_cell(cell)
        self.render_protected()
        self.color_cell(self.maze.entry, Color(0, 255, 0))
        self.color_cell(self.maze.exit, Color(255, 0, 0))
        self.display_maze()

    def display_maze(self) -> None:
        """
        Display the maze image in the window.

        This method puts the maze image to the window at the
        correct position with border and info panel offsets.
        """
        self._maze_image.put_to_win(
            self._window,
            self.border + self.maze_x_offset,
            self.border + self.info_height
        )

    def render_info(self) -> None:
        """
        Render the info panel with control buttons and labels.

        This method displays the UI buttons and their text labels
        at the top of the window, showing the current state of
        animation and path toggles.
        """
        button_a = self.button_a_on if self.animate else self.button_a
        button_p = self.button_p_on if self.path else self.button_p
        info_items: list[dict[str, Any]] = [
            {'button': self.button_esc, 'text': self.text_exit,
             'text_offset_x': 21, 'text_offset_y': 50},
            {'button': self.button_r, 'text': self.text_regen,
             'text_offset_x': -50, 'text_offset_y': 50},
            {'button': button_a, 'text': self.text_animation,
             'text_offset_x': -38, 'text_offset_y': 50},
            {'button': self.button_c, 'text': self.text_colors,
             'text_offset_x': -62, 'text_offset_y': 50},
            {'button': button_p, 'text': self.text_path,
             'text_offset_x': -5, 'text_offset_y': 50},
        ]

        available_width = self.width - 2 * self.border
        num_items = len(info_items)
        spacing = available_width // (num_items + 1) if num_items > 0 else 0

        for i, item in enumerate(info_items):
            x_pos = self.border + spacing * (i + 1) - 23
            y_button = self.border
            y_text = self.border + item['text_offset_y']
            item['button'].put_to_win(self._window, x_pos, y_button)
            item['text'].put_to_win(
                self._window, x_pos + item['text_offset_x'], y_text)

    def render_animation_step(self, steps: list[Step]) -> bool:
        """
        Render one step of the generation animation.

        This method applies the next generation step to the maze,
        renders the affected cell, and updates cursor positions.

        Args:
            steps (list[Step]): The remaining steps to animate.

        Returns:
            bool: True if animation is complete, False otherwise.
        """
        if not steps:
            return True
        step = steps[0]
        self.maze.apply_step(step.x, step.y, step.wall)
        self.render_cell(self.maze.map[step.y][step.x])
        for s in steps[:5]:
            self.render_cursor(self.maze.map[s.y][s.x])
            self.cursors.append(self.maze.map[s.y][s.x])
        self.render_cursor(self.maze.map[step.y][step.x], clear=True)

        self.display_maze()
        return False

    def clear_cursors(self) -> None:
        """
        Clear all cursor highlights from the display.

        This method removes the cursor highlighting from all
        cells that were previously marked as cursors.
        """
        for cursor in self.cursors:
            self.render_cursor(cursor, clear=True)
        self.cursors = []

    def render_path(
            self, path: list[tuple[Cell, str]], clear: bool = False) -> None:
        """
        Render or clear the solution path on the maze.

        This method highlights the cells along the solution path
        and the walls between them.

        Args:
            path (list[tuple[Cell, str]]): The path to render,
                as a list of (cell, direction) tuples.
            clear (bool, optional): If True, clears the path.
                Defaults to False.
        """
        color = self._bg_color if clear else self._path_color
        for cell, dir in path:
            if cell != self.maze.entry:
                self.color_cell(cell, color)
            self.render_wall(cell, dir, color)

        self.display_maze()
