"""
Maze generation and solving logic.
"""

import random
from collections import deque
from typing import Dict, List, Tuple

from ft_draw import Cell, close_42_cells


class MazeGenerator:
    """
    Create, generate, and solve a maze.

    Attributes:
        width: Number of columns in the maze.
        height: Number of rows in the maze.
        enter: Entry cell coordinates as (x, y).
        exit: Exit cell coordinates as (x, y).
        perfect: Whether the maze should remain perfect.
        seed: Random seed for reproducibility.
        grid: 2D maze grid.
        path: Solution path from entry to exit.
    """

    def __init__(
        self,
        width: int,
        height: int,
        enter: Tuple[int, int],
        exit: Tuple[int, int],
        perfect: bool,
        seed: int | None,
    ) -> None:
        """Initialize the maze generator."""
        self.width: int = width
        self.height: int = height
        self.enter: Tuple[int, int] = enter
        self.exit: Tuple[int, int] = exit
        self.perfect: bool = perfect
        self.seed: int = random.randint(0, 10**6) if seed is None else seed

        self.grid: List[List[Cell]] = []
        self.path: List[Tuple[int, int]] = []

        center_y: int = self.height // 2
        center_x: int = self.width // 2

        self.list_2: List[Tuple[int, int]] = [
            (center_x + 1, center_y),
            (center_x + 1, center_y + 2),
            (center_x + 3, center_y),
            (center_x + 3, center_y - 1),
            (center_x + 2, center_y - 2),
            (center_x + 3, center_y - 2),
            (center_x + 1, center_y - 2),
            (center_x + 1, center_y + 1),
            (center_x + 2, center_y),
            (center_x + 2, center_y + 2),
            (center_x + 3, center_y + 2),
        ]
        self.list_4: List[Tuple[int, int]] = [
            (center_x - 1, center_y),
            (center_x - 2, center_y),
            (center_x - 3, center_y),
            (center_x - 3, center_y - 1),
            (center_x - 3, center_y - 2),
            (center_x - 1, center_y + 1),
            (center_x - 1, center_y + 2),
        ]

    def create_grid(self) -> List[List[Cell]]:
        """Create the grid with all walls closed."""
        self.grid = []

        for y in range(self.height):
            row: List[Cell] = []
            for x in range(self.width):
                row.append(Cell(x, y))
            self.grid.append(row)

        return self.grid

    def open_passage(self, y: int, x: int, wall: str) -> None:
        """Open a passage between a cell and its neighbor."""
        maze = self.grid

        if wall == "W" and x - 1 >= 0:
            maze[y][x].walls["W"] = False
            maze[y][x - 1].walls["E"] = False
        elif wall == "E" and x + 1 < self.width:
            maze[y][x].walls["E"] = False
            maze[y][x + 1].walls["W"] = False
        elif wall == "N" and y - 1 >= 0:
            maze[y][x].walls["N"] = False
            maze[y - 1][x].walls["S"] = False
        elif wall == "S" and y + 1 < self.height:
            maze[y][x].walls["S"] = False
            maze[y + 1][x].walls["N"] = False

    def generate(self) -> int:
        """Generate the maze and return the seed used."""
        if not self.grid:
            self.create_grid()

        list_42: List[Tuple[int, int]] = self.list_4 + self.list_2
        close_42_cells(self.grid, list_42)
        if self.enter in list_42 or self.exit in list_42:
            raise ValueError("Entry or exit inside 42 pattern")

        random.seed(self.seed)
        maze = self.grid
        x, y = self.enter
        stack: List[Cell] = [maze[y][x]]

        def neighbors(cell_y: int, cell_x: int) -> List[Cell]:
            """Return unvisited neighboring cells of a given cell."""
            neighbor_list: List[Cell] = []

            if cell_x - 1 >= 0 and not maze[cell_y][cell_x - 1].visited:
                neighbor_list.append(maze[cell_y][cell_x - 1])

            if (cell_x + 1 < self.width
                    and not maze[cell_y][cell_x + 1].visited):
                neighbor_list.append(maze[cell_y][cell_x + 1])

            if cell_y - 1 >= 0 and not maze[cell_y - 1][cell_x].visited:
                neighbor_list.append(
                    maze[cell_y - 1][cell_x]
                )

            if (cell_y + 1 < self.height
                    and not maze[cell_y + 1][cell_x].visited):
                neighbor_list.append(maze[cell_y + 1][cell_x])

            return neighbor_list

        def carve_walls(current: Cell, nxt: Cell) -> None:
            current_x, current_y = current.coordinate
            next_x, next_y = nxt.coordinate

            if current_y == next_y:
                if current_x > next_x:
                    self.open_passage(current_y, current_x, "W")
                else:
                    self.open_passage(current_y, current_x, "E")
            elif current_x == next_x:
                if current_y > next_y:
                    self.open_passage(current_y, current_x, "N")
                else:
                    self.open_passage(current_y, current_x, "S")

        while stack:
            x, y = stack[-1].coordinate
            maze[y][x].visited = True
            neighbor_list = neighbors(y, x)

            if neighbor_list:
                next_cell = random.choice(neighbor_list)
                stack.append(next_cell)
                carve_walls(stack[-2], stack[-1])
            else:
                stack.pop()

        if not self.perfect:
            self.imperfect_maze(0.10)

        return self.seed

    def imperfect_maze(self, probability: float = 0.10) -> None:
        """Randomly open extra walls to make maze imperfect."""
        for y in range(self.height):
            for x in range(self.width):
                if random.random() < probability:
                    directions = []
                    if x > 0:
                        directions.append("W")
                    if x < self.width - 1:
                        directions.append("E")
                    if y > 0:
                        directions.append("N")
                    if y < self.height - 1:
                        directions.append("S")

                    if directions:
                        direction = random.choice(directions)
                        self.open_passage(y, x, direction)

    def solver(self) -> None:
        """Find the shortest path from entry to exit using BFS."""
        self.path = []

        maze: List[List[Cell]] = self.grid
        start: Tuple[int, int] = self.enter
        queue: deque[Tuple[int, int]] = deque([start])
        parent: Dict[Tuple[int, int], Tuple[int, int] | None] = {start: None}

        def solver_neighbors(cell: Tuple[int, int]) -> List[Cell]:
            """Return reachable neighbors of the current cell."""
            neighbor_list: List[Cell] = []
            x, y = cell

            if y - 1 >= 0 and not maze[y][x].walls["N"]:
                neighbor_list.append(maze[y - 1][x])
            if y + 1 < self.height and not maze[y][x].walls["S"]:
                neighbor_list.append(maze[y + 1][x])
            if x - 1 >= 0 and not maze[y][x].walls["W"]:
                neighbor_list.append(maze[y][x - 1])
            if x + 1 < self.width and not maze[y][x].walls["E"]:
                neighbor_list.append(maze[y][x + 1])

            return neighbor_list

        while queue:
            current = queue[0]
            neighbor_list = solver_neighbors(current)

            for neighbor in neighbor_list:
                if neighbor.coordinate not in parent:
                    queue.append(neighbor.coordinate)
                    parent[neighbor.coordinate] = current

            if current == self.exit:
                cell: Tuple[int, int] | None = current
                while cell is not None:
                    self.path.append(cell)
                    cell = parent[cell]
                self.path.reverse()
                break

            queue.popleft()
