from mazegen import MazeGenerator, Maze, Cell
from typing import Callable
from ._display import Frame
from ._color import Color
from time import sleep


class Tui:
    """
    Terminal-based interface (TUI) for interacting with a maze generator.

    This class allows visualizing maze generation and solution paths
    in the terminal using ASCII/ANSI graphics. It supports animation,
    showing solution paths, reseeding, and color changes.

    Attributes:
        show_path (bool): Whether to display the solution path.
        animation (bool): Whether animations are enabled.
    """

    show_path: bool

    def __init__(
            self,
            mazegen: MazeGenerator,
            write_output: Callable[[str], None]
    ) -> None:
        self.mazegen = mazegen
        self.animation = True
        self.show_path = False
        self._write_output = write_output

    def animate(self) -> None:
        """
        Animate the maze generation step by step in the terminal.

        Displays the cells as they are generated with a short delay
        between steps. Highlights recently visited cells and updates
        the terminal output dynamically.
        """
        steps = self.mazegen.generate_steps()

        passed_by = set()

        last_cells: list[Cell] = []

        maze = Maze(
            self.mazegen.maze.width,
            self.mazegen.maze.height,
            (self.mazegen.maze.entry.x, self.mazegen.maze.entry.y),
            (self.mazegen.maze.exit.x, self.mazegen.maze.exit.y)
        )

        Frame.clear()
        for s in steps:
            passed_by.add(maze.map[s.y][s.x])
            Frame.draw(
                maze.apply_step(s.x, s.y, s.wall),
                passed_by,
                cursors=last_cells
            )
            last_cells.append(maze.map[s.y][s.x])
            if len(last_cells) > 5:
                last_cells = last_cells[1:6]
            sleep(0.009)
        Frame.draw(maze)

    def display(self, path: set[Cell] = set(), animate: bool = False) -> None:
        """
        Display the maze in the terminal.

        Depending on the configuration and parameters, this method can
        display the solution path, animate the generation, or simply
        render the current maze.

        Args:
            path (set[Cell], optional): Cells to highlight as the solution path
                Defaults to empty set.
            animate (bool, optional): Whether to animate the generation steps.
                Defaults to False.
        """
        if self.show_path or path:
            Frame.clear()
            if not self.show_path:
                path = set()
            Frame.draw(self.mazegen.maze, path_cell=path)
        elif self.animation and animate:
            self.animate()
        else:
            Frame.clear()
            Frame.draw(self.mazegen.maze)

    def run(self) -> None:
        """
        Run the terminal interface, handling user input and updating display.

        Provides an interactive loop where the user can:
        - Reseed and regenerate the maze
        - Change colors
        - Toggle animation
        - Show or hide the solution path
        - Exit the interface
        """
        Frame.clear()
        Frame.draw(self.mazegen.generate_maze())
        self._print_options()
        self._write_output(self.mazegen.output())

        self.show_path = False
        path: set[Cell] = set()
        animate: bool = False
        while True:
            match input(">>"):
                case "1":
                    self.mazegen.reseed()
                    self.mazegen.generate_maze()
                    path = set()
                    self.show_path = False
                    animate = True
                case "2":
                    Color.change()
                case "3":
                    self.animation = not self.animation
                case "4":
                    self.show_path = not self.show_path
                    if self.show_path:
                        path = {
                            step[0] for step in
                            self.mazegen.generate_path(self.mazegen.maze)
                        }
                case "0":
                    break
                case _:
                    continue

            self.display(path, animate)
            self._print_options()
            animate = False

    def _print_options(self) -> None:
        print("1. Regenerate Maze")
        print("2. Change color")
        print(f"3. {'Enable' if not self.animation else 'Disable'} Animation")
        print(f"4. {'Hide' if self.show_path else 'Show'} path")
        print("0. Exit")
