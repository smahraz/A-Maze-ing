from mazegen import Maze, Cell, Step
from random import Random

def random_cell(cells: set[Cell], rng: Random) -> Cell:
    return rng.choice(list(cells))

def get_neighbours(cell: Cell) -> list[Cell]:
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
    valid = []

    for neighbour in get_neighbours(cell):
        if neighbour in maze:
            valid.append(neighbour)

    neighbour = rng.choice(valid)
    match neighbour:
        case cell.above_cell:
            cell.north.open()
            return 'N'
        case cell.left_cell:
            cell.west.open()
            return 'W'
        case cell.right_cell:
            cell.east.open()
            return 'E'
        case cell.below_cell:
            cell.south.open()
            return 'S'
            
    

def PRIM(map: Maze, save_step: bool, rng: Random) -> tuple[Maze, list[Step]]:
    pool: set[Cell] = set()
    maze: set[Cell] = set()
    frontier: set[Cell] = set()
    steps: list[Step] = []
    
    for cell in map.cell_iterator():
        if cell.is_protected:
            continue
        pool.add(cell)

    cell_count = len(pool)
    cell = random_cell(pool, rng)
    maze.add(cell)
    if save_step:
            steps.append(Step(cell.x, cell.y, None))
    pool.remove(cell)

    for neighbour in get_neighbours(cell):
        if neighbour in pool:
            frontier.add(neighbour)
            pool.remove(neighbour)

    while len(maze) != cell_count:
        cell = random_cell(frontier, rng)
        wall = connect_cells(cell, maze, rng)
        maze.add(cell)
        frontier.remove(cell)
        if save_step:
            steps.append(Step(cell.x, cell.y, wall))
        for neighbour in get_neighbours(cell):
            if neighbour in pool:
                frontier.add(neighbour)
                pool.remove(neighbour)

    return map, steps