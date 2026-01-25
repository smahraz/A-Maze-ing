from mazegen import MazeGenerator, Maze
from ._display import Frame, Color
from time import sleep


class Tui:
    def __init__(self, mazegen: MazeGenerator) -> None:
        self.mazegen = mazegen
        self.animation = False

    def animate(self) -> None:
        def cell_bg(cell) -> str:
            if (cell.x == s.x and cell.y == s.y) or cell in last_cells:
                return Color.GREEN_BG

            return Color.WHITE_BG if cell not in passed_by else ''

        steps = self.mazegen.generate_steps()

        passed_by = set()

        last_cells = []

        maze = Maze(
            self.mazegen.maze.width,
            self.mazegen.maze.height
        )

        Frame.clear()
        for s in steps:
            passed_by.add(maze.map[s.y][s.x])
            Frame.draw(
                maze.apply_step(s.x, s.y, s.wall),
                cell_bg
            )
            last_cells.append(maze.map[s.y][s.x])
            if len(last_cells) > 5:
                last_cells = last_cells[1:6]
            sleep(0.009)
        Frame.draw(maze)

    def display(self) -> None:
        if self.animation:
            self.animate()
        else:
            Frame.clear()
            Frame.draw(self.mazegen.generate_maze())

    def run(self) -> None:
        while True:
            self.display()
            self._print_options()
            match input(">>"):
                case "0":
                    self.animation = not self.animation
                case "1":
                    self.mazegen.reseed()

    def _print_options(self) -> None:
        print(f"0. {'Enable' if not self.animation else 'Disable'} Animation")
        print("1. Regenerate Maze")
