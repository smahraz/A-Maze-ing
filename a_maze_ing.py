from parser import Parser
from sys import argv
from map import Map
from gui import Gui

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
    map = Map(options.width, options.height)
    match options.interface:
        case "gui":
            gui = Gui(map)
            gui.display()
        case "tui":
            pass
