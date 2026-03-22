"""
Terminal grid game using Blessed.

This module runs the main game loop, handles player movement,
renders the grid, manages health, sounds, and UI interactions.
"""

import os
import time
import threading
from typing import List, Tuple, Callable

import pygame
from blessed import Terminal
from parsing import parsing, draw_grid, cells_of_42


def playsound(sound: str) -> None:
    """Play a sound asynchronously using pygame."""
    pygame.mixer.init()
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()


def start_sound(sound_path: str) -> None:
    """Helper to start a sound in a daemon thread."""
    threading.Thread(target=playsound, args=(sound_path,), daemon=True).start()


def drawing() -> None:
    """
    Run the main game interface and gameplay loop.

    Handles terminal initialization, player input, grid updates,
    animations, and sound effects. Ends when the player wins,
    loses all health, or quits.
    """
    term: Terminal = Terminal()
    os.system("clear")
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        width, height, player, end = parsing()
        save_x, save_y = player

        track: List[Tuple[int, int]] = [player]
        track_set: set[Tuple[int, int]] = {player}
        show_track: bool = True
        blocked_42: set[Tuple[int, int]] = set(cells_of_42(width, height))

        colors: List[Callable[[str], str]] = [term.yellow, term.green,
                                              term.blue, term.magenta]
        characters: List[str] = [" 🏃 ", " 🚗 "]
        target: List[str] = [" 🚪 ", " ⛽ "]
        tracker: List[str] = [" 👣 ", " 💨 "]

        color_index: int = 0
        char_index: int = 0
        target_index: int = 0
        tracker_index: int = 0
        player_mode: bool = False

        health: str = "❤️ ❤️ ❤️ "
        health_count: int = 9
        count_move: int = 0

        with open("./files_txt/key_maping.txt") as f:
            menu_text: str = f.read()

        os.system("clear")
        start_sound("./sound/ive-got-this-faaaaaaaaahhhhh.mp3")

        # Intro animations
        for intro_file, delay in [
            ("./files_txt/1.txt", 0.3),
            ("./files_txt/2.txt", 0.3),
            ("./files_txt/3.txt", 0.3),
        ]:
            with open(intro_file) as f:
                print(term.white(f.read().strip()))
            time.sleep(delay)
            os.system("clear")

        with open("./files_txt/intro.txt") as f:
            print(term.red(f.read().strip()))
        time.sleep(1.8)
        os.system("clear")

        with open("./files_txt/loading.txt") as f:
            for line in f:
                print(term.green(line.strip()))

        start_sound("./sound/gta-san-andreas.mp3")

        for i in range(18):
            print(term.move_yx(8, i * 3) +
                  term.green("▆▆▆"), end="", flush=True)
            time.sleep(0.5)

        os.system("clear")
        with open("./files_txt/enter.txt") as f:
            enter_text: str = f.read().strip()

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

    # Main game loop
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        while True:
            os.system("clear")
            draw_grid(
                width,
                height,
                player,
                end,
                colors[color_index],
                characters[char_index],
                target[target_index],
                tracker[tracker_index],
                list(track_set) if show_track else [],  # Convert set to list
            )

            print(term.move_yx(height * 2 + 2, 0) + menu_text)
            print(
                term.move_yx(height * 2 + 2, width * 2 + 2)
                + term.white(health[:health_count]),
                flush=True,
            )
            print(
                term.move_yx(height * 2 + 2, 0)
                + term.white(f"move counter: {count_move}"),
                flush=True,
            )

            key = term.inkey()
            x, y = player

            if player not in track_set:
                track.append(player)
                track_set.add(player)

            # Quit game
            if key == "q":
                os.system("clear")
                start_sound("./sound/oi-oi-oe-oi-a-eye-eye.mp3")
                with open("./files_txt/game_end.txt") as f:
                    print(term.red(f.read().strip()))
                time.sleep(5)
                os.system("clear")
                break

            # Cycle colors
            elif key == "r":
                color_index = (color_index + 1) % len(colors)
                start_sound("./sound/duck-toy-sound.mp3")

            # Reset player position
            elif key == "c":
                x, y = save_x, save_y
                track = [(x, y)]
                track_set = {(x, y)}
                count_move = 0
                start_sound("./sound/rizz-sound-effect.mp3")
                char_index = (char_index + 1) % len(characters)
                target_index = (target_index + 1) % len(target)
                tracker_index = (tracker_index + 1) % len(tracker)

            # Toggle player mode
            elif key == "p":
                start_sound("./sound/correct.mp3")
                x, y = save_x, save_y
                player_mode = not player_mode
                file_name: str = (
                    "./files_txt/key_player.txt" if player_mode
                    else "./files_txt/key_maping.txt"
                )
                with open(file_name) as f:
                    menu_text = f.read()

            # Toggle track display
            elif key == "t":
                show_track = not show_track

            # Player movement
            elif player_mode:
                move_sounds: dict[str, Tuple[int, int]] = {
                    "KEY_UP": (0, -1),
                    "KEY_DOWN": (0, 1),
                    "KEY_LEFT": (-1, 0),
                    "KEY_RIGHT": (1, 0),
                }

                if key.name in move_sounds:
                    dx, dy = move_sounds[key.name]
                    new_x = x + dx
                    new_y = y + dy
                    if 0 <= new_x < width and 0 <= new_y < height:
                        start_sound("./sound/spongebob"
                                    "-walking-sound-single.mp3")
                        x, y = new_x, new_y
                        count_move += 1

                if (x, y) in blocked_42:
                    x, y = save_x, save_y
                    track = [(x, y)]
                    track_set = {(x, y)}
                    start_sound("./sound/ack.mp3")
                    time.sleep(0.3)
                    health_count -= 3
                    count_move = 0

            # Check health
            if health_count <= 0:
                os.system("clear")
                with open("./files_txt/game_over.txt") as f:
                    print(term.red(f.read().strip()))
                time.sleep(2.5)
                os.system("clear")
                break

            player = (x, y)

            # Check victory
            if player == end:
                os.system("clear")
                with open("./files_txt/win.txt") as f:
                    print(term.green(f.read().strip()))
                start_sound("./sound/victory.mp3")
                time.sleep(1.1)
                os.system("clear")
                break
