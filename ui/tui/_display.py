from mazegen import Maze, Cell
from typing import Callable
from ._color import Color


class Frame:
    @staticmethod
    def draw(maze: Maze, cell_bg: Callable | None = None) -> None:
        print("\033[H", end="")
        for row in maze.map:
            if not row[0].above_cell:
                Frame._render_ceiling(row)
            Frame._vertical(row, cell_bg)
            Frame._horizontal(row)

    @staticmethod
    def clear() -> None:
        print("\033[2J", end="")

    @staticmethod
    def _vertical(row: list[Cell], cell_bg: Callable | None):
        Frame._print("║")
        for cell in row:
            if not cell.is_protected:
                if cell_bg:
                    Frame._print(cell_bg(cell), " " * 2)
                else:
                    Frame._print(" " * 2)
            else:
                Frame._print(Color.protected_cell, " " * 2)

            Frame._print("║" if cell.east.is_closed else " ")

        print()

    @staticmethod
    def _horizontal(row: list[Cell]):
        if not row[0].left_cell:
            if row[0].below_cell:
                Frame._print("╠" if row[0].south.is_closed else "║")
            else:
                Frame._print("╚")

        for cell in row:
            Frame._print("═" * 2 if cell.south.is_closed else " " * 2)

            join = Frame._get_join(
                cell.east.is_closed,
                cell.right_cell.south.is_closed if cell.right_cell else False,
                cell.below_cell.east.is_closed if cell.below_cell else False,
                cell.south.is_closed
            )
            Frame._print(join)
        print()

    @staticmethod
    def _get_join(n: bool, e: bool, s: bool, w: bool) -> str:
        if n & e & s & w:
            return "╬"

        if n & e & w:
            return "╩"
        if s & e & w:
            return "╦"
        if s & n & w:
            return "╣"
        if s & n & e:
            return "╠"

        if w & s:
            return "╗"
        if s & e:
            return "╔"
        if e & n:
            return "╚"
        if n & w:
            return "╝"

        if n | s:
            return "║"
        if w | e:
            return "═"

        return " "

    @staticmethod
    def _render_ceiling(row: list[Cell]) -> None:
        Frame._print('╔')

        for cell in row:
            Frame._print("═" * 2)
            if cell.right_cell:
                Frame._print("╦" if cell.east.is_closed else "═")

        Frame._print('╗')
        print(Color.DEFAULT)

    @staticmethod
    def _print(*args, end=Color.DEFAULT) -> None:
        print(Color.bg, Color.wall, *args, end=end, sep="")
