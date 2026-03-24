import os
import time
import threading
from blessed import Terminal
import pygame
from banner import banner


def safe_read(path: str) -> str:
    """Read a file safely and return a default value on failure."""
    with open(path, encoding="utf-8") as file:
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
    threading.Thread(
        target=playsound, args=(sound_path,), daemon=True
    ).start()


def intro() -> None:
    """Display the intro sequence with animated text, sounds, and banner."""
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

        banner()
        os.system("clear")

        loading_text = safe_read("./files_txt/loading.txt")
        if loading_text:
            for line in loading_text.splitlines():
                print(term.green(line.strip()))

        start_sound("./sound/gta-san-andreas.mp3")

        for i in range(18):
            print(term.move_yx(8, i * 3) + term.green("▆▆▆"),
                  end="", flush=True)
            time.sleep(0.13)

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
