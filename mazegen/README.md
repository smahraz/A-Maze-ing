# mazegen

A lightweight Python library for generating and solving rectangular mazes. Supports DFS and Prim algorithms, step-by-step generation for animations, and path finding.

**No external dependencies required.**

---

## Installation

```bash
pip install mazegen-*.whl
```

---

## Quick Start

```python
from mazegen import MazeGenerator

# Create and generate a maze
gen = MazeGenerator(width=20, height=10, algorithm="DFS", perfect=True, seed=42, entry=(0, 0), exit=(19, 9))
maze = gen.generate_maze()

# Find solution path
path = MazeGenerator.generate_path(maze)
print("Solution:", "".join(direction for _, direction in path))
```

---

## API Reference

### MazeGenerator

The main class for creating and managing mazes.

#### Constructor

```python
MazeGenerator(
    width: int,          # Maze width (columns)
    height: int,         # Maze height (rows)
    algorithm: str,      # "DFS" or "PRIM"
    perfect: bool,       # True = no loops, False = some extra passages
    seed: int,           # Random seed for reproducibility
    entry: tuple[int, int],  # Starting cell (x, y)
    exit: tuple[int, int]    # Ending cell (x, y)
)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `width` | `int` | Number of columns (must be > 0) |
| `height` | `int` | Number of rows (must be > 0) |
| `algorithm` | `str` | Generation algorithm: `"DFS"` or `"PRIM"` |
| `perfect` | `bool` | `True` for single-solution maze, `False` for additional openings |
| `seed` | `int` | Random seed for reproducible generation |
| `entry` | `tuple[int, int]` | Entry coordinates `(x, y)` |
| `exit` | `tuple[int, int]` | Exit coordinates `(x, y)` |

#### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `generate_maze()` | `Maze` | Generate maze without recording steps |
| `generate()` | `tuple[Maze, list[Step]]` | Generate maze with animation steps |
| `generate_steps()` | `list[Step]` | Generate and return only the steps |
| `generate_path(maze)` | `list[tuple[Cell, str]]` | Static method - find path from entry to exit |
| `output()` | `str` | Export maze as encoded string with solution |
| `reseed()` | `None` | Assign a new random seed |

---

## Usage Examples

### Basic Maze Generation

```python
from mazegen import MazeGenerator

# Initialize generator
gen = MazeGenerator(
    width=15,
    height=10,
    algorithm="DFS",
    perfect=True,
    seed=12345,
    entry=(0, 0),
    exit=(14, 9)
)

# Generate the maze
maze = gen.generate_maze()

print(f"Maze size: {maze.width}x{maze.height}")
print(f"Entry: ({maze.entry.x}, {maze.entry.y})")
print(f"Exit: ({maze.exit.x}, {maze.exit.y})")
```

### Accessing the Maze Structure

```python
from mazegen import MazeGenerator

gen = MazeGenerator(width=10, height=8, algorithm="PRIM", perfect=True, seed=999, entry=(0, 0), exit=(9, 7))
maze = gen.generate_maze()

# Access the 2D grid of cells
grid = maze.map  # list[list[Cell]]

# Iterate through all cells
for y, row in enumerate(grid):
    for x, cell in enumerate(row):
        # Check wall states
        print(f"Cell ({x},{y}): N={cell.north.is_closed}, E={cell.east.is_closed}, S={cell.south.is_closed}, W={cell.west.is_closed}")
```

### Finding and Using the Solution Path

```python
from mazegen import MazeGenerator

gen = MazeGenerator(width=20, height=15, algorithm="DFS", perfect=True, seed=42, entry=(0, 0), exit=(19, 14))
maze = gen.generate_maze()

# Get solution path
path = MazeGenerator.generate_path(maze)

# path is a list of (Cell, direction) tuples
# Directions: 'N' (north), 'S' (south), 'E' (east), 'W' (west)
for cell, direction in path:
    print(f"From ({cell.x}, {cell.y}) go {direction}")

# Get solution as direction string
solution = "".join(direction for _, direction in path)
print(f"Solution: {solution}")
```

### Generation with Animation Steps

```python
from mazegen import MazeGenerator

gen = MazeGenerator(width=10, height=10, algorithm="DFS", perfect=True, seed=123, entry=(0, 0), exit=(9, 9))

# Get maze and steps for animation
maze, steps = gen.generate()

# Each step contains: x, y, wall (direction opened)
for step in steps:
    print(f"Step at ({step.x}, {step.y}), opened wall: {step.wall}")
```

### Exporting Maze Data

```python
from mazegen import MazeGenerator

gen = MazeGenerator(width=10, height=8, algorithm="PRIM", perfect=True, seed=777, entry=(0, 0), exit=(9, 7))
gen.generate_maze()

# Export complete maze data
output = gen.output()
print(output)

# Output format:
# - Hex-encoded maze layout (one line per row)
# - Entry coordinates (x,y)
# - Exit coordinates (x,y)
# - Solution path directions
```

### Using Different Algorithms

```python
from mazegen import MazeGenerator

# DFS: Creates long winding corridors
dfs_gen = MazeGenerator(width=20, height=15, algorithm="DFS", perfect=True, seed=42, entry=(0, 0), exit=(19, 14))
dfs_maze = dfs_gen.generate_maze()

# Prim: Creates more branching, uniform patterns
prim_gen = MazeGenerator(width=20, height=15, algorithm="PRIM", perfect=True, seed=42, entry=(0, 0), exit=(19, 14))
prim_maze = prim_gen.generate_maze()
```

---

## Data Structures

### Cell

Each cell in the maze has four walls and links to adjacent cells.

```python
cell.north.is_closed  # bool - True if wall exists
cell.south.is_closed
cell.east.is_closed
cell.west.is_closed

cell.above_cell  # Cell | None - neighbor to the north
cell.below_cell  # Cell | None - neighbor to the south
cell.right_cell  # Cell | None - neighbor to the east
cell.left_cell   # Cell | None - neighbor to the west

cell.x  # int - column position
cell.y  # int - row position
```

### Step

Records a single step during maze generation.

```python
step.x     # int - cell x coordinate
step.y     # int - cell y coordinate
step.wall  # str | None - wall opened: 'N', 'S', 'E', 'W', or None
```

---

## Algorithm Comparison

| Algorithm | Pattern | Best For |
|-----------|---------|----------|
| **DFS** | Long corridors, winding paths | Visual appeal, classic maze feel |
| **PRIM** | Uniform branching, shorter passages | Balanced difficulty, animations |

---

## Notes

- Entry and exit positions use `(x, y)` coordinates where `x` is the column and `y` is the row
- Coordinates are 0-indexed
- The maze includes a protected "42" pattern in the center for dimensions ≥ 9x7
- Avoid placing entry/exit on protected cells
