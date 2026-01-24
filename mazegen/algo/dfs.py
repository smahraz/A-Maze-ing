from mazegen import Maze, Cell, Step
from random import Random


def _is_deadend(cell: Cell, visited: set[Cell]) -> bool:
    def check_cell(cell: Cell | None) -> bool:
        return cell is None or\
            cell in visited or\
            cell.is_protected
    return check_cell(cell.above_cell) and check_cell(cell.below_cell) and\
        check_cell(cell.right_cell) and check_cell(cell.left_cell)


def _open_wall(cell: Cell, visited: set[Cell], wall: int) -> Cell | None:
    walls = (
        (cell.above_cell, cell.north),
        (cell.right_cell, cell.east),
        (cell.below_cell, cell.south),
        (cell.left_cell, cell.west)
    )

    def _try(wall_int: int) -> Cell | None:
        next_cell, wall = walls[wall_int]
        if next_cell is None or\
                next_cell.is_protected or next_cell in visited:
            return None
        wall.open()
        return next_cell
    return _try(wall)


def DFS(map: Maze, save_step: bool, rng: Random) -> tuple[Maze, list[Step]]:
    stack: list[Cell] = []
    visited = set()
    steps = []

    stack.append(map.map[0][0])
    visited.add(stack[0])
    while stack:
        if _is_deadend(stack[-1], visited):
            stack.pop()
        else:
            cell = _open_wall(stack[-1], visited, rng.randint(0, 3))
            if cell:
                stack.append(cell)
                visited.add(cell)
    return map, steps
