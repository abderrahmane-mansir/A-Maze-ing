"""Reusable maze generation package.

The public API exposes the :class:`Maze` class and convenience helper
:func:`generate_maze`.
"""

from .core import Maze, generate_maze

__all__ = ["Maze", "generate_maze"]
__version__ = "1.0.0"
