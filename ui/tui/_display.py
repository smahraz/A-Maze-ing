from mazegen import Maze, Cell
from ._color import Color


class Frame:
    """
    Utility class to render a maze in the terminal using ASCII and ANSI colors.

    This class provides static methods to draw a maze, clear the screen,
    and handle the visual rendering of cells, walls, paths, and cursors.
    All methods are static since no instance state is required.
    """
    @staticmethod
    def draw(
            maze: Maze,
            visited: set[Cell] = set(),
            path_cell: set[Cell] = set(),
            cursors: list[Cell] = []
    ) -> None:
        """
        Draw the given maze in the terminal.

        The maze is rendered with walls, visited cells, path cells,
        entry/exit markers, and optional cursors.

        Args:
            maze (Maze): The maze to render.
            visited (set[Cell], optional): Cells that have been visited.
            Defaults to empty set.
            path_cell (set[Cell], optional): Cells that are part of the path.
            Defaults to empty set.
            cursors (list[Cell], optional): Cells representing cursors or
            highlights. Defaults to empty list.
        """
        print("\033[H", end="")
        for row in maze.map:
            if not row[0].above_cell:
                Frame._render_ceiling(row)
            Frame._verti(
                row,
                visited,
                path_cell,
                cursors,
                (maze.entry, maze.exit)
            )
            Frame._horizontal(row, path_cell)

    @staticmethod
    def clear() -> None:
        """
        Clear the terminal screen.
        """
        print("\033[2J", end="")

    @staticmethod
    def _verti(
        row: list[Cell],
        visited: set[Cell],
        path_cell: set[Cell],
        cursors: list[Cell],
        entry_exit: tuple[Cell, Cell]
    ) -> None:
        Frame._print("║")
        for cell in row:
            if not cell.is_protected:
                if cell in cursors:
                    Frame._print(Color.GREEN_BG, "--")
                elif cell == entry_exit[0]:
                    Frame._print(Color.RED_BG, Color.WHITE, "EN")
                elif cell == entry_exit[1]:
                    Frame._print(Color.WHITE_BG, Color.BLACK, "EX")
                elif cell in path_cell:
                    Frame._print(Color.new_cell_bg, "  ")
                elif visited:
                    Frame._print(
                        Color.new_cell_bg if cell not in visited else "",
                        "  "
                    )
                else:
                    Frame._print(" " * 2)
            else:
                Frame._print(Color.protected_cell, " " * 2)
            if not cell.east.is_closed and cell in path_cell:
                Frame._print(
                    Color.new_cell_bg if cell.right_cell in path_cell else "",
                    " "
                )
            else:
                Frame._print("║" if cell.east.is_closed else " ")

        print()

    @staticmethod
    def _horizontal(row: list[Cell], path_cell: set[Cell]) -> None:
        if not row[0].left_cell:
            if row[0].below_cell:
                Frame._print("╠" if row[0].south.is_closed else "║")
            else:
                Frame._print("╚")

        for cell in row:
            if not cell.south.is_closed and cell in path_cell:
                Frame._print(
                    Color.new_cell_bg if cell.below_cell in path_cell else "",
                    " " * 2
                )
            else:
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
    def _print(*args: str, end: str = Color.DEFAULT) -> None:
        print(Color.bg, Color.wall, *args, end=end, sep="")
