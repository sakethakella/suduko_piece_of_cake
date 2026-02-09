"""
Example demonstrating the CSP Sudoku Solver capabilities

This example shows:
1. How the CSP framework models Sudoku
2. Step-by-step solving of different difficulty levels
3. Validation of solutions
"""

from sudoku_solver import SudokuSolver


def demonstrate_sudoku_solver():
    """Demonstrate the Sudoku solver with various examples."""
    
    print("="*70)
    print(" CSP-based Sudoku Solver Demonstration")
    print("="*70)
    print()
    print("This solver uses advanced CSP techniques:")
    print("  • Backtracking search")
    print("  • MRV (Minimum Remaining Values) heuristic")
    print("  • Forward checking for early pruning")
    print("  • AC-3 (Arc Consistency 3) algorithm")
    print()
    print("="*70)
    print()
    
    # Example 1: Nearly solved puzzle
    print("Example 1: Nearly Solved Puzzle")
    print("-" * 70)
    nearly_solved = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 0]  # Only missing last cell
    ]
    
    print("\nPuzzle (only 1 cell missing):")
    SudokuSolver.print_grid(nearly_solved)
    
    solver = SudokuSolver(nearly_solved)
    solution = solver.solve()
    
    print("\nSolution:")
    SudokuSolver.print_grid(solution)
    print(f"\n{'✓ Valid!' if SudokuSolver.is_valid_solution(solution) else '✗ Invalid!'}")
    
    # Example 2: Easy puzzle
    print("\n" + "="*70)
    print("\nExample 2: Easy Puzzle")
    print("-" * 70)
    easy = [
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
    
    empty_cells = sum(row.count(0) for row in easy)
    print(f"\nPuzzle (with {empty_cells} empty cells):")
    SudokuSolver.print_grid(easy)
    
    solver = SudokuSolver(easy)
    solution = solver.solve()
    
    print("\nSolution:")
    SudokuSolver.print_grid(solution)
    print(f"\n{'✓ Valid!' if SudokuSolver.is_valid_solution(solution) else '✗ Invalid!'}")
    
    # Example 3: Medium puzzle
    print("\n" + "="*70)
    print("\nExample 3: Medium Puzzle")
    print("-" * 70)
    medium = [
        [0, 0, 0, 2, 6, 0, 7, 0, 1],
        [6, 8, 0, 0, 7, 0, 0, 9, 0],
        [1, 9, 0, 0, 0, 4, 5, 0, 0],
        [8, 2, 0, 1, 0, 0, 0, 4, 0],
        [0, 0, 4, 6, 0, 2, 9, 0, 0],
        [0, 5, 0, 0, 0, 3, 0, 2, 8],
        [0, 0, 9, 3, 0, 0, 0, 7, 4],
        [0, 4, 0, 0, 5, 0, 0, 3, 6],
        [7, 0, 3, 0, 1, 8, 0, 0, 0]
    ]
    
    empty_cells = sum(row.count(0) for row in medium)
    print(f"\nPuzzle (with {empty_cells} empty cells):")
    SudokuSolver.print_grid(medium)
    
    solver = SudokuSolver(medium)
    solution = solver.solve()
    
    print("\nSolution:")
    SudokuSolver.print_grid(solution)
    print(f"\n{'✓ Valid!' if SudokuSolver.is_valid_solution(solution) else '✗ Invalid!'}")
    
    # Example 4: Demonstrating CSP concepts
    print("\n" + "="*70)
    print("\nCSP Model for Sudoku:")
    print("-" * 70)
    print("""
Variables (xij): 
  • Each cell (i,j) is a variable, i.e., x00, x01, ..., x88
  • Total: 81 variables

Domain:
  • For empty cells: {1, 2, 3, 4, 5, 6, 7, 8, 9}
  • For filled cells: {given_value}

Constraints (27 total):
  • 9 Row constraints: AllDifferent for each row
  • 9 Column constraints: AllDifferent for each column  
  • 9 Box constraints: AllDifferent for each 3×3 box

Solving Strategy:
  1. Apply AC-3 to reduce initial domains
  2. Select variable using MRV (smallest domain)
  3. Try values and use forward checking
  4. Backtrack if dead-end is reached
    """)
    
    print("="*70)
    print("\nDemonstration complete!")
    print("="*70)


if __name__ == "__main__":
    demonstrate_sudoku_solver()
