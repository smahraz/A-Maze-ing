from map import Map, _Cell


class Frame:

    @staticmethod
    def display(map: Map) -> None:
        print("\033[H", end="")
        for i, row in enumerate(map.map):
            if i == 0:
                Frame._border(len(row))
            Frame._vertical(row)
            Frame._horizontal(row)

    @staticmethod
    def clear() -> None:
        print("\033[2J", end="")

    @staticmethod
    def _vertical(row: list[_Cell]):
        print("║", end="")
        for cell in row:
            print("  ", end="")
            print("║" if cell.east.is_closed else " ", end="")
        print()

    @staticmethod
    def _horizontal(row: list[_Cell]):
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


if __name__ == "__main__":
    from time import sleep
    from random import randint, choice
    m = Map(40, 20)
    Frame.clear()
    for i in range(1000):
        f = choice([m.open_east, m.open_north, m.open_south, m.open_west])
        f(randint(0, 39), randint(0, 19))
        Frame.display(m)
        sleep(0.007)
