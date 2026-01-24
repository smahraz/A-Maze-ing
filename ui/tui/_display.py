from mazegen import Maze, Cell
from typing import Callable


class Frame:
    @staticmethod
    def display(maze: Maze, inside_cell: Callable | None = None) -> None:
        print("\033[H", end="")
        for i, row in enumerate(maze.map):
            if i == 0:
                Frame._border(len(row))
            Frame._vertical(row, inside_cell)
            Frame._horizontal(row)

    @staticmethod
    def clear() -> None:
        print("\033[2J", end="")

    @staticmethod
    def _vertical(row: list[Cell], inside_cell: Callable | None):
        print("║", end="")
        for cell in row:
            print(inside_cell(cell) if inside_cell else "  ", end="")
            print("║" if cell.east.is_closed else " ", end="")
        print()

    @staticmethod
    def _horizontal(row: list[Cell]):
        print('+', end="")
        for cell in row:
            if cell.south.is_closed:
                print("--+",  end="")
            else:
                if cell.right_cell and not cell.right_cell.south.is_closed \
                    and cell.below_cell and not cell.below_cell.east.is_closed\
                        and not cell.east.is_closed:
                    print(" "*3, end="")
                else:
                    print("  +", end="")
        print()

    @staticmethod
    def _border(row_len: int) -> None:
        print("+--" * row_len, end="+\n")
