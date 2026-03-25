"""
Helpers to export the maze in the required output format.
"""

from typing import List, Tuple
from ft_draw import Cell


def cell_to_hex(cell: Cell) -> str:
    """
    Convert one maze cell to a single hexadecimal digit.

    Bit mapping:
    - bit 0: North
    - bit 1: East
    - bit 2: South
    - bit 3: West

    Closed wall = 1
    Open wall = 0
    """
    value = 0

    if cell.walls["N"]:
        value |= 1
    if cell.walls["E"]:
        value |= 2
    if cell.walls["S"]:
        value |= 4
    if cell.walls["W"]:
        value |= 8

    return format(value, "X")


def grid_to_lines(grid: List[List[Cell]]) -> List[str]:
    """Convert the full maze grid to text rows of hexadecimal digits."""
    lines: List[str] = []

    for row in grid:
        line = "".join(cell_to_hex(cell) for cell in row)
        lines.append(line)

    return lines


def path_to_directions(path: List[Tuple[int, int]]) -> str:
    """
    Convert a coordinate path to N/E/S/W directions.

    Example:
    [(0, 0), (1, 0), (1, 1)] -> "ES"
    """
    directions: List[str] = []

    for i in range(1, len(path)):
        x1, y1 = path[i - 1]
        x2, y2 = path[i]

        if x2 == x1 and y2 == y1 - 1:
            directions.append("N")
        elif x2 == x1 + 1 and y2 == y1:
            directions.append("E")
        elif x2 == x1 and y2 == y1 + 1:
            directions.append("S")
        elif x2 == x1 - 1 and y2 == y1:
            directions.append("W")
        else:
            raise ValueError(f"Invalid path step: {(x1, y1)} -> {(x2, y2)}")

    return "".join(directions)


def save_output_file(
    filename: str,
    grid: List[List[Cell]],
    entry: Tuple[int, int],
    exit_: Tuple[int, int],
    path: List[Tuple[int, int]],
) -> None:
    """
    Save the maze to a file in the required subject format.

    Format:
    - maze rows in hex
    - empty line
    - entry coordinates
    - exit coordinates
    - shortest path as N/E/S/W
    """
    maze_lines = grid_to_lines(grid)
    path_string = path_to_directions(path)

    with open(filename, "w") as file:
        for line in maze_lines:
            file.write(line + "\n")

        file.write("\n")
        file.write(f"{entry[0]},{entry[1]}\n")
        file.write(f"{exit_[0]},{exit_[1]}\n")
        file.write(path_string + "\n")
