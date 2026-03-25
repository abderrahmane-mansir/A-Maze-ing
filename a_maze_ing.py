"""
Main entry point for the terminal maze game.

This module validates configuration values, generates the maze,
solves it, and starts the drawing loop.
"""

import os
import sys

try:
    from parsing import parsing
    from drawing import drawing
    from gen import MazeGenerator
    from intro import intro
    from output_maze import save_output_file
    from ft_draw import Cell
except ModuleNotFoundError:
    print("Warning: Required dependency not found.")
    print("Use this to fix: make install")
    sys.exit(1)


def validate_config(
    width: int,
    height: int,
    start: tuple[int, int],
    end: tuple[int, int],
) -> None:
    """Validate parsed configuration values."""
    x_start, y_start = start
    x_end, y_end = end

    if not (10 <= width <= 50):
        print("Error: width invalid")
        sys.exit(1)

    if not (10 <= height <= 50):
        print("Error: height invalid")
        sys.exit(1)

    if not (0 <= x_start < width and 0 <= y_start < height):
        print("Error: start position invalid")
        sys.exit(1)

    if not (0 <= x_end < width and 0 <= y_end < height):
        print("Error: end position invalid")
        sys.exit(1)

    if start == end:
        print("Error: start and end must be different")
        sys.exit(1)


def main() -> tuple[
    int,
    int,
    tuple[int, int],
    tuple[int, int],
    list[list[Cell]],
    list[tuple[int, int]],
]:
    """Parse config, validate it, generate the maze, and solve it."""
    width, height, start, end, output_file, perfect, seed = parsing()
    validate_config(width, height, start, end)
    maze = MazeGenerator(
        width=width,
        height=height,
        enter=start,
        exit=end,
        perfect=perfect,
        seed=seed,
    )

    maze.create_grid()
    maze.generate()
    maze.solver()
    save_output_file(
        filename=output_file,
        grid=maze.grid,
        entry=start,
        exit_=end,
        path=maze.path,
    )
    intro()
    return width, height, start, end, maze.grid, maze.path


if __name__ == "__main__":
    try:
        os.system("clear")
        os.system("clear")

        while True:
            width, height, start, end, grid, path = main()
            result = drawing(width, height, start, end, grid, path)

            if result is None:
                continue
            if result == "quit":
                break

    except KeyboardInterrupt:
        print("\nGame exited by user.")
        sys.exit(0)
    except Exception as error:
        print(f"Unexpected error: {error}")
        sys.exit(1)
