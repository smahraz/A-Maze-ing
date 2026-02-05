*This project has been created as part of the 42 curriculum by smahraz, smakkass.*

---

# A-Maze-ing

A maze generation program with graphical and terminal-based visualization, animation support, and path finding capabilities.

---

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Instructions](#instructions)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Usage](#usage)
- [Configuration File](#configuration-file)
- [Maze Generation Algorithms](#maze-generation-algorithms)
- [Reusable Components](#reusable-components)
- [Advanced Features](#advanced-features)
- [Team and Project Management](#team-and-project-management)
- [Resources](#resources)

---

## Description

A-Maze-ing is a maze generation and visualization tool developed in Python. The program generates rectangular mazes using configurable algorithms, displays them through either a graphical user interface (GUI) or a text-based terminal interface (TUI), and supports animated generation as well as path finding from entry to exit.

The project is structured as a modular application with a reusable maze generation library (`mazegen`) that can be installed independently.

---

## Features

- Rectangular maze generation with configurable dimensions
- Two generation algorithms: DFS and Prim
- Perfect and imperfect maze options
- GUI and TUI display modes
- Step-by-step generation animation
- Path finding from entry to exit
- Configurable entry and exit positions
- Reproducible results via seed configuration
- Maze export to file

---

## Instructions

### Requirements

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/saidmakkass/A-Maze-ing.git
cd A-Maze-ing
```

2. Install dependencies:
```bash
make install
```

Or manually:
```bash
uv sync
uv pip install mlx-*.whl
```

### Usage

Run with the default configuration:
```bash
make run
```

Or specify a custom configuration file:
```bash
python3 a_maze_ing.py <config_file>
```

Example:
```bash
python3 a_maze_ing.py default_config.txt
```

---

## Configuration File

The configuration file uses a simple `KEY=VALUE` format. Lines starting with `#` are comments.

### Structure

```
# Comment lines start with #
KEY=VALUE
```

### Available Options

| Key | Required | Description | Default |
|-----|----------|-------------|---------|
| `WIDTH` | Yes | Maze width (Greater than 8) | - |
| `HEIGHT` | Yes | Maze height (Greater than 6) | - |
| `ENTRY` | Yes | Starting position (format: `x,y`) | - |
| `EXIT` | Yes | Ending position (format: `x,y`) | - |
| `OUTPUT_FILE` | Yes | Path to save the generated maze | - |
| `PERFECT` | Yes | Perfect maze with single solution (`True`/`False`) | - |
| `SEED` | No | Random seed for reproducible generation | Random |
| `ALGORITHM` | No | Generation algorithm (`DFS` or `PRIM`) | `DFS` |
| `INTERFACE` | No | Display mode (`gui` or `tui`) | `gui` |

### Example Configuration

```
WIDTH=25
HEIGHT=15
ENTRY=10,10
EXIT=1,1
OUTPUT_FILE=maze.txt
PERFECT=False
SEED=1234567
ALGORITHM=DFS
INTERFACE=gui
```

---

## Maze Generation Algorithms

### Implemented Algorithms

**Depth-First Search (DFS)**
- Creates long, winding passages
- Produces aesthetically pleasing maze patterns
- Simple implementation

**Prim's Algorithm**
- Creates more uniform, branching patterns
- Produces visually appealing animations during generation

### Why We Chose Both

Each algorithm has distinct strengths:

- **DFS** produces more visually appealing final mazes with long corridors and is simpler to implement. It is recommended for general use.
- **Prim** generates mazes with more uniform branching and looks impressive when animated.

We implemented both to give users flexibility based on their preferences and use cases.

---

## Reusable Components

### mazegen Library

The `mazegen/` module is a standalone, reusable maze generation library with no external dependencies. It can be installed separately via pip:

```bash
pip install mazegen-*.whl
```

#### Basic Usage

```python
from mazegen import MazeGenerator

mazegen = MazeGenerator(
    width=20,
    height=10,
    algorithm="DFS",
    perfect=True,
    seed=42,
    entry=(0, 0),
    exit=(19, 9)
)

maze = mazegen.generate_maze()
```

#### Available Features

- `generate_maze()` - Generate a maze
- `generate()` - Generate maze with step-by-step data for animation
- `generate_steps()` - Get only the generation steps
- Access to the 2D cell grid via `mazegen.maze.map`

See [README-mazegen.md](README-mazegen.md) for full documentation.

---

## Advanced Features

### Graphical User Interface (GUI)

A full graphical interface for maze visualization with:
- Real-time maze rendering
- Path visualization
- Interactive controls

<p align="center">
  <img src="assets/gui_screenshot.png" alt="GUI Screenshot" width="600">
</p>

### Text User Interface (TUI)

A terminal-based interface featuring:
- ANSI color rendering
- Animated maze generation
- Path display toggle
- Color theme cycling

<p align="center">
  <img src="assets/tui_screenshot.png" alt="TUI Screenshot" width="600">
</p>

### Generation Animation

Both interfaces support step-by-step visualization of the maze generation process.

<p align="center">
  <img src="assets/animation_demo.gif" alt="Generation Animation" width="550">
</p>

### Multiple Algorithms

Users can switch between DFS and Prim algorithms via the configuration file to achieve different maze characteristics.

---

## Team and Project Management

### Team Members and Roles

| Member | Role |
|--------|------|
| **smahraz** | TUI development, maze algorithms (DFS), build configuration |
| **smakkass** | GUI development, parser, path finding, PRIM algorithm |

### Planning and Evolution

**Initial Approach:**
Each team member claimed the parts they were most interested in working on. After individual implementation, we collaborated to fix bugs, improve code style, and ensure consistency.

**Communication:**
Frequent communication was maintained throughout the project to coordinate integration and resolve issues promptly.

### What Worked Well

- Code from each team member integrated smoothly with the other's work
- Clear division of responsibilities allowed parallel development
- Regular communication prevented integration issues

### Areas for Improvement

- Code efficiency could be optimized further

### Tools Used

- **Git** for version control and collaboration

---

## Resources

### References

- [Maze Generation: Prim's Algorithm - Jamis Buck](https://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm)
- [Maze Generation Algorithm Overview (YouTube)](https://www.youtube.com/watch?v=Y37-gB83HKE)
- [Maze Algorithms Visualization (YouTube)](https://www.youtube.com/watch?v=uctN47p_KVk)

### AI Usage

AI tools were used in this project for:
- **Debugging**: Locating stubborn logic bugs that were difficult to identify manually
- **Learning**: Understanding new Python concepts and best practices

AI was not used for generating core algorithm implementations or project architecture.

---
