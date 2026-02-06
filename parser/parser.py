from random import randint
from typing import TypeVar, Type

pos = TypeVar("pos", bound="Pos")


class ParseError(Exception):
    """
    Exception raised for configuration file parsing errors.

    This exception is raised when the configuration file cannot
    be accessed or contains invalid syntax.
    """
    pass


class Pos:
    """
    Represent a 2D position with x and y coordinates.

    This class is used to store entry and exit coordinates
    for maze configuration.

    Attributes:
        x (int): The x coordinate.
        y (int): The y coordinate.
    """

    def __init__(self, x: int, y: int):
        """
        Initialize a new position.

        Args:
            x (int): The x coordinate.
            y (int): The y coordinate.
        """
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({self.x},{self.y})"

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def from_string(cls: Type[pos], s: str) -> pos:
        """
        Create a Pos instance from a comma-separated string.

        Args:
            s (str): A string in the format "x,y".

        Returns:
            Pos: A new Pos instance with the parsed coordinates.

        Raises:
            ValueError: If the string is not in the correct format.
        """
        x, y = s.split(",")
        return cls(int(x), int(y))


class Options:
    """
    Store configuration options for maze generation.

    This class holds all the settings parsed from a configuration
    file, including maze dimensions, entry/exit positions, algorithm
    choice, and output settings.

    Attributes:
        width (int): The width of the maze in cells.
        height (int): The height of the maze in cells.
        entry (Pos): The entry position.
        exit (Pos): The exit position.
        output_file (str): Path to the output file.
        perfect (bool): Whether to generate a perfect maze.
        seed (int): Random seed for generation.
        algorithm (str): Algorithm to use ("DFS" or "PRIM").
        interface (str): Interface type ("gui" or "tui").
    """

    width: int
    height: int
    entry: Pos
    exit: Pos
    output_file: str
    perfect: bool

    def __init__(self) -> None:
        """
        Initialize Options with default values.

        The seed is randomly generated, and the default algorithm
        is "DFS" with "gui" interface.
        """
        self.seed: int = randint(0, 999_999_999)
        self.algorithm: str = "DFS"
        self.interface: str = "gui"

    def __str__(self) -> str:
        return str(self.__dict__)

    def check(self) -> None:
        """
        Validate all required options are set and have valid values.

        Raises:
            ParseError: If any mandatory option is missing.
            ValueError: If any option has an invalid value.
        """
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
        """
        Parse and add a configuration option.

        This method parses the key-value pair from the configuration
        file and sets the corresponding attribute.

        Args:
            key (str): The option name.
            value (str): The option value as a string.

        Raises:
            ValueError: If the value is not valid for the given key.
        """
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
            case _:
                raise ValueError(f"Unknown key: {key}")


class Parser:
    """
    Parse configuration files for maze generation.

    This class provides static methods to read and parse
    configuration files containing maze generation options.
    """

    @staticmethod
    def _get_lines(file_path: str) -> list[str]:
        """
        Read all lines from a configuration file.

        Args:
            file_path (str): Path to the configuration file.

        Returns:
            list[str]: List of stripped lines from the file.

        Raises:
            ParseError: If the file cannot be accessed.
        """
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
        except Exception:
            raise ParseError(
                f"can't access config file {file_path}")
        return [line.strip() for line in lines]

    @staticmethod
    def get_options(file_path: str) -> Options:
        """
        Parse a configuration file and return the options.

        This method reads the configuration file, parses each
        key-value pair, and validates the complete options.

        Args:
            file_path (str): Path to the configuration file.

        Returns:
            Options: The parsed and validated configuration options.

        Raises:
            ParseError: If the file cannot be accessed or has invalid syntax.
            ValueError: If any option value is invalid.
        """
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
