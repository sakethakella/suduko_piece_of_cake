"""
CSP (Constraint Satisfaction Problem) Framework

This module provides a general framework for solving constraint satisfaction problems
using backtracking search with various heuristics and constraint propagation techniques.
"""

from typing import List, Dict, Set, Tuple, Optional, Callable
from collections import deque
import copy


class Variable:
    """Represents a variable in a CSP."""
    
    def __init__(self, name: str, domain: List[int]):
        """
        Initialize a CSP variable.
        
        Args:
            name: The name/identifier of the variable
            domain: List of possible values this variable can take
        """
        self.name = name
        self.domain = set(domain)  # Use set for efficient operations
        self.value = None
        
    def __repr__(self):
        return f"Variable({self.name}, domain={self.domain}, value={self.value})"
    
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other):
        return isinstance(other, Variable) and self.name == other.name


class Constraint:
    """Base class for constraints in a CSP."""
    
    def __init__(self, variables: List[Variable]):
        """
        Initialize a constraint.
        
        Args:
            variables: List of variables involved in this constraint
        """
        self.variables = variables
    
    def is_satisfied(self, assignment: Dict[Variable, int]) -> bool:
        """
        Check if the constraint is satisfied given the current assignment.
        
        Args:
            assignment: Dictionary mapping variables to their assigned values
            
        Returns:
            True if constraint is satisfied, False otherwise
        """
        raise NotImplementedError("Subclasses must implement is_satisfied")
    
    def get_related_variables(self, var: Variable) -> List[Variable]:
        """
        Get all variables in this constraint except the given variable.
        
        Args:
            var: The variable to exclude
            
        Returns:
            List of related variables
        """
        return [v for v in self.variables if v != var]


class AllDifferentConstraint(Constraint):
    """Constraint that enforces all variables must have different values."""
    
    def is_satisfied(self, assignment: Dict[Variable, int]) -> bool:
        """Check if all assigned variables have different values."""
        assigned_vars = [v for v in self.variables if v in assignment]
        assigned_values = [assignment[v] for v in assigned_vars]
        return len(assigned_values) == len(set(assigned_values))


class CSP:
    """Constraint Satisfaction Problem solver."""
    
    def __init__(self, variables: List[Variable], constraints: List[Constraint]):
        """
        Initialize a CSP.
        
        Args:
            variables: List of all variables in the problem
            constraints: List of all constraints in the problem
        """
        self.variables = variables
        self.constraints = constraints
        self.var_to_constraints = self._build_var_constraint_map()
        
    def _build_var_constraint_map(self) -> Dict[Variable, List[Constraint]]:
        """Build a mapping from each variable to constraints involving it."""
        var_map = {var: [] for var in self.variables}
        for constraint in self.constraints:
            for var in constraint.variables:
                var_map[var].append(constraint)
        return var_map
    
    def is_consistent(self, var: Variable, value: int, assignment: Dict[Variable, int]) -> bool:
        """
        Check if assigning value to var is consistent with current assignment.
        
        Args:
            var: Variable to check
            value: Value to assign to var
            assignment: Current partial assignment
            
        Returns:
            True if assignment is consistent, False otherwise
        """
        test_assignment = assignment.copy()
        test_assignment[var] = value
        
        for constraint in self.var_to_constraints[var]:
            if not constraint.is_satisfied(test_assignment):
                return False
        return True
    
    def ac3(self, assignment: Dict[Variable, int] = None, 
            domains: Dict[Variable, Set[int]] = None) -> Optional[Dict[Variable, Set[int]]]:
        """
        Apply AC-3 (Arc Consistency 3) algorithm to enforce arc consistency.
        
        Args:
            assignment: Current partial assignment
            domains: Current domains for each variable (if None, uses variable domains)
            
        Returns:
            Updated domains if consistent, None if inconsistency detected
        """
        if assignment is None:
            assignment = {}
        
        if domains is None:
            domains = {var: var.domain.copy() for var in self.variables}
        else:
            domains = {var: domain.copy() for var, domain in domains.items()}
        
        # Initialize queue with all arcs
        queue = deque()
        for constraint in self.constraints:
            for var in constraint.variables:
                if var not in assignment:
                    for other_var in constraint.get_related_variables(var):
                        if other_var not in assignment:
                            queue.append((var, other_var, constraint))
        
        while queue:
            var1, var2, constraint = queue.popleft()
            
            if self._revise(var1, var2, constraint, assignment, domains):
                if len(domains[var1]) == 0:
                    return None  # Inconsistency detected
                
                # Add arcs involving var1 back to queue
                for other_constraint in self.var_to_constraints[var1]:
                    for neighbor in other_constraint.get_related_variables(var1):
                        if neighbor != var2 and neighbor not in assignment:
                            queue.append((neighbor, var1, other_constraint))
        
        return domains
    
    def _revise(self, var1: Variable, var2: Variable, constraint: Constraint,
                assignment: Dict[Variable, int], domains: Dict[Variable, Set[int]]) -> bool:
        """
        Revise the domain of var1 with respect to var2.
        
        Returns:
            True if domain of var1 was revised, False otherwise
        """
        revised = False
        to_remove = set()
        
        for value1 in domains[var1]:
            # Check if there exists a value in var2's domain that satisfies the constraint
            satisfies = False
            test_assignment = assignment.copy()
            test_assignment[var1] = value1
            
            for value2 in domains[var2]:
                test_assignment[var2] = value2
                if constraint.is_satisfied(test_assignment):
                    satisfies = True
                    break
            
            if not satisfies:
                to_remove.add(value1)
                revised = True
        
        domains[var1] -= to_remove
        return revised
    
    def select_unassigned_variable_mrv(self, assignment: Dict[Variable, int],
                                       domains: Dict[Variable, Set[int]]) -> Optional[Variable]:
        """
        Select an unassigned variable using MRV (Minimum Remaining Values) heuristic.
        
        Args:
            assignment: Current partial assignment
            domains: Current domains for each variable
            
        Returns:
            Variable with smallest domain (MRV), or None if all assigned
        """
        unassigned = [v for v in self.variables if v not in assignment]
        if not unassigned:
            return None
        
        # Select variable with smallest domain (MRV)
        return min(unassigned, key=lambda v: len(domains[v]))
    
    def forward_check(self, var: Variable, value: int, assignment: Dict[Variable, int],
                      domains: Dict[Variable, Set[int]]) -> Optional[Dict[Variable, Set[int]]]:
        """
        Perform forward checking after assigning value to var.
        
        Args:
            var: Variable being assigned
            value: Value being assigned to var
            assignment: Current assignment
            domains: Current domains
            
        Returns:
            Updated domains if consistent, None if inconsistency detected
        """
        new_domains = {v: d.copy() for v, d in domains.items()}
        test_assignment = assignment.copy()
        test_assignment[var] = value
        
        # Check all constraints involving var
        for constraint in self.var_to_constraints[var]:
            for other_var in constraint.get_related_variables(var):
                if other_var not in assignment:
                    # Remove inconsistent values from other_var's domain
                    to_remove = set()
                    for other_value in new_domains[other_var]:
                        test_assignment[other_var] = other_value
                        if not constraint.is_satisfied(test_assignment):
                            to_remove.add(other_value)
                    
                    new_domains[other_var] -= to_remove
                    
                    if len(new_domains[other_var]) == 0:
                        return None  # Inconsistency detected
        
        return new_domains
    
    def backtrack(self, assignment: Dict[Variable, int] = None,
                  domains: Dict[Variable, Set[int]] = None) -> Optional[Dict[Variable, int]]:
        """
        Solve CSP using backtracking search with MRV and forward checking.
        
        Args:
            assignment: Current partial assignment
            domains: Current domains for each variable
            
        Returns:
            Complete assignment if solution found, None otherwise
        """
        if assignment is None:
            assignment = {}
        
        if domains is None:
            domains = {var: var.domain.copy() for var in self.variables}
        
        # Check if assignment is complete
        if len(assignment) == len(self.variables):
            return assignment
        
        # Select unassigned variable using MRV
        var = self.select_unassigned_variable_mrv(assignment, domains)
        
        if var is None:
            return assignment
        
        # Try each value in the domain
        for value in sorted(domains[var]):  # Sort for deterministic behavior
            if self.is_consistent(var, value, assignment):
                # Make assignment
                assignment[var] = value
                
                # Perform forward checking
                new_domains = self.forward_check(var, value, assignment, domains)
                
                if new_domains is not None:
                    # Recursively solve
                    result = self.backtrack(assignment, new_domains)
                    if result is not None:
                        return result
                
                # Backtrack
                del assignment[var]
        
        return None
    
    def solve(self) -> Optional[Dict[Variable, int]]:
        """
        Solve the CSP using backtracking with MRV, forward checking, and AC-3.
        
        Returns:
            Complete assignment if solution found, None otherwise
        """
        # First apply AC-3 to reduce domains
        domains = self.ac3()
        if domains is None:
            return None  # Problem is inconsistent
        
        # Solve using backtracking with MRV and forward checking
        return self.backtrack(domains=domains)
