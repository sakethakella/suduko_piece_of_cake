"""
Sudoku Solver using CSP Framework

This module implements a Sudoku solver using the CSP framework with:
- Backtracking search
- MRV (Minimum Remaining Values) heuristic
- Forward checking
- AC-3 (Arc Consistency 3) constraint propagation
"""

from typing import List, Dict, Optional, Tuple
from csp import Variable, Constraint, AllDifferentConstraint, CSP


class SudokuSolver:
    """Sudoku solver using CSP techniques."""
    
    def __init__(self, grid: List[List[int]]):
        """
        Initialize Sudoku solver with a 9x9 grid.
        
        Args:
            grid: 9x9 list representing the Sudoku puzzle.
                  0 represents empty cells, 1-9 represent filled cells.
        """
        self.size = 9
        self.box_size = 3
        self.grid = grid
        self.variables = {}
        self.constraints = []
        self._setup_csp()
    
    def _setup_csp(self):
        """Set up the CSP problem with variables and constraints."""
        # Create variables for each cell (i, j)
        for i in range(self.size):
            for j in range(self.size):
                var_name = f"x{i}{j}"
                
                # If cell is filled, domain is just that value
                # Otherwise, domain is 1-9
                if self.grid[i][j] != 0:
                    domain = [self.grid[i][j]]
                else:
                    domain = list(range(1, self.size + 1))
                
                var = Variable(var_name, domain)
                self.variables[(i, j)] = var
        
        # Add row constraints (all different in each row)
        for i in range(self.size):
            row_vars = [self.variables[(i, j)] for j in range(self.size)]
            self.constraints.append(AllDifferentConstraint(row_vars))
        
        # Add column constraints (all different in each column)
        for j in range(self.size):
            col_vars = [self.variables[(i, j)] for i in range(self.size)]
            self.constraints.append(AllDifferentConstraint(col_vars))
        
        # Add 3x3 box constraints (all different in each 3x3 box)
        for box_row in range(self.box_size):
            for box_col in range(self.box_size):
                box_vars = []
                for i in range(box_row * self.box_size, (box_row + 1) * self.box_size):
                    for j in range(box_col * self.box_size, (box_col + 1) * self.box_size):
                        box_vars.append(self.variables[(i, j)])
                self.constraints.append(AllDifferentConstraint(box_vars))
    
    def solve(self) -> Optional[List[List[int]]]:
        """
        Solve the Sudoku puzzle.
        
        Returns:
            Solved 9x9 grid if solution exists, None otherwise
        """
        # Create CSP with all variables and constraints
        all_vars = [self.variables[(i, j)] for i in range(self.size) 
                    for j in range(self.size)]
        csp = CSP(all_vars, self.constraints)
        
        # Solve using CSP backtracking with MRV, forward checking, and AC-3
        solution = csp.solve()
        
        if solution is None:
            return None
        
        # Convert solution to grid format
        result = [[0] * self.size for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                var = self.variables[(i, j)]
                result[i][j] = solution[var]
        
        return result
    
    @staticmethod
    def print_grid(grid: List[List[int]]):
        """Print a Sudoku grid in a readable format."""
        if grid is None:
            print("No solution found!")
            return
        
        print("╔═══════╤═══════╤═══════╗")
        for i in range(9):
            if i == 3 or i == 6:
                print("╟───────┼───────┼───────╢")
            
            row_str = "║ "
            for j in range(9):
                if j == 3 or j == 6:
                    row_str += "│ "
                row_str += str(grid[i][j]) + " "
            row_str += "║"
            print(row_str)
        print("╚═══════╧═══════╧═══════╝")
    
    @staticmethod
    def is_valid_solution(grid: List[List[int]]) -> bool:
        """Verify if a Sudoku solution is valid."""
        if grid is None:
            return False
        
        size = 9
        
        # Check rows
        for i in range(size):
            if len(set(grid[i])) != size or min(grid[i]) < 1 or max(grid[i]) > 9:
                return False
        
        # Check columns
        for j in range(size):
            col = [grid[i][j] for i in range(size)]
            if len(set(col)) != size or min(col) < 1 or max(col) > 9:
                return False
        
        # Check 3x3 boxes
        for box_row in range(3):
            for box_col in range(3):
                box = []
                for i in range(box_row * 3, (box_row + 1) * 3):
                    for j in range(box_col * 3, (box_col + 1) * 3):
                        box.append(grid[i][j])
                if len(set(box)) != size or min(box) < 1 or max(box) > 9:
                    return False
        
        return True


def main():
    """Example usage of the Sudoku solver."""
    
    # Example easy puzzle
    easy_puzzle = [
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
    
    print("Original Sudoku Puzzle:")
    SudokuSolver.print_grid(easy_puzzle)
    print()
    
    solver = SudokuSolver(easy_puzzle)
    solution = solver.solve()
    
    print("Solved Sudoku:")
    SudokuSolver.print_grid(solution)
    print()
    
    if SudokuSolver.is_valid_solution(solution):
        print("✓ Solution is valid!")
    else:
        print("✗ Solution is invalid!")
    
    print("\n" + "="*50 + "\n")
    
    # Example hard puzzle
    hard_puzzle = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 8, 5],
        [0, 0, 1, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 5, 0, 7, 0, 0, 0],
        [0, 0, 4, 0, 0, 0, 1, 0, 0],
        [0, 9, 0, 0, 0, 0, 0, 0, 0],
        [5, 0, 0, 0, 0, 0, 0, 7, 3],
        [0, 0, 2, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 9]
    ]
    
    print("Hard Sudoku Puzzle:")
    SudokuSolver.print_grid(hard_puzzle)
    print()
    
    solver = SudokuSolver(hard_puzzle)
    solution = solver.solve()
    
    print("Solved Hard Sudoku:")
    SudokuSolver.print_grid(solution)
    print()
    
    if SudokuSolver.is_valid_solution(solution):
        print("✓ Solution is valid!")
    else:
        print("✗ Solution is invalid!")


if __name__ == "__main__":
    main()
