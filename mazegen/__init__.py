"""
Maze generation package.

This package provides classes and functions for generating,
encoding, and analyzing rectangular mazes. Supported algorithms
include DFS and Prim. It also includes utilities for computing
paths and exporting maze representations.
"""
from .maze import Maze, Cell, MazeError
from .utils import Step
from .generator import MazeGenerator


__all__ = [
    "Maze",
    "Cell",
    "MazeGenerator",
    "Step",
    "MazeError"
]
