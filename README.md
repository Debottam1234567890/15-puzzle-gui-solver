# 15-Puzzle GUI Solver

Welcome to **15-Puzzle GUI Solver**, an interactive application designed to solve the classic 15-puzzle using advanced AI search algorithms with a graphical interface.

**Goal:** Rearrange the 15 numbered tiles on a 4x4 grid to reach the ordered configuration (1-15 with empty space in the bottom-right corner).

---

## Features

### Interactive GUI

* User-friendly graphical interface built with **Tkinter**.
* Drag-and-click or keyboard navigation to move tiles.
* Real-time visualization of puzzle state.

### Advanced Solvers

* **A*** Search with multiple heuristics:

  * Manhattan Distance
  * Linear Conflict
  * Misplaced Tiles
* **IDA*** (Iterative Deepening A*) for memory-efficient search.
* Step-by-step solution visualization.

### Real-Time Statistics

* Moves count
* Time taken to solve
* Heuristic cost display

### Customization

* Shuffle puzzle randomly
* Input custom puzzle configurations
* Choose different heuristics for AI solving

---

## How It Works

1. **Puzzle Representation:** Internal 2D array represents the board state.
2. **Move Generation:** Generates all valid moves from the current state.
3. **Heuristic Evaluation:** Calculates cost using selected heuristic.
4. **Search Algorithm:** AI searches for optimal solution using A* or IDA*.
5. **Visualization:** Updates GUI for each move until the puzzle is solved.

---

## Requirements

**Python Version:** 3.8+

**Libraries:**

```bash
pip install numpy
pip install pygame
```

---

## How to Run

1. Clone or download the repository:

```
git clone https://github.com/Debottam1234567890/15-puzzle-gui-solver.git
```

2. Navigate into the folder:

```
cd 15-puzzle-gui-solver
```

3. Run the main GUI application:

```
python3 solve.py
```

---

## Usage

* Click **Shuffle** to randomize the puzzle.
* Click **Solve** to see the AI solution.
* Use keyboard arrow keys or click tiles to move manually.
* Select heuristic from dropdown to change AI solving strategy.

---

## Contributing

* Add new heuristics or solving algorithms.
* Improve GUI design and animations.
* Add support for NxN puzzles beyond 4x4.

---

## About

15-Puzzle GUI Solver combines classic puzzle solving with modern AI algorithms to provide an educational and interactive experience. Ideal for learning search algorithms and heuristic techniques in AI.
