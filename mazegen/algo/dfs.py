from mazegen import Maze, Cell, Step
from random import Random


def _is_deadend(cell: Cell, visited: set[Cell]) -> bool:
    def check_cell(cell: Cell | None) -> bool:
        return cell is None or\
            cell in visited or\
            cell.is_protected
    return check_cell(cell.above_cell) and check_cell(cell.below_cell) and\
        check_cell(cell.right_cell) and check_cell(cell.left_cell)


def _open_wall(cell: Cell, visited: set[Cell], wall_int: int)\
        -> tuple[Cell | None, str | None]:
    walls = (
        (cell.above_cell, cell.north),
        (cell.right_cell, cell.east),
        (cell.below_cell, cell.south),
        (cell.left_cell, cell.west)
    )

    next_cell, wall = walls[wall_int]
    if next_cell is None or\
            next_cell.is_protected or\
            next_cell in visited:
        return None, None
    wall.open()
    return next_cell, ["N", "E", "S", "W"][wall_int]


def _open_wall_random(
        cell: Cell,
        should_not_touch: set[Cell | None],
        wall_int: int
) -> tuple[Cell | None, str | None]:
    walls = (
        (cell.above_cell, cell.north),
        (cell.right_cell, cell.east),
        (cell.below_cell, cell.south),
        (cell.left_cell, cell.west)
    )

    next_cell, wall = walls[wall_int]
    if next_cell is None or\
            next_cell.is_protected or\
            cell.is_protected or\
            cell in should_not_touch or\
            not wall.is_closed:
        return None, None
    wall.open()
    return next_cell, ["N", "E", "S", "W"][wall_int]


def _break_random(map: Maze, r: Random) -> list[Step]:
    steps: list[Step] = []
    random_cells = map.height * map.width * 0.06
    should_not_touch: set[Cell | None] = set()
    while len(steps) < random_cells:
        cl = map.map[r.randint(0, map.height - 1)][r.randint(0, map.width - 1)]
        cell, wall = _open_wall_random(cl, should_not_touch, r.randint(0, 3))
        if cell:
            steps.append(Step(cl.x, cl.y, wall))
            should_not_touch.add(cell)
            should_not_touch.add(cell.above_cell)
            should_not_touch.add(cell.below_cell)
            should_not_touch.add(cell.right_cell)
            should_not_touch.add(cell.left_cell)
    return steps


def DFS(
        map: Maze,
        save_step: bool,
        perfect: bool,
        rng: Random,
) -> tuple[Maze, list[Step]]:

    stack: list[Cell] = []
    visited = set()
    steps = []

    stack.append(map.map[map.height//2][map.width//2])
    visited.add(stack[0])
    while stack:
        if _is_deadend(stack[-1], visited):
            if save_step:
                steps.append(Step(
                    stack[-1].x,
                    stack[-1].y,
                    None
                ))
            stack.pop()
        else:
            cell, wall = _open_wall(stack[-1], visited, rng.randint(0, 3))
            if cell:
                if save_step:
                    steps.append(Step(
                        stack[-1].x,
                        stack[-1].y,
                        wall  # {'N', 'E', 'S', 'W', None}
                    ))
                stack.append(cell)
                visited.add(cell)

    if not perfect:
        random_break_steps = _break_random(map, rng)
        if save_step:
            steps.extend(random_break_steps)
    return map, steps
