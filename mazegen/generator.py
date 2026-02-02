from random import Random, randint
from mazegen import Maze, Step, Cell
from mazegen.algo import DFS, PRIM
from .path_finder import path_finder


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        algorithm: str,
        perfect: bool,
        seed: int,
        entry: tuple[int, int],
        exit: tuple[int, int]
    ) -> None:
        self.maze = Maze(width, height, entry, exit)
        self.algorithm = algorithm
        self.perfect = perfect
        self.seed = seed

    def reseed(self) -> None:
        self.seed = randint(0, 999_999_999)

    def generate_maze(self) -> Maze:
        return self._generate(False)[0]

    def generate_steps(self) -> list[Step]:
        return self._generate()[1]

    def generate(self) -> tuple[Maze, list[Step]]:
        return self._generate()

    def _generate(self, save_step: bool = True) -> tuple[Maze, list[Step]]:
        self.maze = Maze(self.maze.width, self.maze.height,
                         (self.maze.entry.x, self.maze.entry.y),
                         (self.maze.exit.x, self.maze.exit.y)
                         )
        if self.algorithm == "DFS":
            return DFS(
                self.maze,
                save_step,
                self.perfect,
                Random(self.seed)
            )
        return PRIM(
                self.maze,
                save_step,
                self.perfect,
                Random(self.seed)
            )

    @staticmethod
    def generate_path(maze: Maze) -> list[tuple[Cell, str]]:
        return path_finder(maze)

    def output(self) -> str:
        return (
            self.maze.encode() +
            "\n\n" +
            f"{self.maze.entry.x},{self.maze.entry.x}\n" +
            f"{self.maze.exit.x},{self.maze.exit.x}\n" +
            "".join(_[1] for _ in self.generate_path(self.maze)) +
            "\n"
        )
