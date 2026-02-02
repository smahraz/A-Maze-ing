from random import randint
from typing import TypeVar, Type

pos = TypeVar("pos", bound="Pos")


class ParseError(Exception):
    pass


class Pos:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({self.x},{self.y})"

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def from_string(cls: Type[pos], s: str) -> pos:
        x, y = s.split(",")
        return cls(int(x), int(y))


class Options:

    width: int
    height: int
    entry: Pos
    exit: Pos
    output_file: str
    perfect: bool

    def __init__(self) -> None:
        self.seed: int = randint(0, 999_999_999)
        self.algorithm: str = "DFS"
        self.interface: str = "gui"

    def __str__(self) -> str:
        return str(self.__dict__)

    def check(self) -> None:
        try:
            self.width
            self.height
            self.entry
            self.exit
            self.output_file
            self.perfect
        except AttributeError:
            raise ParseError("Missing mandatory key: check config file")
        if self.width < 9:
            raise ValueError("Invalid Width (Width > 8)")
        if self.height < 7:
            raise ValueError("Invalid Height (Height > 6)")
        if self.entry.x >= self.width or self.entry.y >= self.height\
                or self.entry.x < 0 or self.entry.y < 0:
            raise ValueError("Invalid Entry coordinates")
        if self.exit.x >= self.width or self.exit.y >= self.height\
                or self.exit.x < 0 or self.exit.y < 0:
            raise ValueError("Invalid Exit coordinates")
        if self.entry.x == self.exit.x and self.entry.y == self.exit.y:
            raise ValueError("Entry and Exit can't be on the same cell")

    def add_option(self, key: str, value: str) -> None:
        value = value.strip()
        key = key.lower().strip()
        match key:
            case "width" | "height" | "seed":
                try:
                    int_value = int(value)
                except ValueError:
                    raise ValueError(
                        f"{key.capitalize()} must be an int value"
                    )
                if key == "width":
                    self.width = int_value
                elif key == "height":
                    self.height = int_value
                else:
                    self.seed = int_value
            case "entry" | "exit":
                try:
                    tpl = Pos.from_string(value)
                except ValueError:
                    raise ValueError("Entry must be a Pos value (ex: x,y) int")
                if key == "entry":
                    self.entry = tpl
                else:
                    self.exit = tpl
            case "output_file":
                self.output_file = value
            case "perfect":
                if value in {'True', 'False'}:
                    self.perfect = True if value == 'True' else False
                else:
                    raise ValueError("Perfect must be a True or False")
            case "algorithm":
                if value not in {'DFS', 'PRIM'}:
                    raise ValueError("Algorithm must be DFS or PRIM")
                self.algorithm = value
            case "interface":
                if value not in {'gui', 'tui'}:
                    raise ValueError("Interface must be gui or tui")
                self.interface = value


class Parser:
    @staticmethod
    def _get_lines(file_path: str) -> list[str]:
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
        except Exception:
            raise ParseError(
                f"can't access config file {file_path}")
        return [line.strip() for line in lines]

    @staticmethod
    def get_options(file_path: str) -> Options:
        options = Options()
        lines = Parser._get_lines(file_path)
        for line in lines:
            if not line or line.lstrip().startswith('#'):
                continue
            try:
                op = line.index('=')
            except ValueError:
                raise ParseError(f"invalid configuration line: {line}")
            options.add_option(line[:op], line[op + 1:])
        options.check()
        return options
