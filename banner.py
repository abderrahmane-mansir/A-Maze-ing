from blessed import Terminal
import time
import drawing

def banner() -> None:
    term = Terminal()

    # Left and right banners
    left_ascii = r"""
     █████╗ ███╗   ███╗ █████╗ ███╗   ██╗███████╗██╗██████╗ 
    ██╔══██╗████╗ ████║██╔══██╗████╗  ██║██╔════╝██║██╔══██╗
    ███████║██╔████╔██║███████║██╔██╗ ██║███████╗██║██████╔╝
    ██╔══██║██║╚██╔╝██║██╔══██║██║╚██╗██║╚════██║██║██╔══██╗
    ██║  ██║██║ ╚═╝ ██║██║  ██║██║ ╚████║███████║██║██║  ██║
    ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝╚═╝  ╚═╝
    """

    right_ascii = r"""
    ███╗   ██╗ ██████╗ ██████╗  ██████╗ ██╗   ██╗██╗      █████╗ ██╗  ██╗
    ████╗  ██║██╔═══██╗██╔══██╗██╔═══██╗██║   ██║██║     ██╔══██╗██║  ██║
    ██╔██╗ ██║██║   ██║██║  ██║██║   ██║██║   ██║██║     ███████║███████║
    ██║╚██╗██║██║   ██║██║  ██║██║   ██║██║   ██║██║     ██╔══██║██╔══██║
    ██║ ╚████║╚██████╔╝██████╔╝╚██████╔╝╚██████╔╝███████╗██║  ██║██║  ██║
    ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝  ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝
    """

    # Fixed red ASCII art
    ascii_art = r"""
    ████████╗██╗  ██╗███████╗    ███╗   ███╗ █████╗ ███████╗███████╗    ██████╗ ██╗   ██╗███╗   ██╗███╗   ██╗███████╗██████╗ 
    ╚══██╔══╝██║  ██║██╔════╝    ████╗ ████║██╔══██╗╚══███╔╝██╔════╝    ██╔══██╗██║   ██║████╗  ██║████╗  ██║██╔════╝██╔══██╗
       ██║   ███████║█████╗      ██╔████╔██║███████║  ███╔╝ █████╗      ██████╔╝██║   ██║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
       ██║   ██╔══██║██╔══╝      ██║╚██╔╝██║██╔══██║ ███╔╝  ██╔══╝      ██╔══██╗██║   ██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
       ██║   ██║  ██║███████╗    ██║ ╚═╝ ██║██║  ██║███████╗███████╗    ██║  ██║╚██████╔╝██║ ╚████║██║ ╚████║███████╗██║  ██║
       ╚═╝   ╚═╝  ╚═╝╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝    ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
    """

    # Vertical alignment
    max_height = max(len(left_ascii.splitlines()), len(right_ascii.splitlines()), len(ascii_art.splitlines()))
    y_pos = max((term.height - max_height) // 4, 0)

    # Widths
    left_width = max(len(line) for line in left_ascii.splitlines())
    right_width = max(len(line) for line in right_ascii.splitlines())
    art_width = max(len(line) for line in ascii_art.splitlines())

    # Center positions
    center_x = term.width // 2
    left_target_x = center_x - left_width - 1
    right_target_x = center_x + 1
    art_x = max((term.width - art_width) // 2, 0)

    # Colors
    BLUE = term.color_rgb(0, 0, 255)
    RED = term.color_rgb(255, 0, 0)

    with term.fullscreen(), term.hidden_cursor():
        print(term.clear)
        for i, line in enumerate(ascii_art.splitlines()):
            print(term.move_yx(y_pos + i, art_x) + RED(line))
        time.sleep(2)

        # Start positions
        left_x = -left_width
        right_x = term.width

        # Slide animation once
        while left_x < left_target_x or right_x > right_target_x:
            print(term.clear)
            # Draw red ASCII art
            for i, line in enumerate(ascii_art.splitlines()):
                print(term.move_yx(y_pos + i, art_x) + RED(line))
            # Update positions
            if left_x < left_target_x:
                left_x += 2
            if right_x > right_target_x:
                right_x -= 2
            # Draw sliding banners
            for i, line in enumerate(right_ascii.splitlines()):
                print(term.move_yx(y_pos + i, right_x) + BLUE(line))
            time.sleep(0.05)

        # Draw banners once centered and exit
        print(term.clear)
        for i, line in enumerate(left_ascii.splitlines()):
            print(term.move_yx(y_pos + i, left_target_x) + BLUE(line))
        for i, line in enumerate(right_ascii.splitlines()):
            print(term.move_yx(y_pos + i, right_target_x) + BLUE(line))
        drawing.start_sound("./sound/victory.mp3")
        time.sleep(1.2)  # pause to see final result