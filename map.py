from typing import Callable


class _Wall:
    id = 0

    def __init__(self) -> None:
        self.id = self.__class__.id
        self.is_closed = True
        self.new_id()

    def __str__(self) -> str:
        return str(self.id)

    def open(self) -> None:
        self.is_closed = False

    @classmethod
    def new_id(cls) -> None:
        cls.id += 1


class _Cell:
    def __init__(self) -> None:
        self.west = _Wall()
        self.east = _Wall()
        self.north = _Wall()
        self.south = _Wall()

    def __str__(self) -> str:
        return (
            "Cell ("
            f"w: {self.west}, "
            f"e: {self.east}, "
            f"n: {self.north}, "
            f"s: {self.south})"
        )

    def __repr__(self) -> str:
        return self.__str__()

    def right_cell(self, other: "_Cell") -> None:
        self.east = other.west

    def bottom_cell(self, other: "_Cell") -> None:
        self.south = other.north


class Map:
    def __init__(self, width: int, height: int) -> None:
        cls_nm = self.__class__.__name__
        assert isinstance(height, int), f"{cls_nm}.height isn't an int"
        assert isinstance(width, int), f"{cls_nm}.width isn't an int"
        assert height > 0 and width > 0, "width,height must be greater than 0"

        self.height = height
        self.width = width

        self.map = [[_Cell() for _ in range(width)] for _ in range(height)]
        self._set_walls()

    def open_north(self, column: int, row: int) -> None:
        self.map[row][column].north.open()

    def open_south(self, column: int, row: int) -> None:
        self.map[row][column].south.open()

    def open_west(self, column: int, row: int) -> None:
        self.map[row][column].west.open()

    def open_east(self, column: int, row: int) -> None:
        self.map[row][column].east.open()

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
            set_walls(row, lambda prev, cell: prev.right_cell(cell))

        for column in range(self.width):
            set_walls(
                column_to_list(column),
                lambda prev, cell: prev.bottom_cell(cell)
            )

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
        return output_


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
