*This project has been created as part of the 42 curriculum by amansir and nodoulah.*

# 🧩 A-Maze-ing

## 📌 Description

A-Maze-ing is a terminal-based maze game built in Python using the `blessed` library.  
The goal of the project is to generate a maze dynamically and allow the player to navigate from an entry point to an exit point while avoiding obstacles.

The maze is displayed in the terminal with a custom visual grid, and the player interacts using keyboard inputs. The project demonstrates algorithmic thinking, real-time terminal rendering, and user interaction.

## 📁 Project Structure

```text
A-Maze-ing/
├── a_maze_ing.py
├── banner.py
├── config.txt
├── drawing.py
├── files_txt/
│   ├── 1.txt
│   ├── 2.txt
│   ├── 3.txt
│   ├── ascii_art.txt
│   ├── enter.txt
│   ├── game_end.txt
│   ├── game_over.txt
│   ├── key_maping.txt
│   ├── key_player.txt
│   ├── left_ascii.txt
│   ├── loading.txt
│   ├── right_ascii.txt
│   └── win.txt
├── ft_draw.py
├── gen.py
├── .gitignore
├── intro.py
├── Makefile
├── maze.txt
├── mazegen/
│   ├── __init__.py
│   ├── __main__.py
│   └── core.py
├── output_maze.py
├── parsing.py
├── pyproject.toml
├── README.md
├── README_MAZEGEN.md
└── sound/
    ├── ack.mp3
    ├── bomb.mp3
    ├── correct.mp3
    ├── duck-toy-sound.mp3
    ├── gta-san-andreas.mp3
    ├── ive-got-this-faaaaaaaaahhhhh.mp3
    ├── oi-oi-oe-oi-a-eye-eye.mp3
    ├── pop.mp3
    ├── rizz-sound-effect.mp3
    ├── spongebob-walking-sound-single.mp3
    └── victory.mp3
```

---

## ⚙️ Instructions

### 🔧 Installation

```bash
make install
```

### ▶️ Run the game

```bash
make run
```

### 🐞 Debug mode

```bash
make debug
```

### 🧹 Clean project

```bash
make clean
```

## ♻️ Reusable Package (`mazegen`)

This repository includes a reusable Python package named `mazegen`.

Build from source:

```bash
python -m pip install --upgrade pip build
python -m build
```

Install from generated files:

```bash
pip install ./mazegen-1.0.0-py3-none-any.whl
```

or:

```bash
pip install ./mazegen-1.0.0.tar.gz
```

Example usage:

```python
from mazegen import generate_maze

maze = generate_maze(width=20, height=12, seed=42)
print(maze.to_ascii(path=maze.solve()))
```

## 🎮 Controls
            ┌────────────────────────────────┐
            |           key maping           |
            |────────────────────────────────|
            |   r    : change color      🎨  |
            |   g    : generate maze     ⚙️  |
            |   s    : show / hide path  🧭  |
            |   p    : player mode       🎮  |
            |   c    : change character  👥  |
            |   t    : show / hide track 🛣️  |
            |   b    : bomb mode         💣  |
            |   m    : mini map          🗺️  |
            |   q    : Quit              🚫  |
            └────────────────────────────────┘
## 📄 Config File Structure
The `config.txt` file must follow this format:
```text
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
```
Rules:
- Width and height must be between 10 and 50
- ENTRY and EXIT must be inside the grid
- ENTRY ≠ EXIT


# 📚 Resources
## Documentation
- https://docs.python.org/3/
- https://blessed.readthedocs.io/
- https://docs.python.org/3/library/pdb.html
## Algorithms
- https://en.wikipedia.org/wiki/Maze_generation_algorithm
- https://en.wikipedia.org/wiki/Depth-first_search
## 🤖 AI Usage
AI tools were used for:

- Debugging errors
- Improving code structure
- Explaining algorithms
- Generating boilerplate (Makefile, README)
- Helping with terminal rendering and centering


### Rules

- `WIDTH` and `HEIGHT` must be between **10 and 50**
- `ENTRY` and `EXIT` must be valid coordinates inside the grid
- `ENTRY` and `EXIT` must be different

---

## 🧠 Maze Generation Algorithm

We implemented a **Depth-First Search (DFS) with backtracking** algorithm.

### How it works

1. Start from the entry cell
2. Mark it as visited
3. Randomly choose an unvisited neighbor
4. Move to that neighbor and continue
5. If no neighbors are available, backtrack
6. Repeat until all reachable cells are visited

This creates a maze with one main connected path and branching dead-ends.

---

## 🤔 Why this algorithm?

We chose DFS because:

- It is simple and intuitive to implement
- It guarantees that there is at least one valid path from entry to exit
- It produces visually interesting mazes
- It is efficient and works well with grid-based structures

---

## 👥 Team & Project Management

### 👤 **amansir**
  - Maze generation implementation
  - Game logic (movement, collision)
### 👤 **nodoulah**
  - Debugging and testing
  - UI rendering and improvements

---

### 📅 Planning & Evolution

#### Initial plan
- Create grid system
- Implement player movement
- Add static obstacles

#### Evolution
- Replaced static obstacles with dynamic maze generation
- Improved user interaction (controls, feedback)
- Added sound effects and visual improvements
- Centered the UI for better experience

---

### ✅ What worked well

- Modular structure (parsing / drawing / main)
- Incremental development approach
- Easy debugging with `pdb`
- Clear separation between logic and display

---

### ⚠️ What could be improved

- Better visualization of maze walls (currently block-based)
- Cleaner separation between game logic and UI
- Add multiple maze generation algorithms
- Improve performance for larger grids

---

### 🛠 Tools Used

- **Python 3** — main language
- **Blessed** — terminal rendering and input handling
- **pygame** — sound effects
- **Makefile** — automation
- **Git** — version control
- **pdb** — debugging tool