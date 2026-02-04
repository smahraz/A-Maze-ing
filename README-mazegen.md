# Maze Generator

A terminal-based maze generation library with visualization, animation, and path finding. It supports multiple algorithms (DFS and Prim), step-by-step generation, ANSI-colored rendering, and exporting a compact textual representation.

---

## Features

* Generate rectangular mazes
* Algorithms: **Depth-First Search (DFS)** and **Prim**
* Perfect or imperfect mazes
* Step recording for animation
* Terminal rendering with ANSI colors
* Path finding from entry to exit
* Export maze encoding

---

## Installation
You will find the wheel find in **releases**.
```bash
pip install mazegen-*.whl
```

No external dependencies are required.

---

## Core Concepts

### Maze

A `Maze` is a grid of `Cell` objects. Each cell has four walls (north, east, south, west) that can be opened or closed.

* Entry and exit are fixed cells
* Mazes can be encoded into a compact hexadecimal format

### MazeGenerator

`MazeGenerator` is the main API for generating mazes.

It controls:

* Maze dimensions
* Algorithm selection
* Random seed
* Whether the maze is perfect (no loops)

---

## Basic Usage

### Create a MazeGenerator

```python
from mazegen import MazeGenerator

mazegen = MazeGenerator(
    width=20,
    height=10,
    algorithm="DFS",  # or "PRIM"
    perfect=True,
    seed=42,
    entry=(0, 0),
    exit=(19, 9)
)
```
**Notes:**
* Avoid setting entry or exit inside 42 patter.
* Avoid setting entry or exit outside of map.

### Generate a Maze

```python
maze = mazegen.generate_maze()
```

### Generate With Steps (for animation)

```python
maze, steps = mazegen.generate()
```

Or only the steps:

```python
steps = mazegen.generate_steps()
```

### Access 2D Array Of Cells
```python
mazegen.generate()
map = mazegen.maze.map
```

---

## Maze Generation Algorithms

### Depth-First Search (DFS)

DFS generates mazes by exploring as far as possible along each branch before backtracking.

Characteristics:

* Produces long corridors
* Always generates a perfect maze when enabled
* Fast and simple

### Prim's Algorithm

Prim's algorithm builds the maze by gradually expanding from a starting cell.

Characteristics:

* Produces more evenly distributed passages
* Always generates a perfect maze when enabled
* Slightly more random-looking layouts

---

## Path Finding

Compute and display a path from entry to exit:

```python
maze = mazegen.generate_maze()
path = MazeGenerator.generate_path(maze)
```

---

## Exporting Maze Output

You can export the maze as a string:

```python
output = mazegen.output()
print(output)
```

The output includes:

* Hex-encoded maze layout
* Entry coordinates
* Exit coordinates
* Path directions

---

## Configuration Options

### Algorithm Selection

Choose the algorithm when creating a `MazeGenerator`:

```python
MazeGenerator(..., algorithm="DFS", ...)
MazeGenerator(..., algorithm="PRIM", ...)
```

### Perfect vs Imperfect Mazes

* `perfect=True`: exactly one

## Notes

* ANSI colors require a compatible terminal
* Private methods are implementation details and may change
