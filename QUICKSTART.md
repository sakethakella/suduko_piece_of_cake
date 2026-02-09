# Quick Start Guide

## Installation

No external dependencies required - uses only Python standard library!

```bash
git clone https://github.com/sakethakella/suduko_piece_of_cake.git
cd suduko_piece_of_cake
```

## Running Examples

### Basic Example
```bash
python3 sudoku_solver.py
```

### Comprehensive Demo
```bash
python3 example.py
```

### Run Tests
```bash
python3 test_sudoku.py -v
```

## Using in Your Code

### Simple Sudoku Solving

```python
from sudoku_solver import SudokuSolver

# Define puzzle (0 = empty cell)
puzzle = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

solver = SudokuSolver(puzzle)
solution = solver.solve()

SudokuSolver.print_grid(solution)
```

### Using the CSP Framework for Other Problems

```python
from csp import Variable, AllDifferentConstraint, CSP

# Create variables
x = Variable("x", [1, 2, 3])
y = Variable("y", [1, 2, 3])
z = Variable("z", [1, 2, 3])

# Add constraint: all must be different
constraint = AllDifferentConstraint([x, y, z])

# Solve
csp = CSP([x, y, z], [constraint])
solution = csp.solve()

print(f"x={solution[x]}, y={solution[y]}, z={solution[z]}")
```

## API Reference

### SudokuSolver

- `__init__(grid)`: Initialize with 9x9 list (0 for empty cells)
- `solve()`: Returns solved 9x9 grid or None if no solution
- `print_grid(grid)`: Pretty print a Sudoku grid
- `is_valid_solution(grid)`: Validate a solution

### CSP

- `solve()`: Solve the CSP using backtracking + MRV + AC3 + forward checking
- `backtrack()`: Backtracking search with MRV and forward checking
- `ac3()`: Apply Arc Consistency 3 algorithm
- `select_unassigned_variable_mrv()`: Select variable with MRV heuristic
- `forward_check()`: Perform forward checking

### Variable

- `__init__(name, domain)`: Create a variable with name and list of possible values

### Constraint

- `is_satisfied(assignment)`: Check if constraint is satisfied (override in subclasses)

## Performance

- Easy puzzles (30+ given cells): < 0.1 seconds
- Medium puzzles (25-30 given cells): < 1 second
- Hard puzzles (20-25 given cells): Varies based on puzzle structure

## Algorithm Explanation

1. **Initial Setup**: Create 81 variables (one per cell) with appropriate domains
2. **AC-3 Preprocessing**: Reduce domains by enforcing arc consistency
3. **Backtracking Search**:
   - Select variable using MRV (fewest remaining values)
   - Try each value in domain
   - Apply forward checking to prune related domains
   - Recursively solve remaining variables
   - Backtrack if dead-end reached

## Constraints

Each Sudoku has 27 AllDifferent constraints:
- 9 row constraints (cells in same row must differ)
- 9 column constraints (cells in same column must differ)
- 9 box constraints (cells in same 3x3 box must differ)

## Troubleshooting

**No solution found for valid puzzle?**
- Verify puzzle is correctly formatted (9x9, values 0-9)
- Check if puzzle is actually solvable
- Some extremely hard puzzles may require extended search time

**Import errors?**
- Ensure you're in the correct directory
- Use Python 3.x (tested with 3.8+)

## Contributing

Feel free to extend the CSP framework for other constraint satisfaction problems!
