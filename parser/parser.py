from random import randint
from typing import TypeVar, Type

pos = TypeVar("pos", bound="Pos")


class ParseError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


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
    def __init__(self) -> None:
        self.width: int
        self.height: int
        self.entry: Pos
        self.exit: Pos
        self.output_file: str
        self.perfect: bool
        self.seed: int = randint(0, 999_999_999)
        self.algorithm: str = "DFS"
        self.interface: str = "gui"

    def __str__(self) -> str:
        return str(self.__dict__)

    def check(self) -> None:
        if self.width is None:
            raise ParseError("Missing mandatory key: WIDTH")
        if self.height is None:
            raise ParseError("Missing mandatory key: HEIGHT")
        if self.entry is None:
            raise ParseError("Missing mandatory key: ENTRY")
        if self.exit is None:
            raise ParseError("Missing mandatory key: EXIT")
        if self.output_file is None:
            raise ParseError("Missing mandatory key: OUTPUT_FILE")
        if self.perfect is None:
            raise ParseError("Missing mandatory key: PERFECT")
        if self.width < 0:
            raise ValueError("Invalid WIDTH")
        if self.height < 0:
            raise ValueError("Invalid HEIGHT")
        if self.entry.x >= self.width or self.entry.y >= self.height\
                or self.entry.x < 0 or self.entry.y < 0:
            raise ValueError("Invalid ENTRY coordinates")
        if self.exit.x >= self.width or self.exit.y >= self.height\
                or self.exit.x < 0 or self.exit.y < 0:
            raise ValueError("Invalid EXIT coordinates")

    def add_option(self, key: str, value: str) -> None:
        value = value.strip()
        match key.lower().strip():
            case "width":
                try:
                    width = int(value)
                except ValueError:
                    raise ValueError("Width must be an int value")
                self.width = width
            case "height":
                try:
                    height = int(value)
                except ValueError:
                    raise ValueError("Height must be an int value")
                self.height = height
            case "entry":
                try:
                    entry = Pos.from_string(value)
                except ValueError:
                    raise ValueError("Entry must be a Pos value (ex: x,y)")
                self.entry = entry
            case "exit":
                try:
                    exit = Pos.from_string(value)
                except ValueError:
                    raise ValueError("Exit must be a Pos value (ex: x,y)")
                self.exit = exit
            case "output_file":
                self.output_file = value
            case "perfect":
                if value == 'True':
                    self.perfect = True
                elif value == 'False':
                    self.perfect = False
                else:
                    raise ValueError("Perfect must be a True or False")
            case "seed":
                try:
                    seed = int(value)
                except ValueError:
                    raise ValueError("Seed must be an int value")
                self.seed = seed
            case "algorithm":
                if value not in ['DFS', 'PRIM']:
                    raise ValueError("Algorithm must be DFS or PRIM")
                self.algorithm = value
            case "interface":
                if value not in ['gui', 'tui']:
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
            if not line or line[0] == '#':
                continue
            try:
                op = line.index('=')
            except ValueError:
                raise ParseError(f"invalid configuration line: {line}")
            options.add_option(line[:op], line[op + 1:])
        options.check()
        return options
