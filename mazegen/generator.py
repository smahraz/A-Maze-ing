from random import Random, randint
from mazegen import Maze, Step
from mazegen.algo import DFS, PRIM


class MazeGenerator:
    def __init__(
            self, width: int, height: int, algorithm: str, seed: int) -> None:
        self.maze = Maze(width, height)
        self.algorithm = algorithm
        self.seed = seed

    def reseed(self) -> None:
        self.maze = Maze(self.maze.width, self.maze.height)
        self.seed = randint(0, 999_999_999)

    def generate_maze(self) -> Maze:
        return self._generate(False)[0]

    def generate_steps(self) -> list[Step]:
        return self._generate()[1]

    def generate(self) -> tuple[Maze, list[Step]]:
        return self._generate()

    def _generate(self, save_step: bool = True) -> tuple[Maze, list[Step]]:
        match self.algorithm:
            case "DFS":
                output = DFS(self.maze, save_step, Random(self.seed))
            case "PRIM":
                output = PRIM(self.maze, save_step, Random(self.seed))
        return output
