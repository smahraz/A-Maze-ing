from typing import Callable, Generator


class _Wall:
    id = 0

    def __init__(self) -> None:
        self.id = self.__class__.id
        self.is_closed = True
        self.new_id()
        self.is_protected: bool = False

    def __str__(self) -> str:
        return str(self.id)

    def open(self) -> None:
        self.is_closed = False

    @classmethod
    def new_id(cls) -> None:
        cls.id += 1


class _Cell:
    def __init__(self, x: int, y: int) -> None:
        self.west = _Wall()
        self.east = _Wall()
        self.north = _Wall()
        self.south = _Wall()

        self.x = x
        self.y = y

        self.above_cell: _Cell | None = None
        self.below_cell: _Cell | None = None
        self.left_cell: _Cell | None = None
        self.right_cell: _Cell | None = None

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

    def next_in_row(self, other: "_Cell") -> None:
        self.east = other.west
        self.right_cell = other
        other.left_cell = self

    def next_in_column(self, other: "_Cell") -> None:
        self.south = other.north
        self.below_cell = other
        other.above_cell = self

    def protect(self) -> None:
        self.west.is_protected = True
        self.south.is_protected = True
        self.north.is_protected = True
        self.east.is_protected = True
        self.is_protected = True


class Map:
    def __init__(self, width: int, height: int) -> None:
        cls_nm = self.__class__.__name__
        assert isinstance(height, int), f"{cls_nm}.height isn't an int"
        assert isinstance(width, int), f"{cls_nm}.width isn't an int"
        assert height > 0 and width > 0, "width,height must be greater than 0"

        self.height = height
        self.width = width

        self.map = [[_Cell(x, y) for x in range(width)] for y in range(height)]
        self._set_walls()

    def _set_walls(self) -> None:
        def column_to_list(column: int) -> list[_Cell]:
            return [row[column] for row in self.map]

        def set_walls(cells: list[_Cell], apply_func: Callable) -> None:
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
        assert not self.map[y][x].north.is_protected, "the wall is protected"
        self.map[y][x].north.open()

    def open_south(self, x: int, y: int) -> None:
        assert not self.map[y][x].south.is_protected, "the wall is protected"
        self.map[y][x].south.open()

    def open_west(self, x: int, y: int) -> None:
        assert not self.map[y][x].west.is_protected, "the wall is protected"
        self.map[y][x].west.open()

    def open_east(self, x: int, y: int) -> None:
        assert not self.map[y][x].east.is_protected, "the wall is protected"
        self.map[y][x].east.open()

    def encode(self) -> str:
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

    def cell_iterator(self) -> Generator[_Cell, None, None]:
        for row in self.map:
            for cell in row:
                yield cell


if __name__ == "__main__":
    # for row in Map(5, 2).map:
    #    print(row)
    m = Map(30, 20)
    m.open_north(10, 10)
    m.open_east(10, 10)
    m.open_south(10, 10)
    m.open_west(10, 10)
    m.open_south(29, 19)
    m.open_south(0, 0)
    m.open_east(0, 0)

    print(m.encode())
