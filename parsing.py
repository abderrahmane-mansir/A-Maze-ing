from typing import List, Tuple, Callable
import sys


def parsing() -> Tuple[int, int, Tuple[int, int], Tuple[int, int]]:
    """
    Parse configuration values from the config.txt file.

    Returns:
        tuple: (width, height, start, end)
            width (int): grid width
            height (int): grid height
            start (Tuple[int, int]): player start coordinates
            end (Tuple[int, int]): exit coordinates
    """
    width = 0
    height = 0

    with open(sys.argv[1]) as f:
        i = 0
        for line in f:
            key, value = line.split("=", 1)
            key = key.strip().upper()
            value = value.strip()

            if key == "WIDTH":
                width = int(value)
                i += 1

            elif key == "HEIGHT":
                height = int(value)
                i += 1

            elif key == "ENTRY":
                x, y = value.split(",")
                start: Tuple[int, int] = (int(x), int(y))
                i += 1

            elif key == "EXIT":
                x, y = value.split(",")
                end: Tuple[int, int] = (int(x), int(y))
                i += 1

        if i > 4:
            print("invalid argument of config")
            exit(1)

    return width, height, start, end


def cells_of_42(wd: int, ht: int) -> List[Tuple[int, int]]:
    """
    Generate the coordinates that form the '42' shape in the grid center.
    """
    cx = wd // 2
    cy = ht // 2

    cells = [
        (cx + 2, cy - 2),
        (cx + 1, cy - 2),
        (cx + 3, cy - 2),
        (cx + 3, cy - 1),
        (cx + 3, cy),
        (cx + 2, cy),
        (cx + 1, cy),
        (cx + 1, cy + 1),
        (cx + 1, cy + 2),
        (cx + 2, cy + 2),
        (cx + 3, cy + 2),
        (cx - 3, cy - 2),
        (cx - 3, cy - 1),
        (cx - 3, cy),
        (cx - 2, cy),
        (cx - 1, cy),
        (cx - 1, cy + 1),
        (cx - 1, cy + 2),
    ]

    return [(x, y) for x, y in cells if 0 <= x < wd and 0 <= y < ht]


def draw_grid(
    width: int,
    height: int,
    player: Tuple[int, int],
    end: Tuple[int, int],
    color: Callable[[str], str],
    characters: str,
    target: str,
    tracker: str,
    track: List[Tuple[int, int]],
) -> None:
    """
    Render the game grid in the terminal.
    """

    lines: List[str] = []
    cells_42 = cells_of_42(width, height)

    for y in range(height):
        lines.append("█" + "█████" * width)

        middle = ""
        for x in range(width):
            if (x, y) == player:
                cell = characters
            elif (x, y) == end:
                cell = target
            elif (x, y) in cells_42:
                cell = " 💥 "
            elif (x, y) in track:
                cell = tracker
            else:
                cell = "    "

            middle += "█" + cell

        middle += "█"
        lines.append(middle)

    lines.append("█" + "█████" * width)

    print(color("\n".join(lines)))
