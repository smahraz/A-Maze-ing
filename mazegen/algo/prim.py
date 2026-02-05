from mazegen import Maze, Cell, Step
from random import Random


def random_cell(cells: dict[Cell, None], rng: Random) -> Cell:
    """
    Select a random cell from a dictionary of cells.

    Args:
        cells (dict[Cell, None]): Dictionary of cells to choose from.
        rng (Random): Random number generator.

    Returns:
        Cell: A randomly selected cell.
    """
    return rng.choice(list(cells.keys()))


def get_neighbours(cell: Cell) -> list[Cell]:
    """
    Get all non-protected neighbours of a cell.

    Args:
        cell (Cell): The cell to find neighbours for.

    Returns:
        list[Cell]: List of neighbouring cells that are not protected.
    """
    neighbours = []
    if cell.above_cell and not cell.above_cell.is_protected:
        neighbours.append(cell.above_cell)
    if cell.below_cell and not cell.below_cell.is_protected:
        neighbours.append(cell.below_cell)
    if cell.right_cell and not cell.right_cell.is_protected:
        neighbours.append(cell.right_cell)
    if cell.left_cell and not cell.left_cell.is_protected:
        neighbours.append(cell.left_cell)
    return neighbours


def connect_cells(cell: Cell, maze: set[Cell], rng: Random) -> str:
    """
    Connect a cell to one of its neighbours in the maze.

    This function finds neighbours of the cell that are already
    in the maze and opens a wall to connect them.

    Args:
        cell (Cell): The cell to connect.
        maze (set[Cell]): Set of cells already in the maze.
        rng (Random): Random number generator for choosing neighbour.

    Returns:
        str: The direction of the wall that was opened ('N', 'S', 'E', 'W').
    """
    valid = []

    for neighbour in get_neighbours(cell):
        if neighbour in maze:
            valid.append(neighbour)

    neighbour = rng.choice(valid)
    match neighbour:
        case cell.above_cell:
            cell.north.open()
            wall = 'N'
        case cell.left_cell:
            cell.west.open()
            wall = 'W'
        case cell.right_cell:
            cell.east.open()
            wall = 'E'
        case cell.below_cell:
            cell.south.open()
            wall = 'S'
    return wall


def _open_wall_random(
        cell: Cell,
        should_not_touch: set[Cell | None],
        wall_int: int
) -> tuple[Cell | None, str | None]:
    """
    Open a random wall to create imperfections in the maze.

    This function is used to break walls randomly after the main
    generation to create loops in imperfect mazes.

    Args:
        cell (Cell): The current cell.
        should_not_touch (set[Cell | None]): Cells that should not be modified.
        wall_int (int): Wall index (0-3) indicating direction.

    Returns:
        tuple[Cell | None, str | None]: The neighbouring cell and
        wall direction if opened, otherwise (None, None).
    """
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
    """
    Randomly break walls to create an imperfect maze.

    This function opens approximately 6% of the maze cells'
    walls randomly to introduce loops, making the maze imperfect.

    Args:
        map (Maze): The maze to modify.
        r (Random): Random number generator.

    Returns:
        list[Step]: List of steps representing the walls that were opened.
    """
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


def PRIM(map: Maze, save_step: bool, perfect: bool, rng: Random
         ) -> tuple[Maze, list[Step]]:
    """
    Generate a maze using Prim's algorithm.

    This function uses a randomized version of Prim's algorithm
    to generate a maze. It starts from a random cell and expands
    the maze by connecting frontier cells to the existing maze.

    Args:
        map (Maze): The maze to generate.
        save_step (bool): Whether to record each step in a list.
        perfect (bool): If True, the maze will have no loops.
        rng (Random): Random number generator for path selection.

    Returns:
        tuple[Maze, list[Step]]: The generated maze and a list of
        steps taken if `save_step` is True; otherwise, an empty list.
    """
    pool: dict[Cell, None] = {}
    maze: set[Cell] = set()
    frontier: dict[Cell, None] = {}
    steps: list[Step] = []

    for cell in map.cell_iterator():
        if cell.is_protected:
            continue
        pool[cell] = None

    cell_count = len(pool)
    cell = random_cell(pool, rng)
    maze.add(cell)
    if save_step:
        steps.append(Step(cell.x, cell.y, None))
    del pool[cell]

    for neighbour in get_neighbours(cell):
        if neighbour in pool:
            frontier[neighbour] = None
            del pool[neighbour]

    while len(maze) != cell_count:
        cell = random_cell(frontier, rng)
        wall = connect_cells(cell, maze, rng)
        maze.add(cell)
        del frontier[cell]
        if save_step:
            steps.append(Step(cell.x, cell.y, wall))
        for neighbour in get_neighbours(cell):
            if neighbour in pool:
                frontier[neighbour] = None
                del pool[neighbour]

    if not perfect:
        random_break_steps = _break_random(map, rng)
        if save_step:
            steps.extend(random_break_steps)

    return map, steps
