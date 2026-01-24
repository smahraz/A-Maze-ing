from random import Random
from mazegen import Maze, Step
from mazegen.algo import DFS


class MazeGenerator:
    def __init__(self, width: int, height: int, seed: int) -> None:
        self.maze = Maze(width, height)
        self.seed = seed

    def generate_maze(self) -> Maze:
        return self._generate(False)[0]

    def generate_steps(self) -> list[Step]:
        return self._generate()[1]

    def generate(self) -> tuple[Maze, list[Step]]:
        return self._generate()

    def _generate(self, save_step: bool = True) -> tuple[Maze, list[Step]]:
        return DFS(self.maze, save_step, Random(self.seed))
