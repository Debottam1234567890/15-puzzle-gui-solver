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

```
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

### Understanding Move Notation
**Important: Move Direction Convention**
The move directions in this solver represent where the empty space moves, which is the standard convention for sliding puzzles.
Example:
Consider this configuration:
12  1 10  2
 7 11  4 14
 5  0  9 15    ← Empty space (0) is at position (2, 1)
 8 13  6  3
When the solution says "move right", it means:

The empty space moves to the right (from column 1 to column 2)
This is accomplished by the tile to the RIGHT of the empty space sliding LEFT into it
In this case, the tile with value 9 at position (2, 2) slides left into the empty position
After the move:

   12  1 10  2
    7 11  4 14
    5  9  0 15    ← Empty space moved right, tile 9 moved left
    8 13  6  3
Direction Summary:

"up": Empty space moves up → tile above slides down
"down": Empty space moves down → tile below slides up
"left": Empty space moves left → tile on left slides right
"right": Empty space moves right → tile on right slides left

This convention makes it intuitive to follow the path of the empty space through the puzzle, which is how humans typically think about solving these puzzles.
---

## Contributing

* Add new heuristics or solving algorithms.
* Improve GUI design and animations.
* Add support for NxN puzzles beyond 4x4.

---

## About

15-Puzzle GUI Solver combines classic puzzle solving with modern AI algorithms to provide an educational and interactive experience. Ideal for learning search algorithms and heuristic techniques in AI.
The website is available at: 
