from mazegen import MazeGenerator, Maze
from ._display import Frame
from time import sleep


class Tui:
    def __init__(self, mazegen: MazeGenerator) -> None:
        self.mazegen = mazegen
        self.animation = True

    def animate(self) -> None:
        def inside_cell(cell) -> str:
            if (cell.x == s.x and cell.y == s.y) or cell in last_cells:
                return "\033[32m██\033[0m"

            return "██" if cell not in passed_by else "  "

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
            Frame.display(
                maze.apply_step(s.x, s.y, s.wall),
                inside_cell
            )
            last_cells.append(maze.map[s.y][s.x])
            if len(last_cells) > 5:
                last_cells = last_cells[1:6]
            sleep(0.009)
        Frame.display(maze)

    def display(self) -> None:
        if self.animation:
            self.animate()
        else:
            Frame.clear()
            Frame.display(self.mazegen.generate_maze())
