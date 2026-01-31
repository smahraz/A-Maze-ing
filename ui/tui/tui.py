from mazegen import MazeGenerator, Maze, Cell
from ._display import Frame
from ._color import Color
from time import sleep


class Tui:
    def __init__(self, mazegen: MazeGenerator) -> None:
        self.mazegen = mazegen
        self.animation = True

    def animate(self) -> None:
        steps = self.mazegen.generate_steps()

        passed_by = set()

        last_cells = []

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
                passed_by
            )
            last_cells.append(maze.map[s.y][s.x])
            if len(last_cells) > 5:
                last_cells = last_cells[1:6]
            sleep(0.009)
        Frame.draw(maze)

    def display(self, path: set[Cell] = set()) -> None:
        if path:
            Frame.clear()
            Frame.draw(self.mazegen.maze, path_cell=path)
        elif self.animation:
            self.animate()
        else:
            Frame.clear()
            Frame.draw(self.mazegen.generate_maze())

    def run(self) -> None:
        Frame.clear()
        Frame.draw(self.mazegen.generate_maze())
        self._print_options()

        path: list[Cell | None] = []
        while True:
            match input(">>"):
                case "1":
                    self.mazegen.reseed()
                case "2":
                    Color.change()
                case "3":
                    self.animation = not self.animation
                case "4":
                    if path and path[0] is not None:
                        path = [None]
                    else:
                        path = {
                            step[0] for step in
                            self.mazegen.generate_path(self.mazegen.maze)
                        }
                    self.display(path)
                    self._print_options()
                    continue
                case "0":
                    break
                case _:
                    continue

            self.display()
            self._print_options()
            path = []

    def _print_options(self) -> None:
        print("1. Regenerate Maze")
        print("2. Change color")
        print(f"3. {'Enable' if not self.animation else 'Disable'} Animation")
        print("0. Exit")
