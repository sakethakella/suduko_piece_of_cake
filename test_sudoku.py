"""
Unit tests for Sudoku Solver and CSP Framework
"""

import unittest
from csp import Variable, AllDifferentConstraint, CSP
from sudoku_solver import SudokuSolver


class TestCSPFramework(unittest.TestCase):
    """Test cases for the CSP framework."""
    
    def test_variable_creation(self):
        """Test creating a CSP variable."""
        var = Variable("x1", [1, 2, 3, 4])
        self.assertEqual(var.name, "x1")
        self.assertEqual(var.domain, {1, 2, 3, 4})
        self.assertIsNone(var.value)
    
    def test_all_different_constraint(self):
        """Test AllDifferentConstraint."""
        var1 = Variable("x1", [1, 2, 3])
        var2 = Variable("x2", [1, 2, 3])
        var3 = Variable("x3", [1, 2, 3])
        
        constraint = AllDifferentConstraint([var1, var2, var3])
        
        # Test satisfied constraint
        assignment = {var1: 1, var2: 2, var3: 3}
        self.assertTrue(constraint.is_satisfied(assignment))
        
        # Test violated constraint
        assignment = {var1: 1, var2: 1, var3: 3}
        self.assertFalse(constraint.is_satisfied(assignment))
        
        # Test partial assignment (should be satisfied)
        assignment = {var1: 1, var2: 2}
        self.assertTrue(constraint.is_satisfied(assignment))
    
    def test_simple_csp(self):
        """Test solving a simple CSP."""
        # Create a simple problem: two variables with all-different constraint
        var1 = Variable("x1", [1, 2])
        var2 = Variable("x2", [1, 2])
        
        constraint = AllDifferentConstraint([var1, var2])
        csp = CSP([var1, var2], [constraint])
        
        solution = csp.solve()
        self.assertIsNotNone(solution)
        self.assertNotEqual(solution[var1], solution[var2])
    
    def test_ac3(self):
        """Test AC-3 algorithm."""
        var1 = Variable("x1", [1, 2, 3])
        var2 = Variable("x2", [2, 3])
        
        constraint = AllDifferentConstraint([var1, var2])
        csp = CSP([var1, var2], [constraint])
        
        domains = csp.ac3()
        self.assertIsNotNone(domains)


class TestSudokuSolver(unittest.TestCase):
    """Test cases for the Sudoku solver."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Very simple puzzle for testing
        self.simple_puzzle = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 0]  # Missing one value
        ]
        
        # Standard easy puzzle
        self.easy_puzzle = [
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
    
    def test_solver_initialization(self):
        """Test Sudoku solver initialization."""
        solver = SudokuSolver(self.easy_puzzle)
        self.assertEqual(len(solver.variables), 81)
        self.assertEqual(len(solver.constraints), 27)  # 9 rows + 9 cols + 9 boxes
    
    def test_simple_puzzle(self):
        """Test solving a nearly complete puzzle."""
        solver = SudokuSolver(self.simple_puzzle)
        solution = solver.solve()
        
        self.assertIsNotNone(solution)
        self.assertTrue(SudokuSolver.is_valid_solution(solution))
        self.assertEqual(solution[8][8], 9)  # The missing value
    
    def test_easy_puzzle(self):
        """Test solving an easy puzzle."""
        solver = SudokuSolver(self.easy_puzzle)
        solution = solver.solve()
        
        self.assertIsNotNone(solution)
        self.assertTrue(SudokuSolver.is_valid_solution(solution))
    
    def test_invalid_solution_detection(self):
        """Test that invalid solutions are detected."""
        # Invalid solution (duplicate in row)
        invalid_grid = [
            [1, 1, 3, 4, 5, 6, 7, 8, 9],
            [4, 5, 6, 7, 8, 9, 1, 2, 3],
            [7, 8, 9, 1, 2, 3, 4, 5, 6],
            [2, 3, 1, 5, 6, 4, 8, 9, 7],
            [5, 6, 4, 8, 9, 7, 2, 3, 1],
            [8, 9, 7, 2, 3, 1, 5, 6, 4],
            [3, 1, 2, 6, 4, 5, 9, 7, 8],
            [6, 4, 5, 9, 7, 8, 3, 1, 2],
            [9, 7, 8, 3, 1, 2, 6, 4, 5]
        ]
        
        self.assertFalse(SudokuSolver.is_valid_solution(invalid_grid))
    
    def test_no_solution_puzzle(self):
        """Test puzzle with no solution."""
        # Impossible puzzle (two 5s in first row)
        impossible_puzzle = [
            [5, 5, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        
        solver = SudokuSolver(impossible_puzzle)
        solution = solver.solve()
        
        self.assertIsNone(solution)


class TestCSPTechniques(unittest.TestCase):
    """Test specific CSP techniques used in the solver."""
    
    def test_mrv_heuristic(self):
        """Test that MRV heuristic selects variable with smallest domain."""
        var1 = Variable("x1", [1, 2, 3, 4, 5])
        var2 = Variable("x2", [1, 2])  # Smallest domain
        var3 = Variable("x3", [1, 2, 3])
        
        csp = CSP([var1, var2, var3], [])
        domains = {var1: {1, 2, 3, 4, 5}, var2: {1, 2}, var3: {1, 2, 3}}
        
        selected = csp.select_unassigned_variable_mrv({}, domains)
        self.assertEqual(selected, var2)
    
    def test_forward_checking(self):
        """Test forward checking reduces domains correctly."""
        var1 = Variable("x1", [1, 2, 3])
        var2 = Variable("x2", [1, 2, 3])
        
        constraint = AllDifferentConstraint([var1, var2])
        csp = CSP([var1, var2], [constraint])
        
        domains = {var1: {1, 2, 3}, var2: {1, 2, 3}}
        assignment = {}
        
        # Assign 1 to var1
        new_domains = csp.forward_check(var1, 1, assignment, domains)
        
        # var2 should no longer have 1 in its domain
        self.assertIsNotNone(new_domains)
        self.assertNotIn(1, new_domains[var2])
        self.assertIn(2, new_domains[var2])
        self.assertIn(3, new_domains[var2])


if __name__ == '__main__':
    unittest.main()
