from mlx import Mlx
from mazegen import MazeGenerator, Maze, Step, Cell
from .color import Color
from .renderer import Renderer
from typing import Any, Callable


class Keys:
    ESC = 0xff1b
    R = 0x72
    A = 0x61
    C = 0x63
    P = 0x70


class Gui:
    def __init__(self, maze_gen: MazeGenerator, write_output: Callable):
        self.maze_gen = maze_gen
        self.map = maze_gen.generate_maze()
        write_output(self.maze_gen.output())
        self.renderer = self._init_renderer(self.map)

        self._mlx = Mlx()

        self.init_mlx()

        self.animate = False
        self.path = False
        self.start_animation = False
        self.start_path_animation = False
        self.steps: list[Step] = []
        self.path_list: list[tuple[Cell, str]] = []
        self.steps_done: list[Step] = []

    def _init_renderer(self, map: Maze) -> Renderer:
        border, cell_size, stroke = self._compute_params(map)
        return Renderer(map, cell_size, stroke, border)

    def _compute_params(self, map: Maze) -> tuple[int, int, int]:
        if map.width <= 50 and map.height <= 25:
            return 40, 32, 8
        elif map.width <= 100 and map.height <= 50:
            return 20, 16, 4
        elif map.width <= 200 and map.height <= 100:
            return 10, 8, 2
        elif map.width <= 400 and map.height <= 200:
            return 5, 4, 1
        else:
            return 0, 2, 1

    def quit_gui(self, param: Any = None) -> None:
        self._mlx.mlx_loop_exit(self._mlx_ptr)

    def init_mlx(self) -> None:
        self._mlx_ptr = self._mlx.mlx_init()

        self._window = self._mlx.mlx_new_window(
            self._mlx_ptr,
            self.renderer.width,
            self.renderer.height + self.renderer.info_height,
            "A-Maze-ing"
        )
        self.renderer.init_mlx(
            self._mlx, self._mlx_ptr, self._window)
        self.renderer.init_images()

    def animate_maze(self) -> None:
        done = self.renderer.render_animation_step(self.steps)
        if done:
            self.start_animation = False
            self.renderer.color_cells_walls(self.renderer._bg_color)
            self.renderer.clear_cursors()
            self.steps_done = []
            self.renderer.render_maze()
        else:
            self.steps_done.append(self.steps[0])
            self.steps = self.steps[1:]

    def key_hook(self, keycode: int, param: Any) -> None:
        match keycode:
            case Keys.ESC:
                self.quit_gui()

            case Keys.R:
                self.maze_gen.reseed()

                if self.path:
                    self.path = False
                    self.renderer.path = False
                    self.renderer.render_info()
                    self.renderer.render_path(self.path_list, clear=True)

                if self.start_animation:
                    self.start_animation = False
                    self.renderer.color_cells_walls(self.renderer._bg_color)
                    self.steps_done = []

                if self.animate:
                    self.steps = self.maze_gen.generate_steps()
                    self.map = Maze(self.map.width, self.map.height,
                                    (self.map.entry.x, self.map.entry.y),
                                    (self.map.exit.x, self.map.exit.y))
                    self.renderer.maze = self.map
                    self.renderer.color_cells_walls(
                        self.renderer._unvisited_color)
                    self.renderer.render_protected()
                    self.start_animation = True
                else:
                    self.map = self.maze_gen.generate_maze()
                    self.renderer.maze = self.map
                    self.renderer.render_maze()

            case Keys.A:
                self.animate = not self.animate
                self.renderer.animate = self.animate
                self.renderer.render_info()

            case Keys.P:
                if self.start_animation:
                    return

                self.path = not self.path
                self.renderer.path = self.path
                self.renderer.render_info()

                if self.path:
                    self.path_list = MazeGenerator.generate_path(self.map)
                    self.renderer.render_path(self.path_list)
                else:
                    self.renderer.render_path(self.path_list, clear=True)

            case Keys.C:
                self.renderer._wall_color = Color.get_random()
                self.renderer._pattern_color = Color.get_random()
                self.renderer._cursor_color = Color.get_random()
                self.renderer._path_color = Color.get_random()

                if self.steps_done:
                    for step in self.steps_done:
                        self.renderer.render_cell(self.map.map[step.y][step.x])
                else:
                    self.renderer.render_maze()
                    if self.path:
                        self.renderer.render_path(self.path_list)

                self.renderer.render_protected()

    def expose_hook(self, param: Any) -> None:
        self.renderer.render_bg()
        self.renderer.render_maze()
        self.renderer.render_info()

    def loop_hook(self, param: Any) -> None:
        if self.start_animation:
            self.animate_maze()

    def run(self) -> None:
        self._mlx.mlx_hook(self._window, 33, 0, self.quit_gui, None)
        self._mlx.mlx_key_hook(self._window, self.key_hook, None)
        self._mlx.mlx_expose_hook(self._window, self.expose_hook, None)
        self._mlx.mlx_loop_hook(self._mlx_ptr, self.loop_hook, None)
        self._mlx.mlx_loop(self._mlx_ptr)
