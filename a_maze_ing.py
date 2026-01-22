from parser import Parser
from map import Map
from gui import Gui

if __name__ == "__main__":
    try:
        options = Parser.get_options("default_config.txt")
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
