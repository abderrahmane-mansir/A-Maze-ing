"""
Configuration parsing and terminal maze rendering helpers.
"""

import sys
from typing import Callable, List, Tuple, Set
from ft_draw import Cell


def parsing() -> Tuple[
    int,
    int,
    Tuple[int, int],
    Tuple[int, int],
    str,
    bool,
    int | None,
]:
    """
    Parse configuration values from a config file.

    Expected keys:
    - WIDTH
    - HEIGHT
    - ENTRY=x,y
    - EXIT=x,y
    - OUTPUT_FILE=filename
    - PERFECT=True/False
    - SEED=number (optional)
    """
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        raise SystemExit(1)

    width: int | None = None
    height: int | None = None
    start: Tuple[int, int] | None = None
    end: Tuple[int, int] | None = None
    output_file: str = "maze.txt"
    perfect: bool = True
    seed: int | None = None

    try:
        with open(sys.argv[1], encoding="utf-8") as file:
            for raw_line in file:
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    print(f"Error: invalid config line: {line}")
                    raise SystemExit(1)

                key, value = line.split("=", 1)
                key = key.strip().upper()
                value = value.strip()

                if key == "WIDTH":
                    width = int(value)
                elif key == "HEIGHT":
                    height = int(value)
                elif key == "ENTRY":
                    x_str, y_str = value.split(",", 1)
                    start = (int(x_str), int(y_str))
                elif key == "EXIT":
                    x_str, y_str = value.split(",", 1)
                    end = (int(x_str), int(y_str))
                elif key == "OUTPUT_FILE":
                    output_file = value
                elif key == "PERFECT":
                    if value.lower() not in ("true", "false"):
                        print("Error: PERFECT must be True or False")
                        raise SystemExit(1)
                    perfect = value.lower() == "true"
                elif key == "SEED":
                    seed = int(value)

    except FileNotFoundError:
        print(f"Error: file not found: {sys.argv[1]}")
        raise SystemExit(1)
    except ValueError as error:
        print(f"Error: invalid config value: {error}")
        raise SystemExit(1)
    except OSError as error:
        print(f"Error: cannot read config file: {error}")
        raise SystemExit(1)

    if width is None or height is None or start is None or end is None:
        print("Error: missing required config keys")
        raise SystemExit(1)

    return width, height, start, end, output_file, perfect, seed


def draw_grid(
    width: int,
    height: int,
    grid: List[List[Cell]],
    player: Tuple[int, int],
    end: Tuple[int, int],
    color: Callable[[str], str],
    characters: str,
    target: str,
    tracker: str,
    track: List[Tuple[int, int]],
    path: List[Tuple[int, int]],
    show_path: bool,
    move_path: str,
    bombs: Set[Tuple[int, int]],
) -> None:
    """Render the maze grid with cells, player, target, and path."""
    lines: List[str] = []
    cells_42: Set[Tuple[int, int]] = set()

    for y in range(height):
        for x in range(width):
            cell = grid[y][x]
            if all(cell.walls.values()):
                cells_42.add((x, y))

    for y in range(height):
        top_line = ""
        middle_line = ""

        for x in range(width):
            cell = grid[y][x]

            north_closed = cell.walls["N"]
            east_closed = cell.walls["E"]
            west_closed = cell.walls["W"]

            top_line += "█"
            top_line += "█████" if north_closed else "     "

            middle_line += "█" if west_closed else " "

            if (x, y) == player:
                middle_line += characters
            elif (x, y) == end:
                middle_line += target
            elif (x, y) in cells_42:
                middle_line += "  💥 "
            elif (x, y) in bombs:
                middle_line += "  💣 "
            elif show_path and (x, y) in path:
                middle_line += move_path
            elif (x, y) in track:
                middle_line += tracker
            else:
                middle_line += "     "

            if x == width - 1:
                middle_line += "█" if east_closed else " "

        lines.append(top_line + "█")
        lines.append(middle_line)

    # Bottom boundary
    bottom_line = ""
    for x in range(width):
        cell = grid[height - 1][x]
        south_closed = cell.walls["S"]
        bottom_line += "█"
        bottom_line += "█████" if south_closed else "     "
    bottom_line += "█"

    lines.append(bottom_line)
    print(color("\n".join(lines)))
