class ParseError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


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

    def add_option(self, key: str, value):
        match key:
            case "WIDTH":
                self.width = value
            case "HEIGHT":
                self.height = value
            case "ENTRY":
                self.entry = value
            case "EXIT":
                self.exit = value
            case "OUTPUT_FILE":
                self.output_file = value
            case "PERFECT":
                self.perfect = value
            case "SEED":
                self.seed = value
            case "ALGORITHM":
                self.algorithm = value
            case "INTERFACE":
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
