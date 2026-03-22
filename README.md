*This project has been created as part of the 42 curriculum by amansir and nodoulah.*

# 🧩 A-Maze-ing

## 📌 Description

A-Maze-ing is a terminal-based maze game built in Python using the `blessed` library.  
The goal of the project is to generate a maze dynamically and allow the player to navigate from an entry point to an exit point while avoiding obstacles.

The maze is displayed in the terminal with a custom visual grid, and the player interacts using keyboard inputs. The project demonstrates algorithmic thinking, real-time terminal rendering, and user interaction.

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

## 🎮 Controls
            ┌────────────────────────────────┐
            |           key maping           |
            |────────────────────────────────|
            |   r    : change color      🎨  |
            |   g    : generate maze     ⚙️  |
            |   s    : show / hide path  🧭  |
            |   p    : player mode       🎮  |
            |   c    : change character  👥  |
            |   t    : show / hide track 🗺️  |
            |   q    : Quit              🚫  |
            └────────────────────────────────┘
## 📄 Config File Structure
The `config.txt` file must follow this format:
```bash
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

## 🔁 Reusable Code

Several parts of the project are reusable:

### 🔹 Maze generation logic
- Can be reused in other grid-based games or simulations

### 🔹 draw_grid()
- A generic terminal rendering function that can display any grid-based system

### 🔹 Input handling system
- Keyboard interaction using `blessed` can be reused in other terminal apps

### 🔹 Config parser
- The parsing system can be reused for other projects requiring configuration files

---

## 👥 Team & Project Management

### 👤 **amnsir**
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