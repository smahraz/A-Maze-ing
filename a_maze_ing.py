from parser import Parser
from sys import argv
from mazegen import MazeGenerator, MazeError
from ui import Gui, Tui


def write_output(output: str) -> None:
    try:
        with open(output_path, 'w') as file:
            file.write(output)
    except OSError as e:
        print(f"Error: '{output_path}' {e.strerror}")
        exit(1)


if __name__ == "__main__":
    if len(argv) != 2:
        print(f"Usage: puthon3 {argv[0]} <config_file>")
        exit(1)
    try:
        config_file = argv[1]
        options = Parser.get_options(config_file)
        maze_gen = MazeGenerator(
            options.width,
            options.height,
            options.algorithm,
            options.perfect,
            options.seed,
            (options.entry.x, options.entry.y),
            (options.exit.x, options.exit.y)
        )
    except Exception as e:
        print("Error:", e)
        exit(1)
    output_path = options.output_file
    try:
        match options.interface:
            case "gui":
                Gui(maze_gen, write_output).run()
            case "tui":
                Tui(maze_gen, write_output).run()

    except MazeError as e:
        print("Error:", e)
