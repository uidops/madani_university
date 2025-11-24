#!/usr/bin/env python3
"""
System of Linear Equations Solver using Cramer's Method

A comprehensive solver for 3x3 systems of linear equations that:
- Parses equations from text input (format: ax + by + cz = w)
- Solves using Cramer's Method with determinants
- Generates detailed markdown reports with step-by-step solutions
- Provides interactive interface and example systems

Author: Expert System Engineer
Method: Cramer's Rule Implementation
"""

import re
import numpy as np
from typing import List, Tuple, Dict


class SystemEquationSolver:
    """
    Complete system equation solver using Cramer's method
    """

    def __init__(self):
        self.equations = []
        self.coefficient_matrix = []
        self.constants = []
        self.variables = ['x', 'y', 'z']
        self.solution = {}
        self.steps = []

    def parse_equation(self, equation_str: str) -> Tuple[List[float], float]:
        """
        Parse equation string in format 'ax + by + cz = w' and extract coefficients

        Args:
            equation_str: String equation like "2x + 3y - z = 5"

        Returns:
            Tuple of (coefficients_list, constant_value)
        """
        # Remove spaces and convert to lowercase
        equation = equation_str.replace(' ', '').lower()

        # Split by equals sign
        left_side, right_side = equation.split('=')
        constant = float(right_side)

        # Initialize coefficients for x, y, z
        coefficients = [0.0, 0.0, 0.0]

        # Add '+' at the beginning if the first character is not '+' or '-'
        if left_side and left_side[0] not in ['+', '-']:
            left_side = '+' + left_side

        # Pattern to match terms like: +2x, -3y, +z, -z, +x, etc.
        pattern = r'([+-])(\d*)([xyz])'
        matches = re.findall(pattern, left_side)

        for sign, coef, var in matches:
            # Handle sign
            sign_multiplier = -1 if sign == '-' else 1

            # Handle coefficient
            if coef == '':
                coef_value = 1.0
            else:
                coef_value = float(coef)

            # Apply sign
            final_coef = sign_multiplier * coef_value

            # Assign to correct position
            var_index = self.variables.index(var)
            coefficients[var_index] = final_coef

        return coefficients, constant

    def input_system(self, equations_list: List[str]):
        """
        Input system of equations as list of strings

        Args:
            equations_list: List of equation strings
        """
        self.equations = equations_list
        self.coefficient_matrix = []
        self.constants = []

        for eq in equations_list:
            coeffs, const = self.parse_equation(eq)
            self.coefficient_matrix.append(coeffs)
            self.constants.append(const)

        self.coefficient_matrix = np.array(self.coefficient_matrix)
        self.constants = np.array(self.constants)

        self.steps.append("## Input System")
        for i, eq in enumerate(equations_list):
            self.steps.append(f"{i+1}. {eq}")
        self.steps.append("")

    def calculate_determinant(self, matrix: np.ndarray) -> float:
        """
        Calculate determinant of 3x3 matrix using cofactor expansion

        Args:
            matrix: 3x3 numpy array

        Returns:
            Determinant value
        """
        if matrix.shape == (3, 3):
            det = (matrix[0, 0] * (matrix[1, 1]*matrix[2, 2] - matrix[1, 2]*matrix[2, 1]) -
                   matrix[0, 1] * (matrix[1, 0]*matrix[2, 2] - matrix[1, 2]*matrix[2, 0]) +
                   matrix[0, 2] * (matrix[1, 0]*matrix[2, 1] - matrix[1, 1]*matrix[2, 0]))
            return det
        else:
            return np.linalg.det(matrix)

    def format_matrix(self, matrix: np.ndarray, name: str = "") -> str:
        """
        Format matrix for markdown display

        Args:
            matrix: Matrix to format
            name: Optional name for the matrix

        Returns:
            Formatted markdown string
        """
        if name:
            result = f"**{name}:**\n\n"
        else:
            result = ""

        # Create proper markdown table
        rows, cols = matrix.shape

        # Header row
        header = "| " + " | ".join([f"Col {i+1}" for i in range(cols)]) + " |"
        separator = "|" + "|".join([" --- " for i in range(cols)]) + "|"

        result += header + "\n"
        result += separator + "\n"

        # Data rows
        for row in matrix:
            row_str = "| " + " | ".join([f"{val: 8.3f}" for val in row]) + " |"
            result += row_str + "\n"

        result += "\n"
        return result

    def solve_cramers_method(self):
        """
        Solve system using Cramer's method
        """
        self.steps.append("## Coefficient Matrix and Constants")
        self.steps.append(self.format_matrix(
            self.coefficient_matrix, "Coefficient Matrix A"))

        # Format constants vector as a proper table
        constants_str = "**Constants Vector b:**\n\n"
        constants_str += "| b₁ | b₂ | b₃ |\n"
        constants_str += "| --- | --- | --- |\n"
        constants_str += f"| {self.constants[0]: .3f} | {
            self.constants[1]: .3f} | {self.constants[2]: .3f} |\n"
        self.steps.append(constants_str)

        # Calculate main determinant
        det_A = self.calculate_determinant(self.coefficient_matrix)
        self.steps.append("## Main Determinant")
        self.steps.append(f"**det(A) = {det_A: .6f}**")
        self.steps.append("")

        if abs(det_A) < 1e-10:
            self.steps.append(
                "**System has no unique solution (determinant ≈ 0)**\n")
            return

        # Calculate determinant for each variable using Cramer's method
        self.steps.append("## Cramer's Method - Variable Solutions")

        for i, var in enumerate(self.variables):
            # Create matrix with i-th column replaced by constants
            temp_matrix = self.coefficient_matrix.copy()
            temp_matrix[:, i] = self.constants

            det_var = self.calculate_determinant(temp_matrix)
            solution_value = det_var / det_A
            self.solution[var] = solution_value

            self.steps.append(f"### For variable {var}: ")
            self.steps.append(self.format_matrix(
                temp_matrix, f"Matrix A_{var}"))
            self.steps.append(f"**det(A_{var}) = {det_var: .6f}**")
            self.steps.append("")
            self.steps.append(
                f"**{var} = det(A_{var}) / det(A) = {det_var: .6f} / {det_A: .6f} = {solution_value: .6f}**")
            self.steps.append("")

    def verify_solution(self):
        """
        Verify the solution by substituting back into original equations
        """
        self.steps.append("## Solution Verification")

        for i, eq in enumerate(self.equations):
            coeffs, constant = self.parse_equation(eq)

            # Calculate left side value
            left_value = sum(
                coeffs[j] * self.solution[self.variables[j]] for j in range(3))

            self.steps.append(f"**Equation {i + 1}:** {eq}")
            substitution = " + ".join([f"({coeffs[j]:.3f} × {self.solution[self.variables[j]]:.6f})"
                                       for j in range(3) if coeffs[j] != 0])
            self.steps.append(
                f"- Left side: {substitution} = {left_value: .6f}")
            self.steps.append(f"- Right side: {constant}")
            self.steps.append(
                f"- Difference: {abs(left_value - constant): .10f}")
            self.steps.append("")

    def generate_report(self, filename: str = "solution_report.md"):
        """
        Generate markdown report with complete solution steps

        Args:
            filename: Output filename for the report
        """
        report_content = [
            "# System of Linear Equations - Cramer's Method Solution",
            "",
            f"**Solution Summary:**",
            ""
        ]

        # Add solution summary
        for var in self.variables:
            if var in self.solution:
                report_content.append(
                    f"- **{var} = {self.solution[var]: .6f}**")

        report_content.extend(["", "---", ""])
        report_content.extend(self.steps)

        # Write to file
        with open(filename, 'w') as f:
            f.write('\n'.join(report_content))

        print(f"Solution report generated: {filename}")

    def solve_system(self, equations_list: List[str], output_file: str = "solution_report.md"):
        """
        Main method to solve system and generate report

        Args:
            equations_list: List of equation strings
            output_file: Output filename for detailed report

        Returns:
            Dictionary with solution values
        """
        self.input_system(equations_list)
        self.solve_cramers_method()
        self.verify_solution()
        self.generate_report(output_file)

        return self.solution


def run_example_systems():
    """
    Run example systems to demonstrate the solver
    """
    print("SYSTEM OF LINEAR EQUATIONS SOLVER - EXAMPLES")
    print("=" * 60)
    print("Using Cramer's Method for solving 3x3 systems")
    print("Format: ax + by + cz = w")
    print()

    examples = [
        {
            "name": "Example 1: Simple Symmetric System",
            "equations": [
                "2x + y + z = 6",
                "x + 2y + z = 6",
                "x + y + 2z = 6"
            ],
            "filename": "example1_solution.md"
        },
        {
            "name": "Example 2: Mixed Coefficients",
            "equations": [
                "x + 2y + 3z = 14",
                "2x + y + 2z = 10",
                "3x + 2y + z = 10"
            ],
            "filename": "example2_solution.md"
        },
        {
            "name": "Example 3: Production Planning Problem",
            "equations": [
                "2x + 3y + z = 95",
                "x + 2y + 3z = 115",
                "4x + y + 2z = 108"
            ],
            "filename": "production_optimization.md"
        }
    ]

    for example in examples:
        print(f"{example['name']}")
        print("=" * 40)

        solver = SystemEquationSolver()
        solution = solver.solve_system(
            example['equations'], example['filename'])

        print("System:")
        for eq in example['equations']:
            print(f"  {eq}")

        print("\nSolution:")
        for var, value in solution.items():
            print(f"  {var} = {value: .6f}")

        print(f"\nDetailed report: {example['filename']}")
        print()


def run_interactive():
    """
    Interactive mode for user input
    """
    print("INTERACTIVE SYSTEM EQUATION SOLVER")
    print("=" * 50)
    print("Enter equations in format: ax + by + cz = w")
    print("Example: 2x + 3y - z = 1")
    print("Enter 3 equations (press Enter after each):\n")

    equations = []
    for i in range(3):
        while True:
            try:
                eq = input(f"Equation {i+1}: ").strip()
                if not eq:
                    print("Please enter an equation.")
                    continue
                if '=' not in eq:
                    print("Equation must contain an equals sign (=).")
                    continue

                # Test parse the equation
                solver = SystemEquationSolver()
                solver.parse_equation(eq)
                equations.append(eq)
                break

            except Exception as e:
                print(f"Error parsing equation: {e}")
                print("Please check the format and try again.")

    print("\nSolving system...")
    solver = SystemEquationSolver()
    solution = solver.solve_system(equations)

    print("\nSolution:")
    for var, value in solution.items():
        print(f"{var} = {value: .6f}")

    print(f"\nDetailed report saved to: solution_report.md")


def main():
    """
    Main entry point with menu system
    """
    print("SYSTEM OF LINEAR EQUATIONS SOLVER")
    print("Using Cramer's Method for 3x3 systems")
    print("=" * 50)
    print()
    print("Choose an option:")
    print("1. Run example systems")
    print("2. Interactive mode (enter your own equations)")
    print("3. Exit")
    print()

    try:
        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            run_example_systems()
        elif choice == '2':
            run_interactive()
        elif choice == '3':
            print("Goodbye!")
            return
        else:
            print("Invalid choice. Running examples...")
            run_example_systems()

    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Check dependencies
    try:
        import numpy as np
        main()
    except ImportError:
        print("Error: numpy is required. Install with: pip install numpy")
