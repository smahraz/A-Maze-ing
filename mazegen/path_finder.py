from queue import Queue
from mazegen import Maze, Cell


def _get_neighbours(cell: Cell, visited: set[Cell]) -> list[Cell]:
    neighbour = []

    if (
        cell.right_cell
        and not cell.right_cell.is_protected
        and cell.right_cell not in visited
        and not cell.east.is_closed
    ):
        neighbour.append(cell.right_cell)
    if (
        cell.left_cell
        and not cell.left_cell.is_protected
        and cell.left_cell not in visited
        and not cell.west.is_closed
    ):
        neighbour.append(cell.left_cell)
    if (
        cell.above_cell
        and not cell.above_cell.is_protected
        and cell.above_cell not in visited
        and not cell.north.is_closed
    ):
        neighbour.append(cell.above_cell)
    if (
        cell.below_cell
        and not cell.below_cell.is_protected
        and cell.below_cell not in visited
        and not cell.south.is_closed
    ):
        neighbour.append(cell.below_cell)

    return neighbour


def path_finder(maze: Maze) -> list[tuple[Cell, str]]:
    """
    Find a path through the maze from entry to exit.

    This function uses a breadth-first search algorithm to find
    a path from the maze entry to the exit. It returns the path
    as a list of cells with their corresponding movement directions.

    Args:
        maze (Maze): The maze to find a path through.

    Returns:
        list[tuple[Cell, str]]: A list of tuples where each tuple
        contains a cell and the direction taken from that cell.
        Returns an empty list if no path exists.
    """
    parent_tree: dict[Cell, Cell] = {}
    visited = set()
    to_visit: Queue = Queue()
    to_visit.put(maze.entry)

    while True:
        current = to_visit.get()
        visited.add(current)
        if current == maze.exit:
            break
        neighbours = _get_neighbours(current, visited)
        for cl in neighbours:
            to_visit.put(cl)
            parent_tree[cl] = current
        # can't find path
        if to_visit.empty():
            return []

    # go back by parents
    cl = current
    path = []
    while cl in parent_tree:
        path.append(cl)
        cl = parent_tree[cl]
    path.append(maze.entry)

    last_index = len(path) - 1
    path = path[::-1]
    for i, cell in enumerate(path):
        if i == last_index:
            continue
        if cell.right_cell == path[i + 1]:
            path[i] = (cell, "E")
        elif cell.left_cell == path[i + 1]:
            path[i] = (cell, "W")
        elif cell.above_cell == path[i + 1]:
            path[i] = (cell, "N")
        else:
            path[i] = (cell, "S")
    return path[:-1]
