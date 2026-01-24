from random import Random
from mazegen import Map
from mazegen.algo import DFS
from mazegen.utils import Step


class MazeGenerator:
    def __init__(self, width: int, height: int, seed: int) -> None:
        self.map = Map(width, height)
        self.seed = seed

    def generate_maze(self) -> Map:
        return self._generate(False)[0]

    def generate_steps(self) -> list[Step]:
        return self._generate()[1]

    def generate(self) -> tuple[Map, list[Step]]:
        pass

    def _generate(self, save_step: bool = True) -> tuple[Map, list[Step]]:
        return DFS(self.map, save_step, Random(self.seed))
