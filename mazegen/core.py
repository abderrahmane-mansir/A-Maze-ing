"""Core maze generation and solving utilities for the ``mazegen`` package."""

from __future__ import annotations

from collections import deque
import random
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

Coord = Tuple[int, int]
WallMap = Dict[str, bool]


@dataclass
class Cell:
    """Represent one maze cell with four walls.

    Wall values are booleans where ``True`` means the wall is closed.
    """

    x: int
    y: int
    visited: bool = False

    def __post_init__(self) -> None:
        self.walls: WallMap = {"N": True, "E": True, "S": True, "W": True}

    @property
    def coordinate(self) -> Coord:
        """Return coordinates as ``(x, y)``."""
        return (self.x, self.y)


class Maze:
    """Generate and solve a 2D maze.

    Parameters:
        width: Number of columns.
        height: Number of rows.
        entry: Entry coordinate ``(x, y)``.
        exit: Exit coordinate ``(x, y)``. If ``None``, bottom-right is used.
        perfect: Keep a perfect maze (single unique path between points).
        seed: Optional random seed for deterministic generation.
    """

    def __init__(
        self,
        width: int,
        height: int,
        entry: Coord = (0, 0),
        exit: Optional[Coord] = None,
        perfect: bool = True,
        seed: Optional[int] = None,
    ) -> None:
        if width < 2 or height < 2:
            raise ValueError("width and height must be >= 2")

        self.width = width
        self.height = height
        self.entry = entry
        self.exit = (width - 1, height - 1) if exit is None else exit
        self.perfect = perfect
        self.seed = random.randint(0, 10**9) if seed is None else seed

        self._validate_coord(self.entry, "entry")
        self._validate_coord(self.exit, "exit")
        if self.entry == self.exit:
            raise ValueError("entry and exit must be different")

        self.grid: List[List[Cell]] = [
            [Cell(x, y) for x in range(self.width)] for y in range(self.height)
        ]

    def _validate_coord(self, value: Coord, name: str) -> None:
        x, y = value
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError(f"{name} must be inside the maze bounds")

    def _open_passage(self, y: int, x: int, wall: str) -> None:
        if wall == "W" and x - 1 >= 0:
            self.grid[y][x].walls["W"] = False
            self.grid[y][x - 1].walls["E"] = False
        elif wall == "E" and x + 1 < self.width:
            self.grid[y][x].walls["E"] = False
            self.grid[y][x + 1].walls["W"] = False
        elif wall == "N" and y - 1 >= 0:
            self.grid[y][x].walls["N"] = False
            self.grid[y - 1][x].walls["S"] = False
        elif wall == "S" and y + 1 < self.height:
            self.grid[y][x].walls["S"] = False
            self.grid[y + 1][x].walls["N"] = False

    def generate(self, imperfection_probability: float = 0.1) -> int:
        """Generate the maze and return the seed used."""
        # Reinitialize the grid so repeated generate() calls are deterministic
        # and produce a fresh maze from the same parameters.
        self.grid = [
            [Cell(x, y) for x in range(self.width)] for y in range(self.height)
        ]
        random.seed(self.seed)

        stack: List[Cell] = [self.grid[self.entry[1]][self.entry[0]]]

        while stack:
            current = stack[-1]
            current.visited = True
            x, y = current.coordinate

            candidates: List[Cell] = []
            if x - 1 >= 0 and not self.grid[y][x - 1].visited:
                candidates.append(self.grid[y][x - 1])
            if x + 1 < self.width and not self.grid[y][x + 1].visited:
                candidates.append(self.grid[y][x + 1])
            if y - 1 >= 0 and not self.grid[y - 1][x].visited:
                candidates.append(self.grid[y - 1][x])
            if y + 1 < self.height and not self.grid[y + 1][x].visited:
                candidates.append(self.grid[y + 1][x])

            if not candidates:
                stack.pop()
                continue

            nxt = random.choice(candidates)
            nx, ny = nxt.coordinate
            if y == ny:
                self._open_passage(y, x, "W" if x > nx else "E")
            else:
                self._open_passage(y, x, "N" if y > ny else "S")
            stack.append(nxt)

        if not self.perfect:
            self.make_imperfect(probability=imperfection_probability)

        return self.seed

    def make_imperfect(self, probability: float = 0.1) -> None:
        """Open additional random walls to create loops."""
        if probability <= 0:
            return

        for y in range(self.height):
            for x in range(self.width):
                if random.random() >= probability:
                    continue
                directions: List[str] = []
                if x > 0:
                    directions.append("W")
                if x < self.width - 1:
                    directions.append("E")
                if y > 0:
                    directions.append("N")
                if y < self.height - 1:
                    directions.append("S")
                if directions:
                    self._open_passage(y, x, random.choice(directions))

    def solve(self) -> List[Coord]:
        """Find a shortest path from entry to exit using BFS."""
        queue: deque[Coord] = deque([self.entry])
        parent: Dict[Coord, Optional[Coord]] = {self.entry: None}

        while queue:
            x, y = queue.popleft()
            if (x, y) == self.exit:
                break

            if y > 0 and not self.grid[y][x].walls["N"]:
                self._push_neighbor((x, y - 1), (x, y), parent, queue)
            if y + 1 < self.height and not self.grid[y][x].walls["S"]:
                self._push_neighbor((x, y + 1), (x, y), parent, queue)
            if x > 0 and not self.grid[y][x].walls["W"]:
                self._push_neighbor((x - 1, y), (x, y), parent, queue)
            if x + 1 < self.width and not self.grid[y][x].walls["E"]:
                self._push_neighbor((x + 1, y), (x, y), parent, queue)

        if self.exit not in parent:
            return []

        path: List[Coord] = []
        node: Optional[Coord] = self.exit
        while node is not None:
            path.append(node)
            node = parent[node]
        path.reverse()
        return path

    @staticmethod
    def _push_neighbor(
        neighbor: Coord,
        current: Coord,
        parent: Dict[Coord, Optional[Coord]],
        queue: deque[Coord],
    ) -> None:
        if neighbor in parent:
            return
        parent[neighbor] = current
        queue.append(neighbor)

    def to_ascii(
        self,
        path: Optional[List[Coord]] = None,
        wall_char: str = "█",
        empty_char: str = " ",
        path_char: str = ".",
    ) -> str:
        """Return a text rendering of the maze.

        The rendering uses a ``(2*height + 1) x (2*width + 1)`` character grid.
        """
        rows = 2 * self.height + 1
        cols = 2 * self.width + 1
        canvas = [[wall_char for _ in range(cols)] for _ in range(rows)]

        for y in range(self.height):
            for x in range(self.width):
                cx = 2 * x + 1
                cy = 2 * y + 1
                canvas[cy][cx] = empty_char

                if not self.grid[y][x].walls["N"]:
                    canvas[cy - 1][cx] = empty_char
                if not self.grid[y][x].walls["S"]:
                    canvas[cy + 1][cx] = empty_char
                if not self.grid[y][x].walls["W"]:
                    canvas[cy][cx - 1] = empty_char
                if not self.grid[y][x].walls["E"]:
                    canvas[cy][cx + 1] = empty_char

        ex, ey = self.entry
        tx, ty = self.exit
        canvas[2 * ey + 1][2 * ex + 1] = "S"
        canvas[2 * ty + 1][2 * tx + 1] = "E"

        if path:
            # Mark both path cells and connecting corridors so the route is
            # visually continuous in the rendered maze.
            corridor_points: List[Tuple[int, int]] = []
            for i in range(1, len(path)):
                x1, y1 = path[i - 1]
                x2, y2 = path[i]
                mx = (2 * x1 + 1 + 2 * x2 + 1) // 2
                my = (2 * y1 + 1 + 2 * y2 + 1) // 2
                corridor_points.append((mx, my))

            for x, y in path:
                if (x, y) in (self.entry, self.exit):
                    continue
                canvas[2 * y + 1][2 * x + 1] = path_char

            for mx, my in corridor_points:
                if canvas[my][mx] == empty_char:
                    canvas[my][mx] = path_char

        # Keep endpoints visible even if path overlay is enabled.
        canvas[2 * ey + 1][2 * ex + 1] = "S"
        canvas[2 * ty + 1][2 * tx + 1] = "E"

        return "\n".join("".join(line) for line in canvas)


def generate_maze(
    width: int,
    height: int,
    entry: Coord = (0, 0),
    exit: Optional[Coord] = None,
    perfect: bool = True,
    seed: Optional[int] = None,
) -> Maze:
    """Create and generate a :class:`Maze` in one call."""
    maze = Maze(
        width=width,
        height=height,
        entry=entry,
        exit=exit,
        perfect=perfect,
        seed=seed,
    )
    maze.generate()
    return maze
