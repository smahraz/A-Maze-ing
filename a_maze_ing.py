from parser import Parser
from sys import argv
from mazegen import MazeGenerator
from ui import Gui, Tui

if __name__ == "__main__":
    if len(argv) != 2:
        print(f"Usage: puthon3 {argv[0]} <config_file>")
        exit(1)
    try:
        config_file = argv[1]
        options = Parser.get_options(config_file)
    except Exception as e:
        print("Error:", e)
        exit(1)
    print(options)
    maze_gen = MazeGenerator(
        options.width, options.height, options.algorithm, options.seed,
        (options.entry.x, options.entry.y), (options.exit.x, options.exit.y)
    )
    match options.interface:
        case "gui":
            Gui(maze_gen).run()
        case "tui":
            Tui(maze_gen).run()
