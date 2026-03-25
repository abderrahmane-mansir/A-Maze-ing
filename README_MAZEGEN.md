# mazegen

`mazegen` is a reusable Python package to generate and solve mazes.

## Install (from built artifact)

```bash
pip install ./mazegen-1.0.0-py3-none-any.whl
```

or:

```bash
pip install ./mazegen-1.0.0.tar.gz
```

## Python API

```python
from mazegen import generate_maze

maze = generate_maze(width=20, height=12, seed=42)
path = maze.solve()
print(maze.to_ascii(path=path))
```

## CLI usage

```bash
mazegen --width 20 --height 12 --seed 42 --solve
```

Write to file:

```bash
mazegen --width 20 --height 12 --solve --output generated_maze.txt
```

## Build from sources

```bash
python -m pip install --upgrade pip build
python -m build
```

This creates `dist/mazegen-1.0.0.tar.gz` and `dist/mazegen-1.0.0-py3-none-any.whl`.
