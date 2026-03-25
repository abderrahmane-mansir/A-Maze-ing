"""CLI entry point for the ``mazegen`` package."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Tuple

from .core import Maze


def _parse_coord(value: str) -> Tuple[int, int]:
    try:
        x_str, y_str = value.split(",", 1)
        return (int(x_str), int(y_str))
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "coordinates must be in 'x,y' format"
        ) from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate and render mazes.")
    parser.add_argument("--width", type=int, required=True, help="Maze width")
    parser.add_argument(
        "--height",
        type=int,
        required=True,
        help="Maze height",
    )
    parser.add_argument("--entry", type=_parse_coord, default=(0, 0))
    parser.add_argument("--exit", dest="exit_coord", type=_parse_coord)
    parser.add_argument("--seed", type=int)
    parser.add_argument(
        "--imperfect",
        action="store_true",
        help="Open extra random walls to create loops",
    )
    parser.add_argument(
        "--solve",
        action="store_true",
        help="Overlay the shortest path from entry to exit",
    )
    parser.add_argument("--output", type=Path, help="Write output to file")
    return parser


def main() -> int:
    args = build_parser().parse_args()

    maze = Maze(
        width=args.width,
        height=args.height,
        entry=args.entry,
        exit=args.exit_coord,
        perfect=not args.imperfect,
        seed=args.seed,
    )
    used_seed = maze.generate()
    path = maze.solve() if args.solve else None
    rendered = maze.to_ascii(path=path)

    if args.output:
        args.output.write_text(rendered + "\n")
    else:
        print(rendered)

    print(f"seed={used_seed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
