class ParseError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x},{self.y})"

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_string(cls, s: str):
        x, y = s.split(",")
        return cls(int(x), int(y))


class Options:
    def __init__(self):
        self.width = None
        self.height = None
        self.entry = None
        self.exit = None
        self.output_file = None
        self.perfect = None

    def __str__(self):
        return str(self.__dict__)

    def check(self):
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

    def add_option(self, key: str, value):
        match key:
            case "WIDTH":
                try:
                    value = int(value)
                except ValueError:
                    raise ValueError("WIDTH must be an int value")
                self.width = value
            case "HEIGHT":
                try:
                    value = int(value)
                except ValueError:
                    raise ValueError("HEIGHT must be an int value")
                self.height = value
            case "ENTRY":
                try:
                    value = Pos.from_string(value)
                except ValueError:
                    raise ValueError("ENTRY must be a Pos value (ex: x,y)")
                self.entry = value
            case "EXIT":
                try:
                    value = Pos.from_string(value)
                except ValueError:
                    raise ValueError("EXIT must be a Pos value (ex: x,y)")
                self.exit = value
            case "OUTPUT_FILE":
                self.output_file = value
            case "PERFECT":
                if value == 'True':
                    self.perfect = True
                elif value == 'False':
                    self.perfect = False
                else:
                    raise ValueError("PERFECT must be a True or False")
            case "SEED":
                try:
                    value = int(value)
                except ValueError:
                    raise ValueError("SEED must be an int value")
                self.seed = value
            case "ALGORITHM":
                if value not in ['DFS', 'BFS']:
                    raise ValueError("ALGORITHM must be DFS or BFS")
                self.algorithm = value
            case "INTERFACE":
                if value not in ['gui', 'tui']:
                    raise ValueError("INTERFACE must be gui or tui")
                self.interface = value


class Parser:
    @staticmethod
    def _get_lines(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        return [line[:-1] for line in lines]

    @staticmethod
    def get_options(file_path):
        options = Options()
        lines = Parser._get_lines(file_path)
        for line in lines:
            if not line or line[0] == '#':
                continue
            op = line.index('=')
            options.add_option(line[:op], line[op + 1:])
        options.check()
        return options


if __name__ == "__main__":
    options = Parser.get_options("default_config.txt")
    print(options)
