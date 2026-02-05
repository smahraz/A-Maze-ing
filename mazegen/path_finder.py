from mazegen import Maze, Cell
from typing import Optional


class PathCell:
    """
    Wrapper for a cell used in pathfinding.

    This class associates a maze cell with its parent in the
    search tree, allowing the path to be reconstructed once
    the exit is found.

    Attributes:
        cell (Cell): The wrapped maze cell.
        parent (PathCell | None): The parent cell in the search path.
    """

    def __init__(self, cell: Cell, parent: Optional["PathCell"] = None):
        """
        Initialize a PathCell.

        Args:
            cell (Cell): The maze cell to wrap.
            parent (PathCell, optional): The parent cell in the path.
                Defaults to None.
        """
        self.cell = cell
        self.parent = parent


def _get_neighbours(cell: PathCell, visited: set[Cell]) -> list[PathCell]:
    """
    Get all unvisited reachable neighbours of a cell.

    This function examines the four cardinal directions and returns
    PathCell wrappers for neighbours that can be reached (wall is open)
    and have not yet been visited.

    Args:
        cell (PathCell): The current cell to find neighbours for.
        visited (set[Cell]): Set of already visited cells.

    Returns:
        list[PathCell]: List of reachable, unvisited neighbour cells.
    """
    neighbours: list[PathCell] = []
    if not cell.cell.north.is_closed:
        if cell.cell.above_cell and cell.cell.above_cell not in visited:
            neighbours.append(PathCell(cell.cell.above_cell, cell))
    if not cell.cell.south.is_closed:
        if cell.cell.below_cell and cell.cell.below_cell not in visited:
            neighbours.append(PathCell(cell.cell.below_cell, cell))
    if not cell.cell.east.is_closed:
        if cell.cell.right_cell and cell.cell.right_cell not in visited:
            neighbours.append(PathCell(cell.cell.right_cell, cell))
    if not cell.cell.west.is_closed:
        if cell.cell.left_cell and cell.cell.left_cell not in visited:
            neighbours.append(PathCell(cell.cell.left_cell, cell))
    return neighbours


def _get_path(cell: PathCell) -> list[tuple[Cell, str]]:
    """
    Reconstruct the path from the exit back to the entry.

    This function traces back through parent references to build
    the path, recording the direction taken at each step.

    Args:
        cell (PathCell): The exit cell from which to trace back.

    Returns:
        list[tuple[Cell, str]]: A list of tuples containing each cell
        and the direction taken from that cell.
    """
    path: list[tuple[Cell, str]] = []

    while cell.parent:
        if cell.parent.cell == cell.cell.above_cell:
            direction = 'S'
        elif cell.parent.cell == cell.cell.below_cell:
            direction = 'N'
        elif cell.parent.cell == cell.cell.right_cell:
            direction = 'W'
        elif cell.parent.cell == cell.cell.left_cell:
            direction = 'E'
        else:
            direction = '?'
        path.append((cell.parent.cell, direction))
        cell = cell.parent
    path.reverse()
    return path


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
    entry = PathCell(maze.entry)
    exit_cell = maze.exit

    frontier: list[PathCell] = []
    visited: set[Cell] = set()

    visited.add(entry.cell)
    frontier.append(entry)

    while frontier:
        current = frontier.pop(0)
        if current.cell == exit_cell:
            break
        for neighbour in _get_neighbours(current, visited):
            visited.add(neighbour.cell)
            frontier.append(neighbour)

    if current and current.cell == exit_cell:
        return _get_path(current)
    else:
        return []
