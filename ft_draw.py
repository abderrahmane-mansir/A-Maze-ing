"""
Maze cell helpers.
"""


class Cell:
    """Represent one maze cell with four walls."""

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.visited = False
        self.walls = {
            "N": True,
            "E": True,
            "S": True,
            "W": True,
        }

    @property
    def coordinate(self) -> tuple[int, int]:
        """Return cell coordinates as (x, y)."""
        return (self.x, self.y)


def close_42_cells(
    grid: list[list[Cell]],
    coords: list[tuple[int, int]],
) -> None:
    """Mark the cells used to draw 42 as visited and fully closed."""
    if not grid or not grid[0]:
        return

    for x, y in coords:
        if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
            grid[y][x].visited = True
            grid[y][x].walls["N"] = True
            grid[y][x].walls["E"] = True
            grid[y][x].walls["S"] = True
            grid[y][x].walls["W"] = True