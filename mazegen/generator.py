from random import Random, randint
from mazegen import Maze, Step, Cell
from mazegen.algo import DFS, PRIM
from .path_finder import path_finder


class MazeGenerator:
    """
        Generate mazes using different algorithms and manage generation
        settings.

        This class provides methods to generate a maze using depth-first search
        (DFS) or Prim's algorithm, optionally record generation steps, and
        produce outputs such as maze encoding and solution paths. It supports
        reseeding for random generation and allows retrieving either the maze,
        the steps, or both.

        Attributes:
            maze (Maze): The current maze being generated.
            algorithm (str): The algorithm to use for generation
            ("DFS" or "PRIM").
            perfect (bool): Whether the generated maze should be perfect
            (no loops).
            seed (int): The random seed used for generation.
        """
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
        """
        Assign a new random seed for maze generation.

        The seed is chosen randomly between 0 and 999,999,999.
        """
        self.seed = randint(0, 999_999_999)

    def generate_maze(self) -> Maze:
        """
        Generate a maze without saving generation steps.

        Returns:
            Maze: The generated maze.
        """
        return self._generate(False)[0]

    def generate_steps(self) -> list[Step]:
        """
        Generate a maze and return the steps taken during generation.

        Returns:
            list[Step]: The list of steps recorded during maze generation.
        """
        return self._generate()[1]

    def generate(self) -> tuple[Maze, list[Step]]:
        """
        Generate a maze and optionally record steps.

        Returns:
            tuple[Maze, list[Step]]: A tuple containing the generated maze
            and the list of steps taken during generation.
        """
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
        """
        Compute a path through the given maze.

        This static method uses the path_finder function to determine
        a path from the maze entry to the exit.

        Args:
            maze (Maze): The maze to find a path in.

        Returns:
            list[tuple[Cell, str]]: A list of tuples where each tuple
            contains a cell and the direction taken from that cell.
        """
        return path_finder(maze)

    def output(self) -> str:
        """
        Produce a string representation of the maze with its path.

        The output includes the maze encoding, the entry and exit
        coordinates, and a sequence of directions representing the
        computed path through the maze.

        Returns:
            str: The formatted string representing the maze and its path.
        """
        return (
            self.maze.encode() +
            "\n\n" +
            f"{self.maze.entry.x},{self.maze.entry.x}\n" +
            f"{self.maze.exit.x},{self.maze.exit.x}\n" +
            "".join(_[1] for _ in self.generate_path(self.maze)) +
            "\n"
        )
