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
    import pygame
    import time
    import threading
    from blessed import Terminal
    from output_maze import save_output_file
except ModuleNotFoundError:
    print("Warning: Required dependency not found.")
    print("Use this to fix: make install")
    sys.exit(1)


def safe_read(path: str) -> str:
    """Read a file safely and return a default value on failure."""
    with open(path) as file:
        return file.read()
def playsound(sound: str) -> None:
    """Play a sound asynchronously using pygame."""
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play()
    except (pygame.error, FileNotFoundError):
        pass


def start_sound(sound_path: str) -> None:
    """Helper to start a sound in a daemon thread."""
    threading.Thread(target=playsound, args=(sound_path,), daemon=True).start()
def intro() -> None:
    term: Terminal = Terminal()
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        os.system("clear")
        start_sound("./sound/ive-got-this-faaaaaaaaahhhhh.mp3")

        for intro_file, delay in [
            ("./files_txt/1.txt", 0.3),
            ("./files_txt/2.txt", 0.3),
            ("./files_txt/3.txt", 0.3),
        ]:
            intro_text = safe_read(intro_file)
            if intro_text:
                print(term.white(intro_text.strip()))
                time.sleep(delay)
                os.system("clear")

        intro_main = safe_read("./files_txt/intro.txt")
        print(term.red(intro_main.strip()))
        time.sleep(1.8)
        os.system("clear")

        loading_text = safe_read("./files_txt/loading.txt")
        if loading_text:
            for line in loading_text.splitlines():
                print(term.green(line.strip()))

        start_sound("./sound/gta-san-andreas.mp3")

        for i in range(18):
            print(term.move_yx(8, i * 3) + term.green("▆▆▆"), end="", flush=True)
            time.sleep(0.08)

        os.system("clear")
        enter_text: str = safe_read("./files_txt/enter.txt").strip()

        while True:
            key = term.inkey(timeout=0.1)
            if key and key.name == "KEY_ENTER":
                start_sound("./sound/rizz-sound-effect.mp3")
                break
            print(term.green(enter_text))
            time.sleep(0.5)
            os.system("clear")
            time.sleep(0.5)

        os.system("clear")

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
    list[list[object]],
    list[tuple[int, int]],
]:
    """Parse config, validate it, generate the maze, and solve it."""
    width, height, start, end, output_file,perfect , seed = parsing()
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

    return width, height, start, end, maze.grid, maze.path
if __name__ == "__main__":
    try:
        #intro()
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
