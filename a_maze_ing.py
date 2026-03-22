"""
Main entry point for the terminal grid game.

This module validates configuration values and
starts the game drawing loop.
"""
import sys
import os
try:
    from parsing import parsing
    from drawing import drawing
except ModuleNotFoundError:
    print("Warning: Required dependency not "
          "found. Some features may not work.")
    print("Use this to fix: make install")
    sys.exit(1)


os.system("clear")
def main() -> None:
    """
    Validate configuration values from the config file.

    Checks:
    - Grid width and height limits (10–50).
    - Valid start coordinates.
    - Valid end coordinates.
    - Start and end positions are different.

    Exits the program with an error message if any value is invalid.
    """
    width, height, start, end = parsing()
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


if __name__ == "__main__":
    try:
        main()
        drawing()
    except KeyboardInterrupt:
        print("Game exited by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
