"""
Terminal grid game using Blessed.

This module runs the main game loop, handles player movement,
renders the grid, manages health, sounds, and UI interactions.
"""

import os
import time
import threading
import random
from typing import List, Tuple, Callable
from ft_draw import Cell

import pygame
from blessed import Terminal

from parsing import draw_grid

characters: List[str] = ["  🏃 ", "  🚗 "]
target: List[str] = ["  🚪 ", "  ⛽ "]
tracker: List[str] = ["  👣 ", "  💨 "]
move_path: str = "  ⭐ "

pygame.mixer.init()


def playsound(sound: str) -> None:
    """Play a sound asynchronously using pygame."""
    try:
        pygame.mixer.Sound(sound).play()
    except Exception:  # Avoid bare except
        pass


def start_sound(sound_path: str) -> None:
    """Helper to start a sound in a daemon thread."""
    threading.Thread(
        target=playsound, args=(sound_path,), daemon=True
    ).start()


def safe_read(path: str) -> str:
    """Read a file safely and return a default value on failure."""
    with open(path, encoding="utf-8") as file:
        return file.read()


def cells_of_42_from_grid(grid: List[List[Cell]]) -> List[Tuple[int, int]]:
    """
    Return coordinates of cells reserved for the visible 42 pattern.

    A cell belongs to the pattern when it is still fully closed.
    """
    blocked: List[Tuple[int, int]] = []

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if (
                cell.walls["N"]
                and cell.walls["E"]
                and cell.walls["S"]
                and cell.walls["W"]
            ):
                blocked.append((x, y))

    return blocked


def can_move(
    grid: list[list[Cell]],
    width: int,
    height: int,
    x: int,
    y: int,
    key_name: str | None,
) -> Tuple[int, int, bool]:
    """Move the player only through open maze walls."""
    cell = grid[y][x]
    moved = False

    if key_name == "KEY_UP" and y > 0 and not cell.walls["N"]:
        y -= 1
        moved = True
    elif key_name == "KEY_DOWN" and y < height - 1 and not cell.walls["S"]:
        y += 1
        moved = True
    elif key_name == "KEY_LEFT" and x > 0 and not cell.walls["W"]:
        x -= 1
        moved = True
    elif key_name == "KEY_RIGHT" and x < width - 1 and not cell.walls["E"]:
        x += 1
        moved = True

    return x, y, moved


def remaining_path(
    path: list[tuple[int, int]],
    player: tuple[int, int],
) -> list[tuple[int, int]]:
    """Return the remaining solution path starting from the player."""
    if player in path:
        index = path.index(player)
        return path[index:]
    return path


def spawn_random_bomb(
    width: int,
    height: int,
    player: tuple[int, int],
    end: tuple[int, int],
    blocked_42: set[tuple[int, int]],
    track_set: set[tuple[int, int]],
    bombs: set[tuple[int, int]],
) -> tuple[int, int] | None:
    """Spawn a bomb in a safe random cell."""
    candidates: list[tuple[int, int]] = []

    for y in range(height):
        for x in range(width):
            pos = (x, y)

            if pos == player:
                continue
            if pos == end:
                continue
            if pos in blocked_42:
                continue
            if pos in track_set:
                continue
            if pos in bombs:
                continue

            candidates.append(pos)

    if not candidates:
        return None

    return random.choice(candidates)


def draw_minimap(
    term: Terminal,
    grid: list[list[Cell]],
    player: tuple[int, int],
    end: tuple[int, int],
    track_set: set[tuple[int, int]],
    bombs: set[tuple[int, int]],
    show_path: bool,
    path: list[tuple[int, int]],
    start_y: int,
    start_x: int,
) -> None:
    """Draw a small mini map on the right side."""
    height = len(grid)
    width = len(grid[0]) if grid else 0
    blocked_42 = set(cells_of_42_from_grid(grid))

    lines: list[str] = ["MINI MAP"]

    for y in range(height):
        row = ""
        for x in range(width):
            pos = (x, y)

            if pos == player:
                row += term.yellow("P")
            elif pos == end:
                row += term.yellow("E")
            elif pos in blocked_42:
                row += term.red("#")
            elif pos in bombs:
                row += term.cyan("B")
            elif show_path and pos in path:
                row += term.green("*")
            elif pos in track_set:
                row += term.blue("*")
            else:
                row += "x"
        lines.append(row)

    for i, line in enumerate(lines):
        print(term.move_yx(start_y + i, start_x) + term.white(line), end="")


def animate_solver(
    term: Terminal,
    width: int,
    height: int,
    grid: list[list[Cell]],
    player: tuple[int, int],
    end: tuple[int, int],
    color: Callable[[str], str],
    characters_skin: str,
    target_skin: str,
    tracker_skin: str,
    track: list[tuple[int, int]],
    path: list[tuple[int, int]],
    menu_text: str,
    count_move: int,
    bombs: set[tuple[int, int]],
    health_text: str,
    show_minimap: bool,
) -> None:
    """Animate the shortest path step by step."""
    shown_path: list[tuple[int, int]] = []

    for step in path:
        shown_path.append(step)
        os.system("clear")

        draw_grid(
            width=width,
            height=height,
            grid=grid,
            player=player,
            end=end,
            color=color,
            characters=characters_skin,
            target=target_skin,
            tracker=tracker_skin,
            track=track,
            path=shown_path,
            show_path=True,
            move_path=move_path,
            bombs=bombs,
        )
        if show_minimap:
            draw_minimap(
                term=term,
                grid=grid,
                player=player,
                end=end,
                track_set=set(track),
                bombs=bombs,
                show_path=True,
                path=shown_path,
                start_y=0,
                start_x=width * 6 + 12,
            )

        print(term.move_yx(height * 2 + 3, 0) + menu_text)
        print(
            term.move_yx(height * 2 + 1, 0)
            + term.white(f"move counter: {count_move}"),
            flush=True,
        )
        print(
            term.move_yx(height * 2 + 2, 0)
            + term.white(health_text),
            flush=True,
        )

        time.sleep(0.08)
        start_sound("./sound/pop.mp3")


def drawing(
    width: int,
    height: int,
    player: tuple[int, int],
    end: tuple[int, int],
    grid: list[list[Cell]],
    path: list[tuple[int, int]],
) -> str | None:
    """
    Run the main game interface and gameplay loop.

    Handles terminal initialization, player input, grid updates,
    animations, and sound effects. Ends when the player wins or quits.
    """
    term: Terminal = Terminal()
    os.system("clear")

    save_x, save_y = player

    track: List[Tuple[int, int]] = [player]
    track_set: set[Tuple[int, int]] = {player}
    show_track: bool = True
    show_path: bool = False
    show_minimap: bool = True
    dynamic_mode: bool = False
    blocked_42: set[Tuple[int, int]] = set(cells_of_42_from_grid(grid))
    bombs: set[Tuple[int, int]] = set()

    colors: List[Callable[[str], str]] = [
        term.yellow,
        term.green,
        term.blue,
        term.magenta,
    ]

    color_index: int = 0
    char_index: int = 0
    target_index: int = 0
    tracker_index: int = 0
    player_mode: bool = False
    count_move: int = 0
    health_count: int = 3

    menu_text: str = safe_read(
        "./files_txt/key_maping.txt"
    )
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        while True:
            os.system("clear")
            draw_grid(
                width=width,
                height=height,
                grid=grid,
                player=player,
                end=end,
                color=colors[color_index],
                characters=characters[char_index],
                target=target[target_index],
                tracker=tracker[tracker_index],
                track=track if show_track else [],
                path=path,
                show_path=show_path,
                move_path=move_path,
                bombs=bombs,
            )

            if show_minimap:
                draw_minimap(
                    term=term,
                    grid=grid,
                    player=player,
                    end=end,
                    track_set=track_set,
                    bombs=bombs,
                    show_path=show_path,
                    path=path,
                    start_y=0,
                    start_x=width * 6 + 12,
                )

            print(term.move_yx(height * 2 + 3, 0) + menu_text)
            print(
                term.move_yx(height * 2 + 1, 0)
                + term.white(f"move counter: {count_move}"),
                flush=True,
            )
            print(
                term.move_yx(height * 2 + 2, 0)
                + term.white(
                    f"health: {health_count}/3 | mini map: "
                    f"{'on' if show_minimap else 'off'} | "
                    f"bomb mode: {'on' if dynamic_mode else 'off'} |"
                    f" bombs: {len(bombs)}"
                ),
                flush=True,
            )

            key = term.inkey()
            x, y = player

            track.append(player)
            track_set.add(player)

            if key == "q":
                os.system("clear")
                start_sound("./sound/oi-oi-oe-oi-a-eye-eye.mp3")
                end_text = safe_read("./files_txt/game_end.txt")
                print(term.red(end_text.strip()))
                time.sleep(5)
                os.system("clear")
                return "quit"

            elif key == "r":
                color_index = (color_index + 1) % len(colors)
                start_sound("./sound/duck-toy-sound.mp3")

            elif key == "c":
                x, y = save_x, save_y
                player = (x, y)
                track = [(x, y)]
                track_set = {(x, y)}
                bombs.clear()
                count_move = 0
                start_sound("./sound/rizz-sound-effect.mp3")
                char_index = (char_index + 1) % len(characters)
                target_index = (target_index + 1) % len(target)
                tracker_index = (tracker_index + 1) % len(tracker)

            elif key == "p":
                start_sound("./sound/correct.mp3")
                x, y = save_x, save_y
                player_mode = not player_mode
                file_name: str = (
                    "./files_txt/key_player.txt"
                    if player_mode
                    else "./files_txt/key_maping.txt"
                )
                menu_text = safe_read(file_name)

            elif key == "t":
                show_track = not show_track

            elif key == "m":
                show_minimap = not show_minimap

            elif key == "b":
                dynamic_mode = not dynamic_mode
                if not dynamic_mode:
                    bombs.clear()

            elif key == "s":
                bombs.clear()
                if not show_path:
                    animated_path = remaining_path(path, player)
                    animate_solver(
                        term=term,
                        width=width,
                        height=height,
                        grid=grid,
                        player=player,
                        end=end,
                        color=colors[color_index],
                        characters_skin=characters[char_index],
                        target_skin=target[target_index],
                        tracker_skin=tracker[tracker_index],
                        track=track if show_track else [],
                        path=animated_path,
                        menu_text=menu_text,
                        count_move=count_move,
                        bombs=bombs,
                        health_text=f"health: {health_count}/3 |"
                        f" bombs: {len(bombs)}",
                        show_minimap=show_minimap
                    )
                    start_sound("./sound/victory.mp3")
                    show_path = True
                else:
                    show_path = False

            elif key == "g":
                return "new_maze"

            elif player_mode:
                new_x, new_y, moved = can_move(
                    grid=grid,
                    width=width,
                    height=height,
                    x=x,
                    y=y,
                    key_name=key.name if key else None,
                )

                if moved:
                    start_sound("./sound/spongebob-walking-sound-single.mp3")
                    x, y = new_x, new_y
                    count_move += 1
                    if (x, y) in path:
                        path.remove((x, y))
                    track.append((x, y))
                    track_set.add((x, y))
                    if dynamic_mode and count_move % 5 == 0:
                        bomb = spawn_random_bomb(
                            width=width,
                            height=height,
                            player=(x, y),
                            end=end,
                            blocked_42=blocked_42,
                            track_set=track_set,
                            bombs=bombs,
                        )
                        if bomb is not None:
                            bombs.add(bomb)
                            start_sound("./sound/bomb.mp3")

                if (x, y) in bombs:
                    bombs.remove((x, y))
                    start_sound("./sound/ack.mp3")
                    x, y = save_x, save_y
                    track = [(x, y)]
                    track_set = {(x, y)}
                    count_move = 0
                    health_count -= 1
                    time.sleep(0.3)

            if health_count == 0:
                os.system("clear")
                game_over_text = safe_read("./files_txt/game_over.txt")
                print(term.red(game_over_text.strip()))
                time.sleep(2.5)
                os.system("clear")
                return "lose"

            player = (x, y)

            if player == end:
                os.system("clear")
                win_text = safe_read("./files_txt/win.txt")
                print(term.green(win_text.strip()))
                start_sound("./sound/victory.mp3")
                time.sleep(1.1)
                os.system("clear")
                return "win"
