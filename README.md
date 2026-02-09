# Sudoku Solver - Piece of Cake! 🍰

A sophisticated Sudoku solver using Constraint Satisfaction Problem (CSP) techniques with advanced algorithms for efficient solving.

## Features

This implementation includes:

- **CSP Framework**: A general-purpose CSP solver that can be applied to various constraint satisfaction problems
- **Backtracking Search**: Intelligent backtracking algorithm with pruning
- **MRV Heuristic**: Minimum Remaining Values heuristic for smart variable selection
- **Forward Checking**: Proactive domain reduction to detect dead-ends early
- **AC-3 Algorithm**: Arc Consistency 3 for constraint propagation and domain reduction

## How It Works

### CSP Model for Sudoku

- **Variables**: Each cell (i,j) in the 9x9 grid is a variable `xij`
- **Domain**: Each variable can take values from 1 to 9
- **Constraints**: 
  - All values in each row must be different (9 constraints)
  - All values in each column must be different (9 constraints)
  - All values in each 3x3 box must be different (9 constraints)
  - Total: 27 AllDifferent constraints

### Solving Algorithm

1. **Initial Setup**: Create variables and constraints based on the puzzle
2. **AC-3 Preprocessing**: Apply Arc Consistency to reduce initial domains
3. **Backtracking Search with**:
   - **MRV**: Select the variable with the fewest remaining values
   - **Forward Checking**: After each assignment, prune inconsistent values from related variables
   - **Backtrack**: If a dead-end is reached, undo the assignment and try another value

## Usage

### Basic Example

```python
from sudoku_solver import SudokuSolver

# Define your puzzle (0 represents empty cells)
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

# Create solver and solve
solver = SudokuSolver(puzzle)
solution = solver.solve()

# Print the solution
SudokuSolver.print_grid(solution)

# Verify solution is valid
if SudokuSolver.is_valid_solution(solution):
    print("✓ Solution is valid!")
```

### Running the Demo

```bash
python3 sudoku_solver.py
```

This will solve example puzzles and display the results.

### Running Tests

```bash
python3 test_sudoku.py -v
```

## File Structure

- `csp.py`: General CSP framework with Variable, Constraint, and CSP classes
- `sudoku_solver.py`: Sudoku-specific implementation using the CSP framework
- `test_sudoku.py`: Comprehensive unit tests for both CSP framework and Sudoku solver

## CSP Framework

The CSP framework is general-purpose and can be used for other constraint satisfaction problems beyond Sudoku. Key components:

### Classes

- **Variable**: Represents a CSP variable with a name and domain
- **Constraint**: Base class for constraints (implement `is_satisfied()`)
- **AllDifferentConstraint**: Constraint ensuring all variables have different values
- **CSP**: Main solver class with backtracking, MRV, AC-3, and forward checking

### Example: Using CSP for Other Problems

```python
from csp import Variable, AllDifferentConstraint, CSP

# Create variables
var1 = Variable("x1", [1, 2, 3])
var2 = Variable("x2", [1, 2, 3])
var3 = Variable("x3", [1, 2, 3])

# Add constraints
constraint = AllDifferentConstraint([var1, var2, var3])

# Create and solve CSP
csp = CSP([var1, var2, var3], [constraint])
solution = csp.solve()

print(solution)  # {var1: 1, var2: 2, var3: 3} (or another valid assignment)
```

## Technical Details

### Complexity

- **Time Complexity**: O(d^n) in worst case where d is domain size (9) and n is number of variables (81)
- **Space Complexity**: O(n) for the recursion stack

### Optimizations

- **AC-3 Preprocessing**: Reduces initial search space
- **MRV Heuristic**: Chooses variables most likely to fail early
- **Forward Checking**: Detects failures before they occur
- **Domain Reduction**: Continuously prunes impossible values

## License

Open source - feel free to use and modify!
