from mazegen import Maze, Cell
from typing import Optional


class PathCell:
    def __init__(self, cell: Cell, parent: Optional["PathCell"] = None):
        self.cell = cell
        self.parent = parent


def _get_neighbours(cell: PathCell, visited: set[Cell]) -> list[PathCell]:
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
