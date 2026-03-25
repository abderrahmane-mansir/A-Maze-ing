from blessed import Terminal
import time
import drawing

"""
banner.py

This module displays an animated ASCII art banner in the terminal using the
blessed library. It shows a central ASCII art, then slides left and right
pieces of text into view, and plays a victory sound at the end.

Dependencies:
- blessed
- drawing (for start_sound)
"""


def banner() -> None:
    """
    Display an animated terminal banner with ASCII art and sound.

    The animation sequence is as follows:
    1. Clear the terminal and display the central ASCII art in red.
    2. Wait 2 seconds.
    3. Slide in the left and right ASCII banners from off-screen to center.
    4. clear the screen and display both side banners in blue.
    5. Play the victory sound.
    6. Pause briefly before finishing.

    Uses `blessed.Terminal` for terminal control and cursor management.

    Returns:
        None
    """
    term = Terminal()

    with open("./files_txt/ascii_art.txt", "r") as f:
        ascii_art = f.read()
    with open("./files_txt/left_ascii.txt", "r") as f:
        left_ascii = f.read()
    with open("./files_txt/right_ascii.txt", "r") as f:
        right_ascii = f.read()

    max_height = max(
        len(left_ascii.splitlines()),
        len(right_ascii.splitlines()),
        len(ascii_art.splitlines()),
    )
    y_pos = max((term.height - max_height) // 4, 0)

    left_width = max(len(line) for line in left_ascii.splitlines())
    art_width = max(len(line) for line in ascii_art.splitlines())

    center_x = term.width // 2
    left_target_x = center_x - left_width - 1
    right_target_x = center_x + 1
    art_x = max((term.width - art_width) // 2, 0)

    BLUE = term.color_rgb(0, 0, 255)
    RED = term.color_rgb(255, 0, 0)

    with term.fullscreen(), term.hidden_cursor():
        print(term.clear)
        for i, line in enumerate(ascii_art.splitlines()):
            print(term.move_yx(y_pos + i, art_x) + RED(line))
        time.sleep(2)

        left_x = -left_width
        right_x = term.width

        while left_x < left_target_x or right_x > right_target_x:
            print(term.clear)

            for i, line in enumerate(ascii_art.splitlines()):
                print(term.move_yx(y_pos + i, art_x) + RED(line))

            if left_x < left_target_x:
                left_x += 2
            if right_x > right_target_x:
                right_x -= 2

            for i, line in enumerate(right_ascii.splitlines()):
                print(term.move_yx(y_pos + i, right_x) + BLUE(line))

            time.sleep(0.05)

        print(term.clear)
        for i, line in enumerate(left_ascii.splitlines()):
            print(term.move_yx(y_pos + i, left_target_x) + BLUE(line))
        for i, line in enumerate(right_ascii.splitlines()):
            print(term.move_yx(y_pos + i, right_target_x) + BLUE(line))

        drawing.start_sound("./sound/victory.mp3")
        time.sleep(1.2)
