from typing import Callable, Generator


class MazeError(Exception):
    """
    Just a custom error i can specificlly Catch.
    """
    pass


class _Wall:
    """
    Represent a single wall, shared between two linked cells.

    Can be opened, and protected.

    Methods:
        open(): Open a closed wall.
    """
    id = 0

    def __init__(self) -> None:
        self.id = self.__class__.id
        self.is_closed = True
        self._new_id()
        self.is_protected: bool = False

    def __str__(self) -> str:
        return str(self.id)

    def open(self) -> None:
        self.is_closed = False

    @classmethod
    def _new_id(cls) -> None:
        cls.id += 1


class Cell:
    """
    Represent a single cell in a Maze.

    A cell is identified by its x and y coordinates and can be linked
    to neighboring cells horizontally or vertically.

    Attributes:
        x (int): The x coordinate of the cell.
        y (int): The y coordinate of the cell.

    Methods:
        next_in_row(): Return or link to the neighboring cell in the same row.
        next_in_column(): Return or link to the neighboring cell in the same
            column.
    """
    def __init__(self, x: int, y: int) -> None:
        self.west = _Wall()
        self.east = _Wall()
        self.north = _Wall()
        self.south = _Wall()

        self.x = x
        self.y = y

        self.above_cell: Cell | None = None
        self.below_cell: Cell | None = None
        self.left_cell: Cell | None = None
        self.right_cell: Cell | None = None

        self.is_protected: bool = False

    def __str__(self) -> str:
        return (
            "Cell ("
            f"w: {self.west} {'P' if self.west.is_protected else ''}, "
            f"e: {self.east} {'P' if self.east.is_protected else ''}, "
            f"n: {self.north} {'P' if self.north.is_protected else ''}, "
            f"s: {self.south} {'P' if self.south.is_protected else ''})"
        )

    def __repr__(self) -> str:
        return self.__str__()

    def next_in_row(self, other: "Cell") -> None:
        """
        Link this cell to a neighboring cell in the same row.

        This method connects the current cell with the given cell
        horizontally, setting the appropriate east/west.

        Args:
            other (Cell): The neighboring cell to link with.
        """
        self.east = other.west
        self.right_cell = other
        other.left_cell = self

    def next_in_column(self, other: "Cell") -> None:
        """
        Link this cell to a neighboring cell in the same column.

        This method connects the current cell with the given cell
        vertically, setting the appropriate north/south.

        Args:
            other (Cell): The neighboring cell to link with.
        """
        self.south = other.north
        self.below_cell = other
        other.above_cell = self

    def protect(self) -> None:
        """
        Protect a Cell and its wall, preventing opening a wall by mistake.
        """
        self.west.is_protected = True
        self.south.is_protected = True
        self.north.is_protected = True
        self.east.is_protected = True
        self.is_protected = True


class Maze:
    """
    Represent a rectangular maze composed of interconnected cells.

    The maze is stored as a two-dimensional grid of cells. Each cell
    has four walls (north, east, south, and west) that can be opened
    or closed to create paths. The maze supports iteration over all
    cells, wall manipulation, and encoding to a compact string form.
    """
    entry: Cell
    exit: Cell

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int]
    ) -> None:
        cls_nm = self.__class__.__name__
        assert isinstance(height, int), f"{cls_nm}.height isn't an int"
        assert isinstance(width, int), f"{cls_nm}.width isn't an int"
        assert height > 0 and width > 0, "width,height must be greater than 0"

        self.height = height
        self.width = width

        self.map = [[Cell(x, y) for x in range(width)] for y in range(height)]
        self._set_walls()
        self._rander_42()
        self._set_entry_exit(entry, exit)

    def _set_walls(self) -> None:
        def column_to_list(column: int) -> list[Cell]:
            return [row[column] for row in self.map]

        def set_walls(
                cells: list[Cell],
                apply_func: Callable[[Cell, Cell], None]
        ) -> None:
            prev = None
            for cell in cells:
                if not prev:
                    prev = cell
                    continue
                apply_func(prev, cell)
                prev = cell

        for row in self.map:
            set_walls(row, lambda prev, cell: prev.next_in_row(cell))

        for column in range(self.width):
            set_walls(
                column_to_list(column),
                lambda prev, cell: prev.next_in_column(cell)
            )

    def open_north(self, x: int, y: int) -> None:
        """Open the north wall of the cell at (x, y)."""
        assert not self.map[y][x].north.is_protected, "the wall is protected"
        self.map[y][x].north.open()

    def open_south(self, x: int, y: int) -> None:
        """Open the south wall of the cell at (x, y)."""
        assert not self.map[y][x].south.is_protected, "the wall is protected"
        self.map[y][x].south.open()

    def open_west(self, x: int, y: int) -> None:
        """Open the west wall of the cell at (x, y)."""
        assert not self.map[y][x].west.is_protected, "the wall is protected"
        self.map[y][x].west.open()

    def open_east(self, x: int, y: int) -> None:
        """Open the east wall of the cell at (x, y)."""
        assert not self.map[y][x].east.is_protected, "the wall is protected"
        self.map[y][x].east.open()

    def encode(self) -> str:
        """
        Encode the maze layout as a hexadecimal string.

        Each cell is encoded as a single hexadecimal digit derived from
        the open or closed state of its four walls. The bits are assigned
        in the following order: north (bit 0), east (bit 1), south (bit 2),
        and west (bit 3). Rows are separated by newline characters.

        Returns:
            str: A newline-separated hexadecimal representation of the maze.
        """
        output_ = ""
        for row in self.map:
            for cell in row:
                nibble = 0
                nibble |= cell.north.is_closed
                nibble |= cell.east.is_closed << 1
                nibble |= cell.south.is_closed << 2
                nibble |= cell.west.is_closed << 3
                output_ += hex(nibble)[2:]
            output_ += "\n"
        return output_[:-1]

    def protect_cell(self, x: int, y: int) -> None:
        self.map[y][x].protect()

    def cell_iterator(self) -> Generator[Cell, None, None]:
        """
        Yield all cells in the map.

        This iterator walks through the map row by row and yields
        each cell in turn.

        Yields:
            Cell: The next cell in the map.
        """
        for row in self.map:
            for cell in row:
                yield cell

    def apply_step(self, x: int, y: int, wall: str | None) -> "Maze":
        """
        Apply a step to the maze by opening a wall at the given position.

        Depending on the value of ``wall``, this method opens the
        corresponding wall (west, east, north, or south) of the cell
        at coordinates ``(x, y)``.

        Args:
            x (int): The x coordinate of the cell.
            y (int): The y coordinate of the cell.
            wall (str | None): The wall to open. Valid values are
                ``'W'``, ``'E'``, ``'N'``, ``'S'``, or ``None``.

        Returns:
            Maze: The maze instance, allowing method chaining.
        """
        match wall:
            case 'W':
                self.open_west(x, y)
            case 'E':
                self.open_east(x, y)
            case 'N':
                self.open_north(x, y)
            case 'S':
                self.open_south(x, y)
        return self

    def _rander_42(self) -> None:
        if self.height < 7 or self.width < 9:
            return

        middle_y = self.height // 2
        middle_x = self.width // 2

        self.protect_cell(middle_x - 1, middle_y)
        self.protect_cell(middle_x - 2, middle_y)
        self.protect_cell(middle_x - 3, middle_y)

        self.protect_cell(middle_x - 3, middle_y - 1)
        self.protect_cell(middle_x - 3, middle_y - 2)

        self.protect_cell(middle_x - 1, middle_y + 1)
        self.protect_cell(middle_x - 1, middle_y + 2)

        self.protect_cell(middle_x + 1, middle_y)
        self.protect_cell(middle_x + 2, middle_y)
        self.protect_cell(middle_x + 3, middle_y)

        self.protect_cell(middle_x + 1, middle_y + 1)
        self.protect_cell(middle_x + 1, middle_y + 2)

        self.protect_cell(middle_x + 2, middle_y + 2)
        self.protect_cell(middle_x + 3, middle_y + 2)

        self.protect_cell(middle_x + 3, middle_y - 1)
        self.protect_cell(middle_x + 3, middle_y - 2)

        self.protect_cell(middle_x + 2, middle_y - 2)
        self.protect_cell(middle_x + 1, middle_y - 2)

    def _set_entry_exit(
        self,
        entry: tuple[int, int],
        exit: tuple[int, int]
    ) -> None:
        if self.map[entry[1]][entry[0]].is_protected:
            raise MazeError("Invalid entry (inside pattern)")
        if self.map[exit[1]][exit[0]].is_protected:
            raise MazeError("Invalid exit (inside pattern)")
        else:
            self.entry = self.map[entry[1]][entry[0]]
            self.exit = self.map[exit[1]][exit[0]]
