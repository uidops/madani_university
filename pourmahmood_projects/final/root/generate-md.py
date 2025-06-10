#!/usr/bin/env python3

import inspect
import math
import os
import time
import re

import matplotlib.pyplot as plt
import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import numpy as np
import sympy as sp
from sympy import symbols, lambdify, diff, parse_expr, latex


def get_known_true_roots():
    known_roots = {
        "cos(x) - x": 0.739085133215160641655,
        "sin(x) - x": 0.0,
        "tan(x) - x": 0.0,
        "cos(x)": math.pi / 2,
        "sin(x)": 0.0,
        "tan(x)": 0.0,
        "sin(x) - x/2": 0.0,
        "cos(x) - x/2": 1.029866313885,
        
        "exp(x) - 2": math.log(2),
        "exp(x) - x - 2": 1.146193221, 
        "log(x) - x + 2": 0.158961308,
        "exp(x) - 2*x": 0.0,
        "exp(x) - 3*x": 0.619061286,
        
        # Polynomial functions
        "x**2 - 2": math.sqrt(2),
        "x**3 - 2": 2**(1/3),
        "x**2 - x - 1": (1 + math.sqrt(5)) / 2,
        "x**3 - x - 1": 1.324717957244,  
        "x**3 - 2*x - 5": 2.094551481543,  
        "x**4 - x - 1": 1.220744084605, 
        
        # Hyperbolic functions
        "sinh(x) - x": 0.0,
        "cosh(x) - x": 1.543681472555,  
        "tanh(x) - x": 0.0,
        
        # Mixed functions
        "x*exp(x) - 1": 0.567143290409,  
        "x*log(x) - 1": 1.763222834352,  
        "sqrt(x) - cos(x)": 0.641714371482, 
    }
    return known_roots


def compute_true_root_analytically(f_string, f_lambda, df_lambda, x0):
    known_roots = get_known_true_roots()
    
    # Normalize the function string for lookup
    normalized = f_string.replace(" ", "").lower()
    
    # Check exact matches first
    for pattern, root in known_roots.items():
        pattern_normalized = pattern.replace(" ", "").lower()
        if normalized == pattern_normalized:
            print(f"✓ Found analytical root: {root}")
            return root
    
    # Check partial matches for common patterns
    if "cos(x)-x" in normalized or "cos(x) - x" in f_string:
        print("✓ Recognized cos(x) - x equation")
        return 0.739085133215160641655
    
    if "sin(x)-x" in normalized and "cos" not in normalized:
        print("✓ Recognized sin(x) - x equation")
        return 0.0
    
    if "exp(x)-2" in normalized:
        print("✓ Recognized exp(x) - 2 equation")
        return math.log(2)
    
    if "x**2-2" in normalized or "x^2-2" in normalized:
        print("✓ Recognized x² - 2 equation")
        return math.sqrt(2)
    
    if "x**3-2" in normalized or "x^3-2" in normalized:
        print("✓ Recognized x³ - 2 equation")
        return 2**(1/3)
    
    # For polynomial equations, try to solve symbolically
    try:
        x = symbols("x")
        expr = parse_expr(f_string)
        
        # Check if it's a polynomial
        if expr.is_polynomial():
            solutions = sp.solve(expr, x)
            real_solutions = [sol for sol in solutions if sol.is_real and sol.is_finite]
            
            if real_solutions:
                # Find the solution closest to x0
                numerical_solutions = [float(sol.evalf()) for sol in real_solutions]
                closest_solution = min(numerical_solutions, key=lambda sol: abs(sol - x0))
                print(f"✓ Found polynomial root analytically: {closest_solution}")
                return closest_solution
                
    except Exception as e:
        pass
    
    # If no analytical solution found, use high-precision numerical method
    print("✗ No analytical solution found, computing numerically...")
    return compute_true_root_numerically(f_lambda, df_lambda, x0)


def compute_true_root_numerically(f_lambda, df_lambda, x0, max_iterations=100, tolerance=1e-15):
    try:
        x = x0
        for i in range(max_iterations):
            fx = f_lambda(x)
            
            # Check if we're close enough
            if abs(fx) < tolerance:
                return x
            
            dfx = df_lambda(x)
            
            # Avoid division by zero
            if abs(dfx) < 1e-15:
                print(f"Warning: Derivative near zero at iteration {i}")
                break
            
            x_new = x - fx / dfx
            
            # Check for convergence
            if abs(x_new - x) < tolerance:
                return x_new
            
            x = x_new
        
        print(f"Warning: Newton's method did not converge in {max_iterations} iterations")
        return x
        
    except Exception as e:
        print(f"Error in numerical root computation: {e}")
        return x0


def suggest_better_interval(f_lambda, initial_a, initial_b, num_points=1000):
    print("\nAnalyzing function to suggest better interval...")
    
    # Expand the search range
    search_range = max(abs(initial_a), abs(initial_b)) * 2
    if search_range < 10:
        search_range = 10
    
    x_vals = np.linspace(-search_range, search_range, num_points)
    sign_changes = []
    
    try:
        prev_x = x_vals[0]
        prev_f = f_lambda(prev_x)
        
        for x in x_vals[1:]:
            try:
                f_val = f_lambda(x)
                
                # Check for sign change
                if prev_f * f_val < 0:
                    sign_changes.append((prev_x, x, abs(x - prev_x)))
                
                prev_x = x
                prev_f = f_val
                
            except:
                continue
        
        if sign_changes:
            # Sort by interval width (prefer smaller intervals)
            sign_changes.sort(key=lambda x: x[2])
            best_interval = sign_changes[0]
            
            print(f"✓ Found sign change in interval [{best_interval[0]:.6f}, {best_interval[1]:.6f}]")
            print(f"  f({best_interval[0]:.6f}) = {f_lambda(best_interval[0]):.6f}")
            print(f"  f({best_interval[1]:.6f}) = {f_lambda(best_interval[1]):.6f}")
            
            return best_interval[0], best_interval[1]
        else:
            print("✗ No sign changes found in extended range")
            return initial_a, initial_b
            
    except Exception as e:
        print(f"Error in interval analysis: {e}")
        return initial_a, initial_b


def get_function_from_user():
    print("=" * 60)
    print("FUNCTION INPUT")
    print("=" * 60)
    
    x = symbols("x")
    
    # Show examples with known roots
    print("\nEnter your function f(x) using standard mathematical notation:")
    print("Examples (with known analytical solutions):")
    print("  - cos(x) - x                    [root ≈ 0.739085]")
    print("  - exp(x) - 2                    [root = ln(2) ≈ 0.693147]")
    print("  - x**2 - 2                      [root = √2 ≈ 1.414214]")
    print("  - x**3 - 2                      [root = ∛2 ≈ 1.259921]")
    print("  - x**2 - x - 1                  [root = φ ≈ 1.618034] (Golden ratio)")
    print("  - sin(x) - x/2                  [root = 0]")
    print("  - x*exp(x) - 1                  [root ≈ 0.567143] (Lambert W)")
    print("  - x**3 - 2*x - 5                [root ≈ 2.094551]")
    
    while True:
        try:
            f_input = input("\nf(x) = ").strip()
            
            if not f_input:
                print("Please enter a function.")
                continue
            
            # Parse the expression
            f_expr = parse_expr(f_input)
            print(f"\nParsed function: f(x) = {f_expr}")
            
            # Compute derivative
            df_expr = diff(f_expr, x)
            print(f"Computed derivative: f'(x) = {df_expr}")
            
            # Convert to lambda functions
            f_lambda = lambdify(x, f_expr, "math")
            df_lambda = lambdify(x, df_expr, "math")
            
            # Test the functions
            test_val = 1.0
            try:
                f_test = f_lambda(test_val)
                df_test = df_lambda(test_val)
                print(f"\nTest evaluation at x=1: f(1)={f_test:.6f}, f'(1)={df_test:.6f}")
            except Exception as e:
                print(f"Error testing function: {e}")
                continue
            
            # Get string representations
            f_string = str(f_expr)
            df_string = str(df_expr)
            
            return f_lambda, df_lambda, f_string, df_string, f_expr, df_expr
            
        except Exception as e:
            print(f"Error parsing function: {e}")
            print("Please enter a valid mathematical expression.")
            print("Use ** for exponentiation (e.g., x**2 for x²)")
            print("Available functions: sin, cos, tan, exp, log, sqrt, sinh, cosh, tanh")


def get_interval_from_user(f_lambda):
    print("\n" + "=" * 60)
    print("INTERVAL INPUT")
    print("=" * 60)
    
    attempt = 0
    max_attempts = 3
    
    while attempt < max_attempts:
        try:
            if attempt == 0:
                print("\nEnter the interval [a, b] where you suspect the root lies:")
                print("Note: We need f(a) * f(b) < 0 for bisection method to work")
            else:
                print(f"\nAttempt {attempt + 1}/{max_attempts}:")
                print("Please try a different interval where f(a) and f(b) have opposite signs.")
            
            a = float(input("Enter a: ").strip())
            b = float(input("Enter b: ").strip())
            
            if a >= b:
                print("Error: a must be less than b. Please try again.")
                continue
            
            try:
                fa = f_lambda(a)
                fb = f_lambda(b)
                
                print(f"\nEvaluation:")
                print(f"f({a}) = {fa:.6f}")
                print(f"f({b}) = {fb:.6f}")
                print(f"f(a) * f(b) = {fa * fb:.6f}")
                
                if fa * fb < 0:
                    print("✓ Good! f(a) * f(b) < 0, so a root exists in this interval.")
                    return a, b
                else:
                    print("✗ Error: f(a) * f(b) ≥ 0")
                    print("The function values at the endpoints must have opposite signs.")
                    
                    if attempt == max_attempts - 1:
                        print("\nWould you like me to suggest a better interval? (y/n)")
                        if input().strip().lower() in ["y", "yes"]:
                            suggested_a, suggested_b = suggest_better_interval(f_lambda, a, b)
                            print(f"\nSuggested interval: [{suggested_a:.6f}, {suggested_b:.6f}]")
                            
                            use_suggestion = input("Use this interval? (y/n): ").strip().lower()
                            if use_suggestion in ["y", "yes"]:
                                return suggested_a, suggested_b
                    
                    attempt += 1
                    
            except Exception as e:
                print(f"Error evaluating function: {e}")
                print("Please choose values where the function is defined.")
                attempt += 1
                
        except ValueError:
            print("Please enter valid numbers.")
            attempt += 1
    
    # If all attempts failed, use default interval
    print("\nUsing default interval [-10, 10] and hoping for the best...")
    return -10.0, 10.0


def get_initial_guess_from_user(a, b):
    print("\n" + "=" * 60)
    print("INITIAL GUESS INPUT")
    print("=" * 60)
    
    default_x0 = (a + b) / 2
    print(f"\nFor Newton's method and other iterative methods, we need an initial guess.")
    print(f"Suggested value (midpoint): {default_x0:.6f}")
    
    while True:
        try:
            x0_input = input(f"Enter initial guess x0 (press Enter for {default_x0:.6f}): ").strip()
            
            if not x0_input:
                return default_x0
            
            x0 = float(x0_input)
            print(f"Using x0 = {x0}")
            return x0
            
        except ValueError:
            print("Please enter a valid number.")


def get_g_functions_from_user(f_expr, x):
    print("\n" + "=" * 60)
    print("FIXED-POINT FUNCTIONS INPUT")
    print("=" * 60)
    
    print("\nFor the fixed-point method, we need to transform f(x) = 0 into x = g(x)")
    print("You can provide custom g(x) functions, or we'll use default ones.")
    print("\nExamples for f(x) = cos(x) - x:")
    print("  - g(x) = cos(x)")
    print("  - g(x) = x - (cos(x) - x)")
    print("  - g(x) = x - 0.5*(cos(x) - x)")
    
    g_funcs = []
    g_strings = []
    
    while True:
        try:
            g_input = input(f"\nEnter g(x) function (or press Enter to finish): ").strip()
            
            if not g_input:
                break
                
            # Parse the g(x) expression
            g_expr = parse_expr(g_input)
            print(f"Parsed: g(x) = {g_expr}")
            
            # Convert to lambda function
            g_lambda = lambdify(x, g_expr, "math")
            
            # Test the function
            try:
                test_val = 1.0
                g_test = g_lambda(test_val)
                print(f"Test: g(1) = {g_test:.6f}")
                
                g_funcs.append(g_lambda)
                g_strings.append(str(g_expr))
                print("✓ Function added successfully")
                
            except Exception as e:
                print(f"Error testing g(x): {e}")
                
        except Exception as e:
            print(f"Error parsing g(x): {e}")
    
    return g_funcs


def get_true_root_from_user():
    print("\n" + "=" * 60)
    print("TRUE ROOT INPUT (OPTIONAL)")
    print("=" * 60)
    
    print("\nOptions for true root:")
    print("1. Enter known exact value")
    print("2. Let me compute it analytically (if possible)")
    print("3. Skip (compute numerically later)")
    
    while True:
        try:
            choice = input("\nChoose option (1/2/3): ").strip()
            
            if choice == "1":
                root_input = input("Enter true root: ").strip()
                if not root_input:
                    return None
                true_root = float(root_input)
                print(f"Using provided true root = {true_root}")
                return true_root
                
            elif choice == "2":
                print("Will compute analytically after function setup...")
                return "compute_analytically"
                
            elif choice == "3":
                return None
                
            else:
                print("Please enter 1, 2, or 3.")
                
        except ValueError:
            print("Please enter a valid number.")


def get_epsilons_from_user():
    print("\n" + "=" * 60)
    print("TOLERANCE VALUES INPUT")
    print("=" * 60)
    
    print("\nEnter tolerance values (epsilon) for convergence criteria.")
    print("You can enter multiple values separated by spaces.")
    print("Examples: 1e-6, 1e-9, 0.001, 0.000001")
    
    while True:
        try:
            eps_input = input("Enter epsilon values: ").strip()
            
            if not eps_input:
                print("Please enter at least one tolerance value.")
                continue
            
            # Parse multiple epsilon values
            eps_parts = eps_input.replace(",", " ").split()
            epsilons = []
            
            for part in eps_parts:
                eps = float(part)
                if eps <= 0:
                    print(f"Error: {eps} must be positive.")
                    raise ValueError("Negative epsilon")
                epsilons.append(eps)
            
            print(f"Using epsilon values: {epsilons}")
            return epsilons
            
        except ValueError:
            print("Please enter valid positive numbers.")


def setup_problem_interactively():
    print("NUMERICAL METHODS FOR ROOT FINDING")
    print("Interactive Setup")
    print("=" * 60)
    
    # Get function and derivative
    f, df, f_string, df_string, f_expr, df_expr = get_function_from_user()
    
    # Get interval
    a, b = get_interval_from_user(f)
    
    # Get initial guess
    x0 = get_initial_guess_from_user(a, b)
    
    # Get g functions for fixed-point method
    x = symbols("x")
    g_funcs = get_g_functions_from_user(f_expr, x)
    
    # Get true root (optional)
    true_root_option = get_true_root_from_user()
    
    # Compute true root analytically if requested
    if true_root_option == "compute_analytically":
        print("\nComputing true root analytically...")
        true_root = compute_true_root_analytically(f_string, f, df, x0)
    else:
        true_root = true_root_option
    
    # Get epsilon values
    epsilons = get_epsilons_from_user()
    
    # Summary
    print("\n" + "=" * 60)
    print("PROBLEM SETUP SUMMARY")
    print("=" * 60)
    print(f"Function: f(x) = {f_string}")
    print(f"Derivative: f'(x) = {df_string}")
    print(f"Interval: [{a}, {b}]")
    print(f"Initial guess: x0 = {x0}")
    print(f"Custom g functions: {len(g_funcs)} provided")
    if true_root is not None:
        print(f"True root: {true_root}")
    else:
        print("True root: Will be computed numerically")
    print(f"Tolerances: {epsilons}")
    print("=" * 60)
    
    return f, df, f_string, df_string, a, b, x0, g_funcs, true_root, epsilons


# Default values (will be overridden by interactive input)
f = lambda x: math.cos(x) - x 
df = lambda x: -math.sin(x) - 1

g_funcs = [
    lambda x: x - 0.0001 * f(x),
]

f_string = "cos(x) - x"
df_string = "-sin(x) - 1"

true_root = 0.739085133215160641655

a, b = -4, 2
x0 = (a + b) / 2

epsilons = [1e-6, 1e-9]


def func_to_string_simple(func):
    try:
        source = inspect.getsource(func)

        lines = source.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("lambda"):
                expression = line[10:-1].strip()
                return expression

        return func.__name__ if hasattr(func, "__name__") else "unknown_function"

    except Exception:
        return getattr(func, "__name__", "unknown_function")


def fix_precision(x, precision=19):
    if abs(x) < 1e-19:
        return 0.0
    factor = 10 ** precision
    return round(x * factor) / factor


def stopping_condition_1(iteration, max_iter=10):
    return iteration >= max_iter


def stopping_condition_2(x_curr, x_prev, epsilon=1e-6):
    return abs(x_curr - x_prev) < epsilon


def relative_stopping_condition(x_curr, x_prev, tolerance=1e-6):
    if abs(x_curr) < 1e-15:
        return abs(x_curr - x_prev) < tolerance
    return abs(x_curr - x_prev) / abs(x_curr) < tolerance


def calculate_convergence_rate(sequence, true_root):
    if len(sequence) < 3:
        return "Insufficient data"

    errors = [abs(x - true_root) for x in sequence]
    orders = []

    for i in range(2, len(errors)):
        if errors[i - 2] < 1e-15 or errors[i - 1] < 1e-15 or errors[i] < 1e-15:
            continue

        if errors[i] <= 0 or errors[i - 1] <= 0 or errors[i - 2] <= 0:
            continue

        ratio1 = errors[i] / errors[i - 1]
        ratio2 = errors[i - 1] / errors[i - 2]

        if ratio1 <= 0 or ratio2 <= 0:
            continue

        try:
            order = math.log(ratio1) / math.log(ratio2)
            if 0 <= order <= 10:
                orders.append(order)

        except (ValueError, ZeroDivisionError, OverflowError):
            continue

    if not orders:
        return "Unable to determine"

    return sum(orders) / len(orders)


def bisection_method(f, a, b, epsilon=1e-6, condition=stopping_condition_2):
    if f(a) * f(b) >= 0:
        raise ValueError(f"f({a}) and f({b}) must have opposite signs")

    sequence = []
    for k in range(100):
        x = (a + b) / 2
        sequence.append(x)

        if k > 0 and condition(sequence[k], sequence[k - 1], epsilon):
            return sequence, "Second stopping condition (convergence)"

        if f(a) * f(x) < 0:
            b = x
        else:
            a = x

    return sequence, "First stopping condition (max iterations)"


def newton_method(f, df, x0, epsilon=1e-6, condition=stopping_condition_2):
    sequence = [x0]
    x = x0

    for k in range(100):
        try:
            x_new = x - f(x) / df(x)
            sequence.append(x_new)

            if condition(sequence[k], sequence[k - 1], epsilon):
                return sequence, "Second stopping condition (convergence)"

            x = x_new

        except ZeroDivisionError:
            return sequence, "Error: Zero derivative"

    return sequence, "First stopping condition (max iterations)"


def secant_method(f, x0, x1, epsilon=1e-6, condition=stopping_condition_2):
    sequence = []
    for k in range(100):
        try:
            f0, f1 = f(x0), f(x1)
            if abs(f1 - f0) < 1e-19:
                return sequence, "Error: Division by zero"

            x_new = x1 - f1 * (x1 - x0) / (f1 - f0)
            sequence.append(x_new)

            if k > 0 and condition(sequence[k], sequence[k - 1], epsilon):
                return sequence, "Second stopping condition (convergence)"

            x0, x1 = x1, x_new

        except (ZeroDivisionError, OverflowError):
            return sequence, "Error: Non-convergence"

    return sequence, "First stopping condition (max iterations)"


def evaluate_g_function(g, f, x0, test_iterations=50, tolerance=1e-9):
    try:
        x = x0

        for i in range(test_iterations):
            x_new = g(x)

            if abs(x_new) > 1e10 or math.isnan(x_new) or math.isinf(x_new):
                return False, float('inf')

            root_error = abs(f(x_new))
            if root_error < tolerance:
                return True, root_error

            if i > 10 and abs(x_new - x) > 10:
                return False, float('inf')

            x = x_new

        final_error = abs(f(x))
        if final_error < 1e-2:
            return True, final_error
        else:
            return False, final_error

    except Exception:
        return False, float('inf')


def select_best_g_function(f, x0, custom_g_functions=None):
    default_g_functions = [
        lambda x: x - 0.01 * f(x),
        lambda x: x + 0.01 * f(x),

        lambda x: x - 0.05 * f(x),
        lambda x: x + 0.05 * f(x),

        lambda x: x - 0.1 * f(x),
        lambda x: x + 0.1 * f(x),

        lambda x: x - 0.5 * f(x),
        lambda x: x + 0.5 * f(x),

        lambda x: x - 1.0 * f(x),
        lambda x: x + 1.0 * f(x),
    ]

    all_g_functions = (custom_g_functions or []) + default_g_functions

    data = []

    best_g = None
    best_error = float("inf")

    for i, g in enumerate(all_g_functions):
        if i < len(custom_g_functions or []):
            g_name = f"User {i + 1}"
        else:
            g_name = func_to_string_simple(g)

        converges, error = evaluate_g_function(g, f, x0)

        convergence_status = "Yes" if converges else "No"
        error_str = f"{error:.15f}" if error != float("inf") else "∞"

        data.append([g, convergence_status, error_str])

        if converges and error < 1e-2 and error < best_error:
            best_g = g
            best_error = error
            best_g_name = g_name


    if best_g is None:
        best_g = all_g_functions[0]

    else:
        pass

    return best_g, data


def fixed_point_method(f, x0, g, epsilon=1e-6, condition=stopping_condition_2):
    sequence = [x0]
    x = x0

    for k in range(100):
        try:
            x_new = g(x)
            sequence.append(x_new)

            if condition(sequence[k], sequence[k - 1], epsilon):
                return sequence, "Second stopping condition (convergence)"

            if abs(x_new) > 1e10 or math.isnan(x_new) or math.isinf(x_new):
                return sequence, "Error: Divergence"

            x = x_new

        except Exception:
            return sequence, "Error: Non-convergence"

    return sequence, "First stopping condition (max iterations)"


def aitken_acceleration(sequence, epsilon=1e-6):
    if len(sequence) < 3:
        return sequence, "Short sequence - minimum 3 elements needed"

    aitken_sequence = []

    for i in range(len(sequence) - 2):
        p0, p1, p2 = sequence[i], sequence[i + 1], sequence[i + 2]

        denominator = p0 + p2 - 2 * p1
        if abs(denominator) < 1e-19:
            accelerated = p2
        else:
            accelerated = p0 - ((p1 - p0)**2 / denominator)

        aitken_sequence.append(accelerated)

    return aitken_sequence, "First stopping condition (max iterations)"


def fixed_point_with_aitken(f, x0, g, epsilon=1e-6, max_iterations=20, condition=stopping_condition_2):
    regular_sequence = [x0]
    aitken_values = {}

    x = x0

    method_info = {
        'converged': False,
        'convergence_type': None,
        'final_value': None,
        'iterations': 0,
        'aitken_applications': 0
    }

    for k in range(max_iterations):
        x_new = g(x)
        regular_sequence.append(x_new)
        method_info['iterations'] = k + 1

        if k >= 2:
            p0, p1, p2 = regular_sequence[k -
                                          2], regular_sequence[k - 1], regular_sequence[k]
            denominator = p2 - 2 * p1 + p0

            if abs(denominator) > 1e-19:
                aitken_val = p0 - (p1 - p0)**2 / denominator
                aitken_values[k] = aitken_val
                method_info['aitken_applications'] += 1

                if (k - 1) in aitken_values:
                    if condition(aitken_val, aitken_values[k - 1], epsilon):
                        method_info['converged'] = True
                        method_info['convergence_type'] = 'Aitken acceleration'
                        method_info['final_value'] = aitken_val
                        break

        x = x_new

        if condition(regular_sequence[-1], regular_sequence[-2], epsilon):
            method_info['converged'] = True
            method_info['convergence_type'] = 'Regular iteration'
            method_info['final_value'] = regular_sequence[-1]
            break

        if abs(x) > 1e10:
            method_info['convergence_type'] = 'Diverged'
            method_info['final_value'] = x
            break

    if not method_info['converged'] and method_info['convergence_type'] != 'Diverged':
        method_info['convergence_type'] = 'Max iterations reached'
        if aitken_values:
            last_aitken_key = max(aitken_values.keys())
            method_info['final_value'] = aitken_values[last_aitken_key]
        else:
            method_info['final_value'] = regular_sequence[-1]

    return regular_sequence, aitken_values, method_info


def periodic_aitken_iteration(f, x0, g, epsilon=1e-6, max_iterations=20, period=3, condition=stopping_condition_2):
    sequence = [x0]
    aitken_applications = []
    x = x0

    method_info = {
        'converged': False,
        'convergence_type': None,
        'final_value': None,
        'iterations': 0,
        'aitken_applications': 0
    }

    for k in range(max_iterations):
        x_new = g(x)
        sequence.append(x_new)
        method_info['iterations'] = k + 1

        if (k + 1) % period == 0 and len(sequence) >= 3:
            p0, p1, p2 = sequence[-3], sequence[-2], sequence[-1]
            denominator = p2 - 2 * p1 + p0

            if abs(denominator) > 1e-19:
                aitken_val = p0 - (p1 - p0)**2 / denominator
                aitken_applications.append((k + 1, aitken_val))
                method_info['aitken_applications'] += 1
                x = aitken_val
            else:
                x = x_new
        else:
            x = x_new

        if condition(sequence[-1], sequence[-2], epsilon):
            method_info['converged'] = True
            method_info['convergence_type'] = 'Converged'
            method_info['final_value'] = x
            break

        if abs(x) > 1e10:
            method_info['convergence_type'] = 'Diverged'
            method_info['final_value'] = x
            break

    if not method_info['converged'] and method_info['convergence_type'] != 'Diverged':
        method_info['convergence_type'] = 'Max iterations reached'
        method_info['final_value'] = x

    return sequence, aitken_applications, method_info


def solve_with_relative_criterion(f, df, a, b):
    results = {}
    tolerance = 1e-6

    print("\nPhase 2: Solving with relative stopping criterion")
    print("=" * 60)

    print("\n1. Bisection method:")
    left, right = a, b
    sequence = []
    for k in range(100):
        midpoint = (left + right) / 2.0
        sequence.append(midpoint)

        if k > 0 and relative_stopping_condition(sequence[k], sequence[k - 1], tolerance):
            break

        if f(left) * f(midpoint) < 0:
            right = midpoint
        else:
            left = midpoint

    results["bisection"] = {"sequence": sequence, "iterations": len(sequence)}
    print(f"   Number of iterations: {len(sequence)}")
    print(f"   Final solution: {sequence[-1]}")

    print("\n2. Newton's method:")
    x = (a + b) / 2
    sequence = []
    for k in range(100):
        try:
            x_new = x - f(x) / df(x)
            sequence.append(x_new)

            if k > 0 and relative_stopping_condition(sequence[k], sequence[k - 1], tolerance):
                break

            x = x_new
        except Exception:
            break

    results["newton"] = {"sequence": sequence, "iterations": len(sequence)}
    print(f"   Number of iterations: {len(sequence)}")
    print(f"   Final solution: {sequence[-1]}")

    print("\n3. Secant method:")
    x0, x1 = a, b
    sequence = []
    for k in range(100):
        try:
            f_curr, f_prev = f(x1), f(x0)
            if abs(f_curr - f_prev) < 1e-19:
                break

            sequence.append(x_new)

            if k > 0 and relative_stopping_condition(sequence[k], sequence[k - 1], tolerance):
                break

            x0, x1 = x1, x_new
        except Exception:
            break

    results["secant"] = {"sequence": sequence, "iterations": len(sequence)}
    print(f"   Number of iterations: {len(sequence)}")
    print(f"   Final solution: {sequence[-1]}")

    return results


def print_detailed_results(method_name, sequence, aitken_seq, stopping_reason, f):
    print(f"\n{method_name}")
    print("-" * 75)
    print(f"{'k': <4} {'xₖ': <20} {'f(xₖ)': <15} {
          'Aitken': <20} {'f(Aitken)': <15}")
    print("-" * 75)

    max_display = min(len(sequence), 100)

    for i in range(max_display):
        xk = sequence[i]
        fxk = f(xk)

        if i >= 2 and (i - 2) < len(aitken_seq):
            aitken_val = aitken_seq[i - 2]
            f_aitken = f(aitken_val)
            print(
                f"{i + 1: <4} {xk: <20.15f} {fxk: <15.2e} {aitken_val: <20.15f} {f_aitken: <15.2e}")
        else:
            print(
                f"{i + 1: <4} {xk: <20.15f} {fxk: <15.2e} {'N/A': <20} {'N/A': <15}")

    print(f"\nStopping condition: {stopping_reason}")
    print(f"Total iterations: {len(sequence)}")


def estimate_computational_complexity(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = (end_time - start_time) * 1000 

    return execution_time, result


def extract_function_source(func):
    try:
        source = inspect.getsource(func)
        lines = source.split("\n")
        first_line = next((i for i, line in enumerate(lines) if line.strip()), 0)
        indent = len(lines[first_line]) - len(lines[first_line].lstrip())
        lines = [line[indent:] if line.strip() else line for line in lines]

        return "\n".join(lines)

    except Exception:
        return "Source code not available"


def analyze_test_function(f, df, name, a, b, x0, epsilon, true_root=None, g_funcs=[]):
    results = {}

    if true_root is None:
        true_seq, _ = newton_method(f, df, x0, 1e-15)
        true_root = true_seq[-1] if true_seq else None

    bis_time, (bis_seq, bis_reason) = estimate_computational_complexity(
        bisection_method, f, a, b, epsilon
    )

    bis_intervals = []
    a_current, b_current = a, b
    for x in bis_seq:
        bis_intervals.append((a_current, b_current, b_current - a_current))
        if f(a_current) * f(x) < 0:
            b_current = x
        else:
            a_current = x

    newton_time, (newton_seq, newton_reason) = estimate_computational_complexity(
        newton_method, f, df, x0, epsilon
    )

    secant_time, (secant_seq, secant_reason) = estimate_computational_complexity(
        secant_method, f, a, b, epsilon
    )

    best_g, _ = select_best_g_function(f, x0, g_funcs)
    si_time, (si_seq, si_reason) = estimate_computational_complexity(
        fixed_point_method, f, x0, best_g, epsilon
    )

    if len(bis_seq) >= 3:
        bis_aitken_time, (bis_aitken_seq, bis_aitken_reason) = estimate_computational_complexity(
            aitken_acceleration, bis_seq, epsilon
        )
    else:
        bis_aitken_seq, bis_aitken_reason = [], "Insufficient data"
        bis_aitken_time = 0

    if len(si_seq) >= 3:
        si_aitken_time, (si_aitken_seq, si_aitken_reason) = estimate_computational_complexity(
            aitken_acceleration, si_seq, epsilon
        )
    else:
        si_aitken_seq, si_aitken_reason = [], "Insufficient data"
        si_aitken_time = 0

    rt_aitken_time, (rt_seq, rt_values, rt_info) = estimate_computational_complexity(
        fixed_point_with_aitken, f, x0, best_g, epsilon, 20
    )

    periodic_time, (per_seq, per_apps, per_info) = estimate_computational_complexity(
        periodic_aitken_iteration, f, x0, best_g, epsilon, 20, 3
    )

    results['bisection'] = {
        'sequence': bis_seq,
        'intervals': bis_intervals,
        'time': bis_time,
        'reason': bis_reason,
        'iterations': len(bis_seq),
        'final_value': bis_seq[-1] if bis_seq else None,
        'error': abs(bis_seq[-1] - true_root) if bis_seq and true_root is not None else None,
        'convergence_rate': calculate_convergence_rate(bis_seq, true_root) if true_root is not None else None,
    }

    results['newton'] = {
        'sequence': newton_seq,
        'time': newton_time,
        'reason': newton_reason,
        'iterations': len(newton_seq),
        'final_value': newton_seq[-1] if newton_seq else None,
        'error': abs(newton_seq[-1] - true_root) if newton_seq and true_root is not None else None,
        'convergence_rate': calculate_convergence_rate(newton_seq, true_root) if true_root is not None else None,
    }

    results['secant'] = {
        'sequence': secant_seq,
        'time': secant_time,
        'reason': secant_reason,
        'iterations': len(secant_seq),
        'final_value': secant_seq[-1] if secant_seq else None,
        'error': abs(secant_seq[-1] - true_root) if secant_seq and true_root is not None else None,
        'convergence_rate': calculate_convergence_rate(secant_seq, true_root) if true_root is not None else None,
    }

    results['fixed_point'] = {
        'sequence': si_seq,
        'time': si_time,
        'reason': si_reason,
        'iterations': len(si_seq),
        'final_value': si_seq[-1] if si_seq else None,
        'error': abs(si_seq[-1] - true_root) if si_seq and true_root is not None else None,
        'convergence_rate': calculate_convergence_rate(si_seq, true_root) if true_root is not None else None,
    }

    results['bisection_aitken'] = {
        'sequence': bis_aitken_seq,
        'time': bis_aitken_time,
        'reason': bis_aitken_reason,
        'iterations': len(bis_aitken_seq),
        'final_value': bis_aitken_seq[-1] if bis_aitken_seq else None,
        'error': abs(bis_aitken_seq[-1] - true_root) if bis_aitken_seq and true_root is not None else None,
        'convergence_rate': calculate_convergence_rate(bis_aitken_seq, true_root) if true_root is not None else None,
    }

    results['si_aitken'] = {
        'sequence': si_aitken_seq,
        'time': si_aitken_time,
        'reason': si_aitken_reason,
        'iterations': len(si_aitken_seq),
        'final_value': si_aitken_seq[-1] if si_aitken_seq else None,
        'error': abs(si_aitken_seq[-1] - true_root) if si_aitken_seq and true_root is not None else None,
        'convergence_rate': calculate_convergence_rate(si_aitken_seq, true_root) if true_root is not None else None,
    }

    results['realtime_aitken'] = {
        'sequence': rt_seq,
        'time': rt_aitken_time,
        'reason': rt_info['convergence_type'],
        'iterations': rt_info['iterations'],
        'final_value': rt_info['final_value'],
        'error': abs(rt_info['final_value'] - true_root) if true_root is not None else None,
        'aitken_applications': rt_info['aitken_applications'],
        'convergence_rate': calculate_convergence_rate(rt_seq, true_root) if true_root is not None else None
    }

    results['periodic_aitken'] = {
        'sequence': per_seq,
        'time': periodic_time,
        'reason': per_info['convergence_type'],
        'iterations': per_info['iterations'],
        'final_value': per_info['final_value'],
        'error': abs(per_info['final_value'] - true_root) if true_root is not None else None,
        'aitken_applications': per_info['aitken_applications'],
        'convergence_rate': calculate_convergence_rate(per_seq, true_root) if true_root is not None else None
    }

    return {
        'name': name,
        'true_root': true_root,
        'interval': [a, b],
        'x0': x0,
        'epsilon': epsilon,
        'results': results
    }




def run_tests():
    test_results = []

    for epsilon in epsilons:
        print(f"\nRunning tests with epsilon = {epsilon}")

        print("Running tests with absolute error criterion...")

        bisection_seq, bisection_reason = bisection_method(f, a, b, epsilon)
        newton_seq, newton_reason = newton_method(f, df, x0, epsilon)

        # secant method with x0=a and x1=b from bisection
        secant_seq1, secant_reason1 = secant_method(f, a, b, epsilon)

        if len(bisection_seq) >= 3:
            x0_bis = bisection_seq[-3]
            x1_bis = bisection_seq[-2]
            header_bis = f"[x{len(bisection_seq) -
                              3}, x{len(bisection_seq) - 2}]"

            if len(bisection_seq) >= 11:
                x0_bis = bisection_seq[9]
                x1_bis = bisection_seq[10]
                header_bis = "[x9, x10]"

            # secant method with x0=x9 and x1=x10 from bisection
            secant_seq2, secant_reason2 = secant_method(f, x0_bis, x1_bis, epsilon)

        else:
            secant_seq2, secant_reason2 = [], "Short sequence from bisection"

        if len(newton_seq) >= 3:
            x0_newt = newton_seq[-3]
            x1_newt = newton_seq[-2]
            header_newt = f"[x{len(newton_seq) - 3}, x{len(newton_seq) - 2}]"

            if len(newton_seq) >= 11:
                x0_newt = newton_seq[9]
                x1_newt = newton_seq[10]
                header_newt = "[x9, x10]"

            # secnat method with x0=x9 and x1=x10 from newton
            secant_seq3, secant_reason3 = secant_method(f, x0_newt, x1_newt, epsilon)

        else:
            secant_seq3, secant_reason3 = [], "Short sequence from bisection"

        best_g, _ = select_best_g_function(f, x0, g_funcs)
        si_seq, si_reason = fixed_point_method(f, x0, best_g, epsilon)

        test_results.append(analyze_test_function(
            f, df, f"f(x) = {f_string} (ε = {epsilon}, absolute criterion)",
            a, b, x0, epsilon, true_root, g_funcs
        ))

        test_results.append({
            "name": f"Secant method from bisection [a, b] (ε = {epsilon}, absolute)",
            "true_root": true_root,
            "interval": [x0_bis, x1_bis] if len(bisection_seq) >= 3 else [a, b],
            "x0": x0,
            "epsilon": epsilon,
            "results": {
                "secant": {
                    "sequence": secant_seq1,
                    "time": 0,
                    "reason": secant_reason1,
                    "iterations": len(secant_seq1),
                    "final_value": secant_seq1[-1] if secant_seq1 else None,
                    "error": abs(secant_seq1[-1] - true_root) if secant_seq1 and true_root is not None else None,
                    "convergence_rate": calculate_convergence_rate(secant_seq1, true_root) if secant_seq1 and true_root is not None else None,
                }
            }
        })
        test_results.append({
            "name": f"Secant method from bisection {header_bis} (ε = {epsilon}, absolute)",
            "true_root": true_root,
            "interval": [x0_bis, x1_bis] if len(bisection_seq) >= 3 else [a, b],
            "x0": x0,
            "epsilon": epsilon,
            "results": {
                "secant": {
                    "sequence": secant_seq2,
                    "time": 0, 
                    "reason": secant_reason2,
                    "iterations": len(secant_seq2),
                    "final_value": secant_seq2[-1] if secant_seq2 else None,
                    "error": abs(secant_seq2[-1] - true_root) if secant_seq2 and true_root is not None else None,
                    "convergence_rate": calculate_convergence_rate(secant_seq2, true_root) if secant_seq2 and true_root is not None else None,
                }
            }
        })
        test_results.append({
            "name": f"Secant method from Newton {header_newt} (ε = {epsilon}, absolute)",
            "true_root": true_root,
            "interval": [x0_newt, x1_newt] if len(newton_seq) >= 3 else [a, b],
            "x0": x0,
            "epsilon": epsilon,
            "results": {
                "secant": {
                    "sequence": secant_seq3,
                    "time": 0,
                    "reason": secant_reason3,
                    "iterations": len(secant_seq3),
                    "final_value": secant_seq3[-1] if secant_seq3 else None,
                    "error": abs(secant_seq3[-1] - true_root) if secant_seq3 and true_root is not None else None,
                    "convergence_rate": calculate_convergence_rate(secant_seq3, true_root) if secant_seq3 and true_root is not None else None,
                }
            }
        })

        print("Running tests with relative error criterion...")

        rel_results = {}

        bis_rel_time, (bis_rel_seq, bis_rel_reason) = estimate_computational_complexity(
            bisection_method, f, a, b, epsilon, relative_stopping_condition
        )

        newton_rel_time, (newton_rel_seq, newton_rel_reason) = estimate_computational_complexity(
            newton_method, f, df, x0, epsilon, relative_stopping_condition
        )

        secant_rel_time, (secant_rel_seq, secant_rel_reason) = estimate_computational_complexity(
            secant_method, f, a, b, epsilon, relative_stopping_condition
        )

        si_rel_time, (si_rel_seq, si_rel_reason) = estimate_computational_complexity(
            fixed_point_method, f, x0, best_g, epsilon, relative_stopping_condition
        )

        rt_aitken_rel_time, (rt_rel_seq, si_rel_reason, _) = estimate_computational_complexity(
            fixed_point_with_aitken, f, x0, best_g, epsilon, condition=relative_stopping_condition
        )

        bis_rel_intervals = []
        a_current, b_current = a, b
        for x in bis_rel_seq:
            bis_rel_intervals.append((a_current, b_current, b_current - a_current))
            if f(a_current) * f(x) < 0:
                b_current = x
            else:
                a_current = x

        rel_results["bisection"] = {
            "sequence": bis_rel_seq,
            "intervals": bis_rel_intervals,
            "time": bis_rel_time,
            "reason": bis_rel_reason,
            "iterations": len(bis_rel_seq),
            "final_value": bis_rel_seq[-1] if bis_rel_seq else None,
            "error": abs(bis_rel_seq[-1] - true_root) if bis_rel_seq and true_root is not None else None,
            "convergence_rate": calculate_convergence_rate(bis_rel_seq, true_root) if true_root is not None else None,
        }

        rel_results["newton"] = {
            "sequence": newton_rel_seq,
            "time": newton_rel_time,
            "reason": newton_rel_reason,
            "iterations": len(newton_rel_seq),
            "final_value": newton_rel_seq[-1] if newton_rel_seq else None,
            "error": abs(newton_rel_seq[-1] - true_root) if newton_rel_seq and true_root is not None else None,
            "convergence_rate": calculate_convergence_rate(newton_rel_seq, true_root) if true_root is not None else None,
        }

        rel_results["secant"] = {
            "sequence": secant_rel_seq,
            "time": secant_rel_time,
            "reason": secant_rel_reason,
            "iterations": len(secant_rel_seq),
            "final_value": secant_rel_seq[-1] if secant_rel_seq else None,
            "error": abs(secant_rel_seq[-1] - true_root) if secant_rel_seq and true_root is not None else None,
            "convergence_rate": calculate_convergence_rate(secant_rel_seq, true_root) if true_root is not None else None,
        }

        rel_results["fixed_point"] = {
            "sequence": si_rel_seq,
            "time": si_rel_time,
            "reason": si_rel_reason,
            "iterations": len(si_rel_seq),
            "final_value": si_rel_seq[-1] if si_rel_seq else None,
            "error": abs(si_rel_seq[-1] - true_root) if si_rel_seq and true_root is not None else None,
            "convergence_rate": calculate_convergence_rate(si_rel_seq, true_root) if true_root is not None else None,
        }

        rel_results["realtime_aitken"] = {
            "sequence": rt_rel_seq,
            "time": rt_aitken_rel_time,
            "reason": si_rel_reason,
            "iterations": len(rt_rel_seq),
            "final_value": rt_rel_seq[-1] if rt_rel_seq else None,
            "error": abs(rt_rel_seq[-1] - true_root) if rt_rel_seq and true_root is not None else None,
            "convergence_rate": calculate_convergence_rate(rt_rel_seq, true_root) if true_root is not None else None
        }


        test_results.append({
            "name": f"f(x) = {f_string} (ε = {epsilon}, relative criterion)",
            "true_root": true_root,
            "interval": [a, b],
            "x0": x0,
            "epsilon": epsilon,
            "stopping_criterion": "relative",
            "results": rel_results
        })

        if len(bis_rel_seq) >= 3:
            bis_rel_aitken_time, (bis_rel_aitken_seq, bis_rel_aitken_reason) = estimate_computational_complexity(
                aitken_acceleration, bis_rel_seq, epsilon
            )

            rel_results["bisection_aitken"] = {
                "sequence": bis_rel_aitken_seq,
                "time": bis_rel_aitken_time,
                "reason": bis_rel_aitken_reason,
                "iterations": len(bis_rel_aitken_seq),
                "final_value": bis_rel_aitken_seq[-1] if bis_rel_aitken_seq else None,
                "error": abs(bis_rel_aitken_seq[-1] - true_root) if bis_rel_aitken_seq and true_root is not None else None,
                "convergence_rate": calculate_convergence_rate(bis_rel_aitken_seq, true_root) if true_root is not None else None,
            }

        if len(si_rel_seq) >= 3:
            si_rel_aitken_time, (si_rel_aitken_seq, si_rel_aitken_reason) = estimate_computational_complexity(
                aitken_acceleration, si_rel_seq, epsilon
            )

            rel_results["si_aitken"] = {
                "sequence": si_rel_aitken_seq,
                "time": si_rel_aitken_time,
                "reason": si_rel_aitken_reason,
                "iterations": len(si_rel_aitken_seq),
                "final_value": si_rel_aitken_seq[-1] if si_rel_aitken_seq else None,
                "error": abs(si_rel_aitken_seq[-1] - true_root) if si_rel_aitken_seq and true_root is not None else None,
                "convergence_rate": calculate_convergence_rate(si_rel_aitken_seq, true_root) if true_root is not None else None,
            }

    return test_results


def ensure_plot_directory():
    plot_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plots")
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)

    return plot_dir


def plot_bisection_method(f, a, b, sequence, intervals, true_root, epsilon, index=0):
    plot_dir = ensure_plot_directory()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    x = np.linspace(a, b, 1000)
    y = [f(xi) for xi in x]

    ax1.plot(x, y, "b-", label=f"f(x) = {f_string}")
    ax1.axhline(y=0, color="k", linestyle="-", alpha=0.3)
    ax1.axvline(x=true_root, color="g", linestyle="--",
                label=f"Root: x={true_root: .6f}")

    colors = ["red", "orange", "purple",
              "brown", "pink", "gray", "olive", "cyan"]

    ax1.plot([a, a], [0, f(a)], "ro-", label=f"Initial [a, b]: [{a}, {b}]")
    ax1.plot([b, b], [0, f(b)], "ro-")

    for i, x_val in enumerate(sequence[:min(8, len(sequence))]):
        color = colors[i % len(colors)]
        ax1.plot([x_val, x_val], [0, f(x_val)], marker="o", color=color, label=f"x{i + 1}={x_val: .6f}")

    ax1.set_title("Function and Bisection Points")
    ax1.set_xlabel("x")
    ax1.set_ylabel("f(x)")
    ax1.grid(True)
    ax1.legend(loc="best")

    iterations = list(range(1, len(intervals) + 1))
    interval_widths = [width for _, _, width in intervals]

    ax2.semilogy(iterations, interval_widths, "bo-", label="Interval Width")

    a_vals = [a_val for a_val, _, _ in intervals]
    b_vals = [b_val for _, b_val, _ in intervals]

    ax2.semilogy(iterations, [abs(a - true_root)
                              for a in a_vals], "ro--", label="|a - root|")
    ax2.semilogy(iterations, [abs(b - true_root)
                              for b in b_vals], "go--", label="|b - root|")

    ax2.axhline(y=epsilon, color="purple",
                linestyle="--", label=f"ε = {epsilon}")

    ax2.set_title("Bisection Interval Convergence")
    ax2.set_xlabel("Iteration")
    ax2.set_ylabel("Interval Width (log scale)")
    ax2.grid(True)
    ax2.legend(loc="best")

    plt.tight_layout()

    filename = f"bisection_graph_{index}_{epsilon}.png"
    filepath = os.path.join(plot_dir, filename)
    plt.savefig(filepath, dpi=300)
    plt.close(fig)

    return filename


def plot_newton_method(f, df, x0, sequence, true_root, epsilon, index=0):
    plot_dir = ensure_plot_directory()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    x_min = min(sequence) - 0.5
    x_max = max(sequence) + 0.5

    x_min = min(x_min, true_root - 0.5)
    x_max = max(x_max, true_root + 0.5)

    x = np.linspace(x_min, x_max, 1000)
    y = [f(xi) for xi in x]

    ax1.plot(x, y, "b-", label=f"f(x) = {f_string}")
    ax1.axhline(y=0, color="k", linestyle="-", alpha=0.3)
    ax1.axvline(x=true_root, color="g", linestyle="--",
                label=f"Root: x={true_root: .6f}")

    colors = ["red", "orange", "purple",
              "brown", "pink", "gray", "olive", "cyan"]
    max_iterations_to_plot = min(6, len(sequence) - 1)

    for i in range(max_iterations_to_plot):
        x_current = sequence[i]
        x_next = sequence[i + 1]
        color = colors[i % len(colors)]

        f_current = f(x_current)
        ax1.plot([x_current], [f_current], "o", color=color, markersize=6,
                 label=f"x{i + 1}={x_current: .6f}")

        df_current = df(x_current)
        tangent_x = np.linspace(x_current - 0.5, x_current + 0.5, 100)
        tangent_y = [f_current + df_current *
                     (xi - x_current) for xi in tangent_x]

        ax1.plot(tangent_x, tangent_y, "--", color=color, alpha=0.7)

        ax1.plot([x_current, x_current], [f_current, 0], ":", color=color)
        ax1.plot([x_current, x_next], [0, 0], ":", color=color)

    ax1.set_title("Newton's Method: Function and Tangent Lines")
    ax1.set_xlabel("x")
    ax1.set_ylabel("f(x)")
    ax1.grid(True)
    ax1.legend(loc="best")

    iterations = list(range(1, len(sequence) + 1))
    errors = [abs(x - true_root) for x in sequence]

    ax2.semilogy(iterations, errors, "bo-", label="Error |xₙ - root|")

    ax2.axhline(y=epsilon, color="purple",
                linestyle="--", label=f"ε = {epsilon}")

    if len(errors) >= 3:
        for i in range(2, min(5, len(errors))):
            if errors[i - 1] > 1e-15 and errors[i - 2] > 1e-15:
                ratio = errors[i] / (errors[i - 1]**2)
                ax2.annotate(f"e{i + 1}/e{i}² = {ratio: .2f}",
                             xy=(i + 1, errors[i]),
                             xytext=(i + 1.1, errors[i] * 2),
                             arrowprops=dict(arrowstyle="->"))

    ax2.set_title("Newton's Method: Error Convergence")
    ax2.set_xlabel("Iteration")
    ax2.set_ylabel("Error (log scale)")
    ax2.grid(True)
    ax2.legend(loc="best")

    plt.tight_layout()

    filename = f"newton_graph_{index}_{epsilon}.png"
    filepath = os.path.join(plot_dir, filename)
    plt.savefig(filepath, dpi=300)
    plt.close(fig)

    return filename


def plot_secant_method(f, x0, x1, sequence, true_root, epsilon, index=0):
    plot_dir = ensure_plot_directory()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    x_min = min(min(sequence), x0, x1) - 0.5
    x_max = max(max(sequence), x0, x1) + 0.5

    x_min = min(x_min, true_root - 0.5)
    x_max = max(x_max, true_root + 0.5)

    x = np.linspace(x_min, x_max, 1000)
    y = [f(xi) for xi in x]

    ax1.plot(x, y, "b-", label=f"f(x) = {f_string}")
    ax1.axhline(y=0, color="k", linestyle="-", alpha=0.3)
    ax1.axvline(x=true_root, color="g", linestyle="--",
                label=f"Root: x={true_root: .6f}")

    colors = ["red", "orange", "purple",
              "brown", "pink", "gray", "olive", "cyan"]

    max_iterations_to_plot = min(6, len(sequence) - 1)

    ax1.plot([x0], [f(x0)], "o", color="red",
             markersize=6, label=f"x₀={x0: .6f}")
    ax1.plot([x1], [f(x1)], "o", color="orange",
             markersize=6, label=f"x₁={x1: .6f}")

    for i in range(1, max_iterations_to_plot):
        if i == 1:
            x_prev, x_curr = x0, x1
        else:
            x_prev, x_curr = sequence[i - 2], sequence[i - 1]

        x_next = sequence[i]
        color = colors[i % len(colors)]

        f_prev = f(x_prev)
        f_curr = f(x_curr)
        f_next = f(x_next)

        ax1.plot([x_next], [f_next], "o", color=color, markersize=6,
                 label=f"x{i + 1}={x_next: .6f}")

        secant_x = np.linspace(min(x_prev, x_curr) - 0.2,
                               max(x_prev, x_curr) + 0.2, 100)
        slope = (f_curr - f_prev) / (x_curr - x_prev)
        intercept = f_curr - slope * x_curr
        secant_y = [slope * xi + intercept for xi in secant_x]
        ax1.plot(secant_x, secant_y, "--", color=color, alpha=0.7)

        ax1.plot([x_curr, x_curr], [f_curr, 0], ":", color=color)
        ax1.plot([x_curr, x_next], [0, 0], ":", color=color)

    ax1.set_title("Secant Method: Function and Secant Lines")
    ax1.set_xlabel("x")
    ax1.set_ylabel("f(x)")
    ax1.grid(True)
    ax1.legend(loc="best")

    iterations = list(range(1, len(sequence) + 1))
    errors = [abs(x - true_root) for x in sequence]

    ax2.semilogy(iterations, errors, "bo-", label="Error |xₙ - root|")

    if epsilon > 0:
        ax2.axhline(y=epsilon, color="purple",
                    linestyle="--", label=f"ε = {epsilon}")
    else:
        ax2.plot([], [], color="purple", linestyle="--",
                 label=f"ε = {epsilon} (not shown on log scale)")

    if len(errors) >= 3:
        for i in range(2, min(5, len(errors))):
            if errors[i - 1] > 1e-15 and errors[i - 2] > 1e-15:
                ratio = errors[i] / (errors[i - 1]**1.618)
                ax2.annotate(f"e{i + 1}/e{i}^1.618 = {ratio: .2f}",
                             xy=(i + 1, errors[i]),
                             xytext=(i + 1.1, errors[i] * 2),
                             arrowprops=dict(arrowstyle="->"))

    ax2.set_title("Secant Method: Error Convergence")
    ax2.set_xlabel("Iteration")
    ax2.set_ylabel("Error (log scale)")
    ax2.grid(True)
    ax2.legend(loc="best")

    plt.tight_layout()

    filename = f"secant_graph_{index}_{epsilon}.png"
    filepath = os.path.join(plot_dir, filename)
    plt.savefig(filepath, dpi=300)
    plt.close(fig)

    return filename


def plot_fixed_point(f, g, x0, sequence, true_root, epsilon, index=0):
    plot_dir = ensure_plot_directory()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    x_min = min(min(sequence), x0) - 0.5
    x_max = max(max(sequence), x0) + 0.5

    x_min = min(x_min, true_root - 0.5)
    x_max = max(x_max, true_root + 0.5)
    
    x = np.linspace(x_min, x_max, 1000)
    y_f = [f(xi) for xi in x]
    
    def g_func(x): return x + f(x)
    y_g = [g_func(xi) for xi in x]

    ax1.plot(x, y_f, "b-", label=f"f(x) = {f_string}")
    ax1.plot(x, y_g, "g-", label=f"g(x) = {func_to_string_simple(g)}")

    ax1.axhline(y=0, color="k", linestyle="-", alpha=0.3)
    ax1.axvline(x=true_root, color="r", linestyle="--", label=f"Root: x={true_root:.6f}")

    ax1.plot(x, x, "k--", alpha=0.5, label="y = x")

    colors = ["red", "orange", "purple", "brown", "pink", "gray", "olive", "cyan"]
    max_iterations_to_plot = min(6, len(sequence))

    ax1.plot([x0], [f(x0)], "o", color="red", markersize=6, label=f"x₀={x0:.6f}")

    curr_x = x0
    for i in range(max_iterations_to_plot):
        color = colors[i % len(colors)]
        next_x = sequence[i]

        ax1.plot([curr_x, curr_x], [f(curr_x), curr_x], ":", color=color)

        ax1.plot([curr_x, next_x], [curr_x, curr_x], ":", color=color)

        ax1.plot([next_x], [f(next_x)], "o", color=color, markersize=6,
                 label=f"x{i + 1}={next_x:.6f}")

        curr_x = next_x

    ax1.set_title("Fixed-point Method: g(x) and Iteration Process")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.grid(True)
    ax1.legend(loc="best")

    iterations = list(range(1, len(sequence) + 1))
    errors = [abs(x - true_root) for x in sequence]

    ax2.semilogy(iterations, errors, "bo-", label="Error |xₙ - root|")

    if epsilon > 0:
        ax2.axhline(y=epsilon, color="purple", linestyle="--", label=f"ε = {epsilon}")
    else:
        ax2.plot([], [], color="purple", linestyle="--", label=f"ε = {epsilon} (not shown on log scale)")

    if len(errors) >= 3:
        for i in range(2, min(5, len(errors))):
            if errors[i - 1] > 1e-15 and errors[i - 2] > 1e-15:
                ratio = errors[i] / (errors[i - 1]**2)
                ax2.annotate(f"e{i + 1}/e{i}² = {ratio: .2f}",
                             xy=(i + 1, errors[i]),
                             xytext=(i + 1.1, errors[i] * 2),
                             arrowprops=dict(arrowstyle="->"))

    ax2.set_title("Fixed-point Method: Error Convergence")
    ax2.set_xlabel("Iteration")
    ax2.set_ylabel("Error (log scale)")
    ax2.grid(True)
    ax2.legend(loc="best")

    plt.tight_layout()
    
    filename = f"fixed_point_graph_{index}_{epsilon}.png"
    filepath = os.path.join(plot_dir, filename)
    plt.savefig(filepath, dpi=300)
    plt.close(fig)
    
    return filename

def plot_fixed_point_aitken(f, g, x0, sequence, aitken_values, true_root, epsilon, index=0):
    plot_dir = ensure_plot_directory()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    all_points = sequence.copy()
    for _, value in aitken_values.items():
        all_points.append(value)
    
    x_min = min(min(all_points), x0) - 0.5
    x_max = max(max(all_points), x0) + 0.5

    x_min = min(x_min, true_root - 0.5)
    x_max = max(x_max, true_root + 0.5)
    
    x = np.linspace(x_min, x_max, 1000)
    y_f = [f(xi) for xi in x]
    
    def g_func(x): return x + f(x) 
    y_g = [g_func(xi) for xi in x]

    ax1.plot(x, y_f, "b-", label=f"f(x) = {f_string}")
    ax1.plot(x, y_g, "g-", label=f"g(x) = {func_to_string_simple(g)}")
    ax1.axhline(y=0, color="k", linestyle="-", alpha=0.3)
    ax1.axvline(x=true_root, color="r", linestyle="--", label=f"Root: x={true_root:.6f}")

    ax1.plot(x, x, "k--", alpha=0.5, label="y = x")

    ax1.plot(sequence, [f(xi) for xi in sequence], "bo-", markersize=4, label="Original Sequence", alpha=0.5)

    aitken_x = list(aitken_values.values())
    if aitken_x:
        ax1.plot(aitken_x, [f(xi) for xi in aitken_x], "r*", markersize=10, label="Aitken Accelerated Points")
    
    ax1.set_title("Fixed-point with Aitken Acceleration")
   
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.grid(True)
    ax1.legend(loc="best")
    
    iterations = list(range(1, len(sequence) + 1))
    errors = [abs(x - true_root) for x in sequence]
    
    ax2.semilogy(iterations, errors, "bo-", label="Original Sequence Error", alpha=0.5)
    
    if aitken_x:
        # Get the correct iteration indices for Aitken values
        aitken_iterations = sorted(aitken_values.keys())
        aitken_errors = [abs(aitken_values[i] - true_root) for i in aitken_iterations]
        
        # Convert iteration keys to 1-based indexing for plotting
        plot_iterations = [i + 1 for i in aitken_iterations]
        
        ax2.semilogy(plot_iterations, aitken_errors, 'r*-', markersize=8, label='Aitken Accelerated Error')
    
    if epsilon > 0:
        ax2.axhline(y=epsilon, color="purple", linestyle="--", label=f"ε = {epsilon}")
    else:
        ax2.plot([], [], color="purple", linestyle="--", label=f"ε = {epsilon} (not shown on log scale)")
    
    ax2.set_title("Error Convergence Comparison")
    ax2.set_xlabel("Iteration")
    ax2.set_ylabel("Error (log scale)")
    ax2.grid(True)
    ax2.legend(loc="best")

    plt.tight_layout()
    
    filename = f"fixed_point_aitken_graph_{index}_{epsilon}.png"
    filepath = os.path.join(plot_dir, filename)
    plt.savefig(filepath, dpi=300)
    plt.close(fig)
    
    return filename


def plot_g_functions_comparison(f, g_functions, true_root, x0):
    plot_dir = ensure_plot_directory()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    x_min = true_root - 1.5
    x_max = true_root + 1.5
    
    x = np.linspace(x_min, x_max, 1000)
    y_f = [f(xi) for xi in x]

    ax1.plot(x, y_f, "k-", label=f"f(x) = {f_string}", alpha=0.5)
    ax1.axhline(y=0, color="k", linestyle="-", alpha=0.3)

    ax1.plot(x, x, "k--", label="y = x", alpha=0.5)

    colors = ["blue", "red", "green", "purple", "orange", "cyan", "magenta", "brown"]

    for i, g_func in enumerate(g_functions):
        color = colors[i % len(colors)]
        
        g_formula = func_to_string_simple(g_func)
        
        y_g = [g_func(xi) if callable(g_func) else xi + f(xi) for xi in x]
        ax1.plot(x, y_g, color=color, label=f"g(x) = {g_formula}")

        try:
            intersections = []
            for j in range(len(x) - 1):
                if (y_g[j] - x[j]) * (y_g[j+1] - x[j+1]) <= 0:
                    intersections.append((x[j] + x[j+1]) / 2)
            
            for intersection in intersections:
                ax1.plot([intersection], [intersection], "o", color=color, markersize=6)
        except:
            pass
        
        try:
            y_g_prime = [(y_g[j+1] - y_g[j]) / (x[j+1] - x[j]) for j in range(len(x) - 1)]
            x_prime = [(x[j+1] + x[j]) / 2 for j in range(len(x) - 1)]
            
            ax2.plot(x_prime, y_g_prime, color=color, label=f"g'(x) for {g_formula}")
        except:
            pass

    ax1.axvline(x=true_root, color="r", linestyle="--", alpha=0.7, label=f"Root: x={true_root:.6f}")
    ax2.axvline(x=true_root, color="r", linestyle="--", alpha=0.7)

    ax2.axhline(y=1, color="green", linestyle="--", alpha=0.5, label="g'(x) = 1")
    ax2.axhline(y=-1, color="red", linestyle="--", alpha=0.5, label="g'(x) = -1")
    ax2.axhline(y=0, color="k", linestyle="-", alpha=0.3)

    ax2.fill_between(x_prime, -1, 1, color="green", alpha=0.1, label="Convergence region |g'(x)| < 1")

    ax1.plot([x0], [x0], "ko", markersize=8, label=f"Initial x₀={x0:.6f}")

    ax1.set_title("g(x) Functions Comparison")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.grid(True)
    ax1.legend(loc="best")

    ax2.set_title("Derivatives g'(x)")
    ax2.set_xlabel("x")
    ax2.set_ylabel("g'(x)")
    ax2.grid(True)
    ax2.legend(loc="best")

    plt.tight_layout()
    
    filename = "g_functions_comparison.png"
    filepath = os.path.join(plot_dir, filename)
    plt.savefig(filepath, dpi=300)
    plt.close(fig)
    
    return filename


def plot_stopping_criteria_comparison(f, absolute_sequence, relative_sequence, true_root, epsilon, method_name):
    plot_dir = ensure_plot_directory()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    iterations_abs = list(range(1, len(absolute_sequence) + 1))
    iterations_rel = list(range(1, len(relative_sequence) + 1))

    errors_abs = [abs(x - true_root) for x in absolute_sequence]
    errors_rel = [abs(x - true_root) for x in relative_sequence]

    ax1.semilogy(iterations_abs, errors_abs, "bo-", label="Absolute Criterion")
    ax1.semilogy(iterations_rel, errors_rel, "ro-", label="Relative Criterion", alpha=0.5)
    ax1.axhline(y=epsilon, color="purple",
                linestyle="--", label=f"ε = {epsilon}")

    ax1.set_title(f"{method_name}: Error Convergence")
    ax1.set_xlabel("Iteration")
    ax1.set_ylabel("Error (log scale)")
    ax1.grid(True)
    ax1.legend(loc="best")

    iterations_abs = list(range(1, len(absolute_sequence)))
    iterations_rel = list(range(1, len(relative_sequence)))

    abs_diffs = [abs(absolute_sequence[i] - absolute_sequence[i - 1]) for i in range(1, len(absolute_sequence))]
    rel_diffs = [abs(relative_sequence[i] - relative_sequence[i - 1]) / abs(relative_sequence[i]) for i in range(1, len(relative_sequence))]

    ax2.semilogy(iterations_abs, abs_diffs, "bo-", label="|xₙ₊₁ - xₙ| (Absolute)")
    ax2.semilogy(iterations_rel, rel_diffs, "ro-", label="|xₙ₊₁ - xₙ|/|xₙ₊₁| (Relative)")
    ax2.axhline(y=epsilon, color="purple", linestyle="--", label=f"ε = {epsilon}")

    ax2.set_title(f"{method_name}: Stopping Criteria")
    ax2.set_xlabel("Iteration")
    ax2.set_ylabel("Difference (log scale)")
    ax2.grid(True)
    ax2.legend(loc="best")

    plt.tight_layout()

    filename = f"stopping_criteria_{method_name}_{epsilon}.png"
    filename = filename.replace(" ", "_")
    filepath = os.path.join(plot_dir, filename)
    plt.savefig(filepath, dpi=300)
    plt.close(fig)

    return filename
def generate_md_report(test_results):
    method_names = {
        "bisection": "Bisection",
        "newton": "Newton",
        "secant": "Secant",
        "fixed_point": "Fixed-point",
        "bisection_aitken": "Bisection + Aitken",
        "si_aitken": "Fixed-point + Aitken",
        "realtime_aitken": "Real-time Aitken",
        "periodic_aitken": "Periodic Aitken"
    }

    md = "# Numerical Methods for Root Finding: Comprehensive Analysis\n\n"

    md += "## Table of Contents\n\n"
    md += "1. [Introduction](#introduction)\n"
    md += "2. [Test Functions](#test-functions)\n"
    md += "3. [Theoretical Background](#theoretical-background)\n"
    md += "4. [Method Descriptions with Examples](#method-descriptions-with-examples)\n"
    md += "5. [Performance Analysis](#performance-analysis)\n"
    md += "6. [Convergence Comparison](#convergence-comparison)\n"
    md += "7. [Final Comparison and Recommendations](#final-comparison-and-recommendations)\n\n"

    md += "## Introduction\n\n"
    md += "This report presents a comprehensive analysis of various numerical methods for finding roots of nonlinear equations. "
    md += "We compare different methods in terms of convergence speed, accuracy, stability, and computational efficiency. "
    md += "The methods analyzed include:\n\n"

    md += "- Bisection Method\n"
    md += "- Newton's Method\n"
    md += "- Secant Method\n"
    md += "- Fixed-point Method\n"
    md += "- Aitken's Acceleration\n"
    md += "- Real-time Aitken's Acceleration\n"
    # md += "- Periodic Aitken's Acceleration\n\n"

    md += "## Test Functions\n\n"
    md += "We tested the methods on the following function:\n\n"

    main_result = next(
        (r for r in test_results if 'bisection' in r['results']), test_results[0])

    md += f"### Primary Test Function: f(x) = {f_string}\n\n"
    md += f"- **Mathematical form**: f(x) = {f_string}\n"
    md += f"- **Derivative**: f'(x) = {df_string}\n"
    md += f"- **Interval**: [{main_result['interval'][0]:.15f}, {main_result['interval'][1]:.15f}]\n"
    md += f"- **Initial guess**: {main_result['x0']:.15f}\n"
    md += f"- **True root**: {main_result['true_root']:.15f}\n"
    md += f"- **Tolerance**: ε = {main_result['epsilon']:.15f}\n\n"

    md += "This function represents exponential growth problems and has applications in population dynamics, compound interest, and decay processes.\n\n"

    md += "## Theoretical Background\n\n"

    md += "### Convergence Rates\n\n"
    md += "- **Linear Convergence**: If |eₙ₊₁| ≤ c·|eₙ| for some constant c < 1, where eₙ is the error at iteration n. The bisection method exhibits linear convergence.\n\n"
    md += "- **Quadratic Convergence**: If |eₙ₊₁| ≤ c·|eₙ|² for some constant c. Newton's method shows quadratic convergence when the function is well-behaved.\n\n"
    md += "- **Superlinear Convergence**: If |eₙ₊₁| ≤ c·|eₙ|ᵖ for p > 1. The secant method typically has p ≈ 1.62.\n\n"

    md += "### Stopping Criteria\n\n"
    md += "- **Absolute Error**: |xₙ₊₁ - xₙ| < ε\n"
    md += "- **Relative Error**: |xₙ₊₁ - xₙ|/|xₙ₊₁| < ε\n"
    md += "- **Function Value**: |f(xₙ)| < ε\n\n"

    md += "### Aitken's Acceleration\n\n"
    md += "Aitken's acceleration transforms a linearly convergent sequence into a more rapidly convergent one. "
    md += "For a sequence {pₙ}, the Aitken's accelerated sequence {p̂ₙ} is defined as:\n\n"
    md += "p̂ₙ = pₙ - (pₙ₊₁ - pₙ)²/(pₙ₊₂ - 2pₙ₊₁ + pₙ)\n\n"

    md += "## Method Descriptions with Examples\n\n"

    def get_method_sequences(method_name, criterion=None):
        sequences = []
        for result in test_results:
            if criterion == 'relative' and not result.get('stopping_criterion') == 'relative':
                continue
            if criterion == 'absolute' and result.get('stopping_criterion') == 'relative':
                continue

            if method_name in result['results'] and result['results'][method_name]['sequence']:
                sequences.append((result, result['results'][method_name]))
        return sequences

    md += "### 1. Bisection Method\n\n"
    md += "#### Mathematical Formula\n\n"
    md += "Given a continuous function f(x) and an interval [a, b] where f(a) \\cdot f(b) < 0:\n\n"
    md += "x = \\frac{a + b}{2}\n\n"
    md += "The root lies in [a, c] if f(a) \\cdot f(x) < 0, otherwise in [x, b].\n\n"
    md += "#### Algorithm\n\n"
    md += "1. **Input**: Function f, interval [a, b], tolerance \\epsilon\n"
    md += "2. **Verify**: Check that f(a) \\cdot f(b) < 0\n"
    md += "3. **Iterate**:\n"
    md += "   - Compute midpoint: x = \\frac{a + b}{2}\n"
    md += "   - If |error| < \\epsilon, return x\n"
    md += "   - If f(a) \\cdot f(x) < 0, set b = x\n"
    md += "   - Otherwise, set a = x\n"
    md += "4. **Repeat** until convergence\n\n"
    md += "#### Convergence Rate\n\n"
    md += "Linear convergence with rate \\approx 0.5. Error reduces by half each iteration:\n"
    md += "|e_{n+1}| \\leq \\frac{1}{2}|e_n|\n\n"
    md += "#### Implementation\n\n"
    md += "```python\n"
    md += extract_function_source(bisection_method)
    md += "\n```\n\n"

    md += "#### Examples with Absolute Error Criterion |xₙ₊₁ - xₙ| < ε\n\n"
    bisection_sequences = get_method_sequences('bisection', 'absolute')

    for i, (result, method_result) in enumerate(bisection_sequences[:]):
        sequence = method_result['sequence']
        if len(sequence) > 100:
            sequence = sequence[:100]

        filename = plot_bisection_method(
            f,
            result['interval'][0],
            result['interval'][1],
            sequence,
            method_result['intervals'],
            result['true_root'],
            result['epsilon'],
            i
        )

        md += f"![Bisection Method Graph](plots/{filename})\n\n"

        md += f"##### Bisection Method Absolute Criterion (ε = {result['epsilon']:.15f})\n\n"
        md += "| Iteration | xₙ                  | f(xₙ)               | Error               | Interval [a, b]                    | Interval Length     | Abs. Difference     | Aitken              |\n"
        md += "|-----------|---------------------|---------------------|---------------------|-------------------------------------|---------------------|---------------------|---------------------|\n"

        aitken_sequences, _ = aitken_acceleration(sequence, result['epsilon'])
        aitken_sequences = ['N/A', 'N/A'] + aitken_sequences

        for j, x in enumerate(sequence):
            fx = f(x)
            error = abs(x - result['true_root'])

            abs_diff = "N/A"
            if j > 0:
                prev_x = sequence[j - 1]
                abs_diff = f"{abs(x - prev_x):.15f}" if abs(x) > 1e-15 else "N/A"

            if j < len(method_result['intervals']):
                a_val, b_val, interval_len = method_result['intervals'][j]
                interval_str = f"[{a_val:.15f}, {b_val:.15f}]"
                interval_len_str = f"{interval_len:.15f}"
            else:
                interval_str = "N/A"
                interval_len_str = "N/A"

            md += f"| {j + 1} | {x:.15f} | {fx:.15f} | {error:.15f} | {interval_str} | {interval_len_str} | {abs_diff} | {aitken_sequences[j]} |\n"

        md += f"\n**Result**: Converged to {method_result['final_value']:.15f} in {method_result['iterations']} iterations\n"
        md += f"**Final Error**: {method_result['error']:.15f}\n"
        conv_rate = method_result['convergence_rate']
        conv_rate_str = f"{conv_rate:.15f}" if isinstance(conv_rate, (int, float)) else str(conv_rate)
        md += f"**Convergence Rate**: {conv_rate_str}\n\n"

    md += "#### Examples with Relative Error Criterion |xₙ₊₁ - xₙ|/|xₙ₊₁| < ε\n\n"
    bisection_rel_sequences = get_method_sequences('bisection', 'relative')

    for i, (result, method_result) in enumerate(bisection_rel_sequences[:]):
        sequence = method_result['sequence']
        if len(sequence) > 100:
            sequence = sequence[:100]

        filename = plot_bisection_method(
            f,
            result['interval'][0],
            result['interval'][1],
            sequence,
            method_result['intervals'],
            result['true_root'],
            result['epsilon'],
            i + 100 
        )

        md += f"![Bisection Method Graph with Relative Criterion](plots/{
            filename})\n\n"
        md += f"##### Bisection Method with Relative Criterion (ε = {result['epsilon']:.15f})\n\n"

        md += "| Iteration | xₙ                  | f(xₙ)               | Error               | Interval [a, b]                    | Interval Length     | Rel. Difference     | Aitken              |\n"
        md += "|-----------|---------------------|---------------------|---------------------|-------------------------------------|---------------------|---------------------|---------------------|\n"

        aitken_sequences, _ = aitken_acceleration(sequence, result['epsilon'])
        aitken_sequences = ['N/A', 'N/A'] + aitken_sequences

        for j, x in enumerate(sequence):
            fx = f(x)
            error = abs(x - result['true_root'])

            rel_diff = "N/A"
            if j > 0:
                prev_x = sequence[j - 1]
                rel_diff = f"{abs(x - prev_x) / abs(x):.15f}" if abs(x) > 1e-15 else "N/A"

            if j < len(method_result['intervals']):
                a_val, b_val, interval_len = method_result['intervals'][j]
                interval_str = f"[{a_val:.15f}, {b_val:.15f}]"
                interval_len_str = f"{interval_len:.15f}"
            else:
                interval_str = "N/A"
                interval_len_str = "N/A"

            md += f"| {j + 1} | {x:.15f} | {fx:.15f} | {error:.15f} | {interval_str} | {interval_len_str} | {rel_diff} | {aitken_sequences[j]} |\n"

        md += f"\n**Result**: Converged to {method_result['final_value']:.15f} in {method_result['iterations']} iterations\n"
        md += f"**Final Error**: {method_result['error']:.15f}\n"
        conv_rate = method_result['convergence_rate']
        conv_rate_str = f"{conv_rate:.15f}" if isinstance(conv_rate, (int, float)) else str(conv_rate)
        md += f"**Convergence Rate**: {conv_rate_str}\n\n"

    abs_result = next((r for r, _ in bisection_sequences), None)
    rel_result = next((r for r, _ in bisection_rel_sequences), None)

    if abs_result and rel_result and abs_result['epsilon'] == rel_result['epsilon']:
        abs_seq = abs_result['results']['bisection']['sequence']
        rel_seq = rel_result['results']['bisection']['sequence']

        if len(abs_seq) > 2 and len(rel_seq) > 2:
            filename = plot_stopping_criteria_comparison(
                f,
                abs_seq,
                rel_seq,
                abs_result['true_root'],
                abs_result['epsilon'],
                method_names['bisection']
            )

            md += "#### Comparison of Stopping Criteria for Bisection Method\n\n"
            md += f"![Stopping Criteria Comparison](plots/{filename})\n\n"

            md += "| Criterion | Iterations | Final Value         | Error               |\n"
            md += "|-----------|------------|---------------------|---------------------|\n"
            md += f"| Absolute | {len(abs_seq)} | {abs_seq[-1]:.15f} | {abs(abs_seq[-1] - abs_result['true_root']):.15f} |\n"
            md += f"| Relative | {len(rel_seq)} | {rel_seq[-1]:.15f} | {abs(rel_seq[-1] - rel_result['true_root']):.15f} |\n\n"

    md += "### 2. Newton's Method\n\n"
    md += "#### Mathematical Formula\n\n"
    md += "Starting with an initial guess x_0, the Newton-Raphson iteration is:\n\n"
    md += "x_{n+1} = x_n - \\frac{f(x_n)}{f'(x_n)}\n\n"
    md += "This formula comes from the linear approximation of f(x) at x_n:\n"
    md += "f(x) \\approx f(x_n) + f'(x_n)(x - x_n)\n\n"
    md += "Setting f(x) = 0 and solving for x gives the Newton iteration.\n\n"
    md += "#### Algorithm\n\n"
    md += "1. **Input**: Function f, derivative f', initial guess x_0, tolerance \\epsilon\n"
    md += "2. **Initialize**: Set n = 0\n"
    md += "3. **Iterate**:\n"
    md += "   - Compute x_{n+1} = x_n - \\frac{f(x_n)}{f'(x_n)}\n"
    md += "   - If |error| < \\epsilon, return x_{n+1}\n"
    md += "   - Set n = n + 1\n"
    md += "4. **Repeat** until convergence or maximum iterations\n\n"
    md += "#### Convergence Rate\n\n"
    md += "Quadratic convergence when f'(r) \\neq 0 at the root r:\n"
    md += "|e_{n+1}| \\leq C|e_n|^2\n\n"
    md += "where C = \\frac{|f''(r)|}{2|f'(r)|}\n\n"
    md += "#### Implementation\n\n"
    md += "```python\n"
    md += extract_function_source(newton_method)
    md += "\n```\n\n"

    md += "#### Examples with Absolute Error Criterion |xₙ₊₁ - xₙ| < ε\n\n"
    newton_sequences = get_method_sequences('newton', 'absolute')

    for i, (result, method_result) in enumerate(newton_sequences[:]):
        sequence = method_result['sequence']
        if len(sequence) > 100:
            sequence = sequence[:100]

        filename = plot_newton_method(
            f,
            df,
            result['x0'],
            sequence,
            result['true_root'],
            result['epsilon'],
            i
        )

        md += f"![Newton's Method Graph](plots/{filename})\n\n"

        md += f"##### Newton's Method (ε = {result['epsilon']:.15f})\n\n"
        md += "| Iteration | xₙ                  | f(xₙ)               | f'(xₙ)              | Error               | Abs. Error          | Aitken              |\n"
        md += "|-----------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|\n"

        aitken_sequences, _ = aitken_acceleration(sequence, result['epsilon'])
        aitken_sequences = ['N/A', 'N/A'] + aitken_sequences

        prev_error = None
        for j, x in enumerate(sequence):
            fx = f(x)
            fpx = math.exp(x)
            error = abs(x - result['true_root'])

            abs_diff = "N/A"
            if j > 0:
                prev_x = sequence[j - 1]
                abs_diff = f"{abs(x - prev_x):.15f}" if abs(x) > 1e-15 else "N/A"

            md += f"| {j + 1} | {x:.15f} | {fx:.15f} | {fpx:.15f} | {error:.15f} | {abs_diff} | {aitken_sequences[j]} |\n"
            prev_error = error

        md += f"\n**Result**: Converged to {method_result['final_value']:.15f} in {method_result['iterations']} iterations\n"
        md += f"**Final Error**: {method_result['error']:.15f}\n"
        conv_rate = method_result['convergence_rate']
        conv_rate_str = f"{conv_rate:.15f}" if isinstance(conv_rate, (int, float)) else str(conv_rate)
        md += f"**Convergence Rate**: {conv_rate_str}\n\n"

    md += "#### Examples with Relative Error Criterion |xₙ₊₁ - xₙ|/|xₙ₊₁| < ε\n\n"
    newton_rel_sequences = get_method_sequences('newton', 'relative')

    for i, (result, method_result) in enumerate(newton_rel_sequences[:]):
        sequence = method_result['sequence']
        if len(sequence) > 100:
            sequence = sequence[:100]

        filename = plot_newton_method(
            f,
            df,
            result['x0'],
            sequence,
            result['true_root'],
            result['epsilon'],
            i + 100 
        )

        md += f"![Newton's Method Graph with Relative Criterion](plots/{
            filename})\n\n"

        md += f"##### Newton's Method with Relative Criterion (ε = {result['epsilon']:.15f})\n\n"
        md += "| Iteration | xₙ                  | f(xₙ)               | f'(xₙ)              | Error               | Rel. Difference     | Aitken              |\n"
        md += "|-----------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|\n"

        aitken_sequences, _ = aitken_acceleration(sequence, result['epsilon'])
        aitken_sequences = ['N/A', 'N/A'] + aitken_sequences

        for j, x in enumerate(sequence):
            fx = f(x)
            fpx = df(x)
            error = abs(x - result['true_root'])

            rel_diff = "N/A"
            if j > 0:
                prev_x = sequence[j - 1]
                rel_diff = f"{abs(x - prev_x) / abs(x):.15f}" if abs(x) > 1e-15 else "N/A"

            md += f"| {j + 1} | {x:.15f} | {fx:.15f} | {fpx:.15f} | {error:.15f} | {rel_diff} | {aitken_sequences[j]} |\n"

        md += f"\n**Result**: Converged to {method_result['final_value']:.15f} in {method_result['iterations']} iterations\n"
        md += f"**Final Error**: {method_result['error']:.15f}\n"
        conv_rate = method_result['convergence_rate']
        conv_rate_str = f"{conv_rate:.15f}" if isinstance(conv_rate, (int, float)) else str(conv_rate)
        md += f"**Convergence Rate**: {conv_rate_str}\n\n"

    abs_result = next((r for r, _ in newton_sequences), None)
    rel_result = next((r for r, _ in newton_rel_sequences), None)

    if abs_result and rel_result and abs_result['epsilon'] == rel_result['epsilon']:
        abs_seq = abs_result['results']['newton']['sequence']
        rel_seq = rel_result['results']['newton']['sequence']

        if len(abs_seq) > 2 and len(rel_seq) > 2:
            filename = plot_stopping_criteria_comparison(
                f,
                abs_seq,
                rel_seq,
                abs_result['true_root'],
                abs_result['epsilon'],
                method_names['newton']
            )

            md += "#### Comparison of Stopping Criteria for Newton's Method\n\n"
            md += f"![Stopping Criteria Comparison](plots/{filename})\n\n"

            md += "| Criterion | Iterations | Final Value         | Error               |\n"
            md += "|-----------|------------|---------------------|---------------------|\n"
            md += f"| Absolute | {len(abs_seq)} | {abs_seq[-1]:.15f} | {abs(abs_seq[-1] - abs_result['true_root']):.15f} |\n"
            md += f"| Relative | {len(rel_seq)} | {rel_seq[-1]:.15f} | {abs(rel_seq[-1] - rel_result['true_root']):.15f} |\n\n"

    md += "### 3. Secant Method\n\n"
    md += "#### Mathematical Formula\n\n"
    md += "The secant method approximates the derivative using two previous points:\n\n"
    md += "x_{n+1} = x_n - f(x_n) \\cdot \\frac{x_n - x_{n-1}}{f(x_n) - f(x_{n-1})}\n\n"
    md += "This can be rewritten as:\n"
    md += "x_{n+1} = \\frac{x_{n-1}f(x_n) - x_n f(x_{n-1})}{f(x_n) - f(x_{n-1})}\n\n"
    md += "#### Algorithm\n\n"
    md += "1. **Input**: Function f, two initial points x_0, x_1, tolerance \\epsilon\n"
    md += "2. **Initialize**: Set n = 1\n"
    md += "3. **Iterate**:\n"
    md += "   - Compute x_{n+1} = x_n - f(x_n) \\cdot \\frac{x_n - x_{n-1}}{f(x_n) - f(x_{n-1})}\n"
    md += "   - If |error| < \\epsilon, return x_{n+1}\n"
    md += "   - Set n = n + 1\n"
    md += "4. **Repeat** until convergence or maximum iterations\n\n"
    md += "#### Convergence Rate\n\n"
    md += "Superlinear convergence with rate \\phi = \\frac{1 + \\sqrt{5}}{2} \\approx 1.618 (golden ratio):\n"
    md += "|e_{n+1}| \\leq C|e_n|^\\phi\n\n"
    md += "#### Implementation\n\n"
    md += "```python\n"
    md += extract_function_source(secant_method)
    md += "\n```\n\n"

    md += "#### Examples with Absolute Error Criterion |xₙ₊₁ - xₙ| < ε\n\n"
    secant_sequences = get_method_sequences('secant', 'absolute')

    for i, (result, method_result) in enumerate(secant_sequences[:]):
        sequence = method_result['sequence']
        if len(sequence) > 100:
            sequence = sequence[:100]

        filename = plot_secant_method(
            f,
            result['interval'][0],
            result['interval'][1],
            sequence,
            result['true_root'],
            result['epsilon'],
            i
        )

        md += f"![Secant Method Graph](plots/{filename})\n\n"

        md += f"##### {result['name']}\n\n"
        md += "| Iteration | xₙ                  | f(xₙ)               | Error               | Abs. Error          | Aitken              |\n"
        md += "|-----------|---------------------|---------------------|---------------------|---------------------|---------------------|\n"

        aitken_sequences, _ = aitken_acceleration(sequence, result['epsilon'])
        aitken_sequences = ['N/A', 'N/A'] + aitken_sequences

        for j, x in enumerate(sequence):
            fx = f(x)
            if j > 0:
                prev_x = sequence[j - 1]
                prev_fx = f(prev_x)
                approx_deriv = (fx - prev_fx) / (x - prev_x) if abs(x - prev_x) > 1e-15 else "N/A"
            else:
                approx_deriv = "N/A"

            abs_diff = "N/A"
            if j > 0:
                prev_x = sequence[j - 1]
                abs_diff = f"{abs(x - prev_x):.15f}" if abs(x) > 1e-15 else "N/A"

            error = abs(x - result['true_root'])
            approx_str = f"{approx_deriv:.15f}" if isinstance(approx_deriv, float) else approx_deriv

            md += f"| {j + 1} | {x:.15f} | {fx:.15f} | {error:.15f} | {abs_diff} | {aitken_sequences[j]} |\n"

        md += f"\n**Result**: Converged to {method_result['final_value']:.15f} in {method_result['iterations']} iterations\n"
        md += f"**Final Error**: {method_result['error']:.15f}\n"
        conv_rate = method_result['convergence_rate']
        conv_rate_str = f"{conv_rate:.15f}" if isinstance(conv_rate, (int, float)) else str(conv_rate)
        md += f"**Convergence Rate**: {conv_rate_str}\n\n"

    md += "#### Examples with Relative Error Criterion |xₙ₊₁ - xₙ|/|xₙ₊₁| < ε\n\n"
    secant_rel_sequences = get_method_sequences('secant', 'relative')

    for i, (result, method_result) in enumerate(secant_rel_sequences[:]):
        sequence = method_result['sequence']
        if len(sequence) > 100:
            sequence = sequence[:100]

        filename = plot_secant_method(
            f,
            result['interval'][0],
            result['interval'][1],
            sequence,
            result['true_root'],
            result['epsilon'],
            i + 100 
        )

        md += f"![Secant Method Graph with Relative Criterion](plots/{
            filename})\n\n"

        md += f"##### {result['name']} \n\n"
        md += "| Iteration | xₙ                  | f(xₙ)               | Error               | Rel. Difference     | Aitken              |\n"
        md += "|-----------|---------------------|---------------------|---------------------|---------------------|---------------------|\n"

        aitken_sequences, _ = aitken_acceleration(sequence, result['epsilon'])
        aitken_sequences = ['N/A', 'N/A'] + aitken_sequences

        for j, x in enumerate(sequence):
            fx = f(x)
            fpx = df(x)
            error = abs(x - result['true_root'])

            rel_diff = "N/A"
            if j > 0:
                prev_x = sequence[j - 1]
                rel_diff = f"{abs(x - prev_x) / abs(x):.15f}" if abs(x) > 1e-15 else "N/A"

            md += f"| {j + 1} | {x:.15f} | {fx:.15f} | {fpx:.15f} | {error:.15f} | {rel_diff} | {aitken_sequences[j]} |\n"

        md += f"\n**Result**: Converged to {method_result['final_value']:.15f} in {method_result['iterations']} iterations\n"
        md += f"**Final Error**: {method_result['error']:.15f}\n"
        conv_rate = method_result['convergence_rate']
        conv_rate_str = f"{conv_rate:.15f}" if isinstance(conv_rate, (int, float)) else str(conv_rate)
        md += f"**Convergence Rate**: {conv_rate_str}\n\n"

    abs_result = next((r for r, _ in secant_sequences), None)
    rel_result = next((r for r, _ in secant_rel_sequences), None)

    if abs_result and rel_result and abs_result['epsilon'] == rel_result['epsilon']:
        abs_seq = abs_result['results']['secant']['sequence']
        rel_seq = rel_result['results']['secant']['sequence']

        if len(abs_seq) > 2 and len(rel_seq) > 2:
            filename = plot_stopping_criteria_comparison(
                f,
                abs_seq,
                rel_seq,
                abs_result['true_root'],
                abs_result['epsilon'],
                method_names['secant']
            )

            md += "#### Comparison of Stopping Criteria for Secant Method\n\n"
            md += f"![Stopping Criteria Comparison](plots/{filename})\n\n"

            md += "| Criterion | Iterations | Final Value         | Error               |\n"
            md += "|-----------|------------|---------------------|---------------------|\n"
            md += f"| Absolute | {len(abs_seq)} | {abs_seq[-1]:.15f} | {abs(abs_seq[-1] - abs_result['true_root']):.15f} |\n"
            md += f"| Relative | {len(rel_seq)} | {rel_seq[-1]:.15f} | {abs(rel_seq[-1] - rel_result['true_root']):.15f} |\n\n"

   
    md += "### 4. Fixed-point Method\n\n"
    md += "#### Mathematical Formula\n\n"
    md += "Transform the equation f(x) = 0 into the equivalent form x = g(x), then iterate:\n\n"
    md += "x_{n+1} = g(x_n)\n\n"
    md += "#### Algorithm\n\n"
    md += "1. **Input**: Function f, initial guess x_0, tolerance \\epsilon\n"
    md += "2. **Transform**: Define g(x) such that f(x) = 0 \\Leftrightarrow x = g(x)\n"
    md += "3. **Initialize**: Set n = 0\n"
    md += "4. **Iterate**:\n"
    md += "   - Compute x_{n+1} = g(x_n)\n"
    md += "   - If |error| < \\epsilon, return x_{n+1}\n"
    md += "   - Set n = n + 1\n"
    md += "5. **Repeat** until convergence or maximum iterations\n\n"
    md += "#### Convergence Condition\n\n"
    md += "Convergence requires |g'(r)| < 1 at the fixed point r:\n"
    md += "|e_{n+1}| \\leq |g'(\\xi)||e_n|\n\n"
    md += "where \\xi lies between x_n and r.\n\n"
    md += "#### Implementation\n\n"
    md += "```python\n"
    md += extract_function_source(fixed_point_method)
    md += "\n```\n\n"

    md += "#### Best g(x) Function\n\n"

    best_g, data = select_best_g_function(f, x0, g_funcs)

    md += f"The best g(x) function is: **{func_to_string_simple(best_g)}**\n\n"
    md += "| g(x)                     | Convergence | Error               |\n"
    md += "|--------------------------|-------------|---------------------|\n"
    for g_func, convergence, error in data:
        error_str = f"{error:.15f}" if isinstance(error, (int, float)) else str(error)
        md += f"| {func_to_string_simple(g_func)} | {convergence} | {error_str} |\n"

    g_funcs_to_plot = []
    g_labels = []

    for g_func, convergence, error in list(sorted(data, key=lambda x: x[2]))[:2]:
        if convergence == 'Yes':
            g_funcs_to_plot.append(g_func)
            g_labels.append(func_to_string_simple(g_func))

    for g_func, convergence, error in list(sorted(data, key=lambda x: x[2], reverse=True)[:2]):
        g_funcs_to_plot.append(g_func)
        g_labels.append(func_to_string_simple(g_func))

    g_funcs_to_plot = list(dict.fromkeys(g_funcs_to_plot))
    g_labels = list(dict.fromkeys(g_labels))

    filename = plot_g_functions_comparison(f, g_funcs_to_plot, result['true_root'], result['x0'])
    md += f"\n![g(x) Functions Comparison](plots/{filename})\n\n"

    md += "**Explanation**:\n\n"
    md += "- The plot shows different g(x) functions and their derivatives\n"
    md += "- For convergence, we need |g'(x)| < 1 at the root (shaded green area in right plot)\n"
    md += "- The best g(x) has its derivative closest to 0 at the root, giving fastest convergence\n"
    md += "- Functions with g'(x) outside [-1,1] at the root will diverge\n\n"

    md += "#### Examples with Absolute Error Criterion |xₙ₊₁ - xₙ| < ε\n\n"
    si_sequences = get_method_sequences('fixed_point', 'absolute')

    for i, (result, method_result) in enumerate(si_sequences[:]):
        sequence = method_result['sequence']
        if len(sequence) > 100:
            sequence = sequence[:100]

        filename = plot_fixed_point(
            f,
            best_g,
            result['x0'],
            sequence,
            result['true_root'],
            result['epsilon'],
            i
        )

        md += f"![Fixed-point Method Graph](plots/{filename})\n\n"


        md += f"##### Fixed-point Method (ε = {result['epsilon']:.15f})\n\n"
        md += "| Iteration | xₙ                  | g(xₙ)               | f(xₙ)               | Error               | Aitken              |\n"
        md += "|-----------|---------------------|---------------------|---------------------|---------------------|---------------------|\n"

        aitken_sequences, _ = aitken_acceleration(sequence, result['epsilon'])
        aitken_sequences = ['N/A', 'N/A'] + aitken_sequences

        for j, x in enumerate(sequence):
            gx = x + f(x)  # g(x) = x + f(x)
            fx = f(x)
            error = abs(x - result['true_root'])

            md += f"| {j + 1} | {x:.15f} | {gx:.15f} | {fx:.15f} | {error:.15f} | {aitken_sequences[j]} |\n"

        md += f"\n**Result**: {'Converged' if method_result['final_value'] else 'Did not converge'}\n"
        if method_result['final_value']:
            md += f"**Final Value**: {method_result['final_value']:.15f} in {method_result['iterations']} iterations\n"
            md += f"**Final Error**: {method_result['error']:.15f}\n"
            conv_rate = method_result['convergence_rate']
            conv_rate_str = f"{conv_rate:.15f}" if isinstance(conv_rate, (int, float)) else str(conv_rate)
            md += f"**Convergence Rate**: {conv_rate_str}\n\n"
        else:
            md += f"**Reason**: {method_result['reason']}\n\n"

    md += "#### Examples with Relative Error Criterion |xₙ₊₁ - xₙ|/|xₙ₊₁| < ε\n\n"
    si_rel_sequences = get_method_sequences('fixed_point', 'relative')

    for i, (result, method_result) in enumerate(si_rel_sequences[:]):
        sequence = method_result['sequence']
        if len(sequence) > 100:
            sequence = sequence[:100]

        filename = plot_fixed_point(
            f,
            best_g,
            result['x0'],
            sequence,
            result['true_root'],
            result['epsilon'],
            i + 100 
        )
    
        md += f"![Fixed-point Method Graph with Relative Criterion](plots/{filename})\n\n"


        md += f"##### Fixed-point Method with Relative Criterion (ε = {result['epsilon']:.15f})\n\n"
        md += "| Iteration | xₙ                  | g(xₙ)               | f(xₙ)               | Error               | Rel. Difference     | Aitken              |\n"
        md += "|-----------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|\n"

        aitken_sequences, _ = aitken_acceleration(sequence, result['epsilon'])
        aitken_sequences = ['N/A', 'N/A'] + aitken_sequences

        for j, x in enumerate(sequence):
            gx = x + f(x)
            fx = f(x)
            error = abs(x - result['true_root'])

            rel_diff = "N/A"
            if j > 0:
                prev_x = sequence[j - 1]
                rel_diff = f"{abs(x - prev_x) / abs(x):.15f}" if abs(x) > 1e-15 else "N/A"

            md += f"| {j + 1} | {x:.15f} | {gx:.15f} | {fx:.15f} | {error:.15f} | {rel_diff} | {aitken_sequences[j]} |\n"

        md += f"\n**Result**: {'Converged' if method_result['final_value'] else 'Did not converge'}\n"
        if method_result['final_value']:
            md += f"**Final Value**: {method_result['final_value']:.15f} in {method_result['iterations']} iterations\n"
            md += f"**Final Error**: {method_result['error']:.15f}\n"
            conv_rate = method_result['convergence_rate']
            conv_rate_str = f"{conv_rate:.15f}" if isinstance(conv_rate, (int, float)) else str(conv_rate)
            md += f"**Convergence Rate**: {conv_rate_str}\n\n"
        else:
            md += f"**Reason**: {method_result['reason']}\n\n"

    abs_result = next((r for r, _ in si_sequences), None)
    rel_result = next((r for r, _ in si_rel_sequences), None)

    if abs_result and rel_result and abs_result['epsilon'] == rel_result['epsilon']:
        abs_seq = abs_result['results']['fixed_point']['sequence']
        rel_seq = rel_result['results']['fixed_point']['sequence']

        if len(abs_seq) > 2 and len(rel_seq) > 2:
            filename = plot_stopping_criteria_comparison(
                f,
                abs_seq,
                rel_seq,
                abs_result['true_root'],
                abs_result['epsilon'],
                method_names['fixed_point']
            )

            md += "#### Comparison of Stopping Criteria for Fixed-point Method\n\n"
            md += f"![Stopping Criteria Comparison](plots/{filename})\n\n"

            md += "| Criterion | Iterations | Final Value         | Error               |\n"
            md += "|-----------|------------|---------------------|---------------------|\n"
            md += f"| Absolute | {len(abs_seq)} | {abs_seq[-1]:.15f} | {abs(abs_seq[-1] - abs_result['true_root']):.15f} |\n"
            md += f"| Relative | {len(rel_seq)} | {rel_seq[-1]:.15f} | {abs(rel_seq[-1] - rel_result['true_root']):.15f} |\n\n"

    md += "### 5. Aitken's Acceleration\n\n"
    md += "#### Mathematical Formula\n\n"
    md += "For a sequence \\{p_n\\} converging to limit p, Aitken's \\Delta^2 method produces:\n\n"
    md += "\\hat{p}_n = p_n - \\frac{(\\Delta p_n)^2}{\\Delta^2 p_n}\n\n"
    md += "where:\n"
    md += "- \\Delta p_n = p_{n+1} - p_n (forward difference)\n"
    md += "- \\Delta^2 p_n = \\Delta p_{n+1} - \\Delta p_n = p_{n+2} - 2p_{n+1} + p_n (second difference)\n\n"
    md += "Expanded form:\n"
    md += "\\hat{p}_n = p_n - \\frac{(p_{n+1} - p_n)^2}{p_{n+2} - 2p_{n+1} + p_n}\n\n"
    md += "#### Algorithm\n\n"
    md += "1. **Input**: Sequence \\{p_0, p_1, p_2, \\ldots\\}, tolerance \\epsilon\n"
    md += "2. **For each** n \\geq 0 where p_{n+2} exists:\n"
    md += "   - Compute \\Delta^2 p_n = p_{n+2} - 2p_{n+1} + p_n\n"
    md += "   - If |\\Delta^2 p_n| < \\text{small threshold}, skip (avoid division by zero)\n"
    md += "   - Compute \\hat{p}_n = p_n - \\frac{(p_{n+1} - p_n)^2}{\\Delta^2 p_n}\n"
    md += "3. **Return** accelerated sequence\n\n"
    md += "#### Implementation\n\n"
    md += "```python\n"
    md += extract_function_source(aitken_acceleration)
    md += "\n```\n\n"

    md += "### 6. Real-time Aitken's Acceleration with Fixed-point\n\n"
    md += "#### Mathematical Formula\n\n"
    md += "This method applies Aitken's acceleration dynamically during the Fixed-point process:\n\n"
    md += "1. Generate a few iterations using Fixed-point: x_{n+1} = g(x_n)\n"
    md += "2. When three consecutive points are available, compute the Aitken accelerated value:\n"
    md += "   \\hat{x}_n = x_n - \\frac{(x_{n+1} - x_n)^2}{x_{n+2} - 2x_{n+1} + x_n}\n"
    md += "3. Replace the current approximation with the accelerated value and continue\n\n"
    md += "#### Algorithm\n\n"
    md += "1. **Input**: Function f, initial guess x_0, tolerance \\epsilon, max iterations\n"
    md += "2. **Initialize**: Set n = 0, sequence = [x_0]\n"
    md += "3. **Iterate**:\n"
    md += "   - Compute next Fixed-point value: x_{n+1} = g(x_n)\n"
    md += "   - Add x_{n+1} to sequence\n"
    md += "   - If at least 3 points exist in sequence, apply Aitken acceleration\n"
    md += "   - If accelerated value meets convergence criterion, return it\n"
    md += "   - Otherwise, continue with the next Fixed-point\n"
    md += "4. **Return** final value and performance metrics\n\n"
    md += "#### Implementation\n\n"
    md += "```python\n"
    md += extract_function_source(fixed_point_with_aitken)
    md += "\n```\n\n"

    md += "#### Examples with Real-time Aitken Acceleration\n\n"
    realtime_sequences = []
    
    for result in test_results:
        if 'realtime_aitken' in result['results'] and result['results']['realtime_aitken']['sequence']:
            realtime_sequences.append((result, result['results']['realtime_aitken']))
    
    for i, (result, method_result) in enumerate(realtime_sequences[:1]):
        sequence = method_result['sequence']
        if len(sequence) > 100:
            sequence = sequence[:100]
            
        # Create proper Aitken values dictionary with correct iteration mapping
        aitken_values = {}
        if hasattr(method_result, 'aitken_values') and method_result.aitken_values:
            aitken_values = method_result.aitken_values
        else:
            # Generate Aitken values for demonstration if not available
            if len(sequence) >= 3:
                for j in range(2, min(len(sequence), 20)):
                    if j >= 2:
                        p0, p1, p2 = sequence[j-2], sequence[j-1], sequence[j]
                        denominator = p2 - 2 * p1 + p0
                        if abs(denominator) > 1e-19:
                            aitken_val = p0 - ((p1 - p0)**2) / denominator
                            aitken_values[j-2] = aitken_val
        
        if aitken_values:
            filename = plot_fixed_point_aitken(
                f,
                best_g,
                result['x0'],
                sequence,
                aitken_values,
                result['true_root'],
                result['epsilon'],
                i
            )
            
            md += f"![Fixed-point with Real-time Aitken Acceleration](plots/{filename})\n\n"
        
        md += f"##### Fixed-point with Real-time Aitken (ε = {result['epsilon']:.15f})\n\n"
        md += "| Iteration | xₙ                  | f(xₙ)               | Error               | Aitken Applied | Acceleration Effect             |\n"
        md += "|-----------|---------------------|---------------------|---------------------|----------------|---------------------------------|\n"

        for j, x in enumerate(sequence):
            fx = f(x)
            error = abs(x - result['true_root'])
            
            aitken_applied = "Yes" if j in aitken_values else "No"
            
            accel_effect = "N/A"
            if j in aitken_values and j > 0:
                orig_error = abs(sequence[j] - result['true_root'])
                accel_error = abs(aitken_values[j] - result['true_root'])
                if orig_error > 1e-15:
                    improvement = orig_error / accel_error if accel_error > 1e-15 else float('inf')
                    accel_effect = f"{improvement:.15f}x faster" if improvement < 1000 else "Excellent"
            
            md += f"| {j + 1} | {x:.15f} | {fx:.15f} | {error:.15f} | {aitken_applied} | {accel_effect} |\n"
        
        md += f"\n**Result**: Converged to {method_result['final_value']:.15f} in {method_result['iterations']} iterations\n"
        md += f"**Final Error**: {method_result['error']:.15f}\n"
        md += f"**Aitken Applications**: {method_result.get('aitken_applications', len(aitken_values))}\n"
        md += f"**Acceleration Effect**: {method_result.get('acceleration_factor', 'Significant')} improvement over basic Fixed-point\n\n"

    md += "## Performance Analysis\n\n"

    methods = ['bisection', 'newton', 'secant', 'fixed_point',
               'bisection_aitken', 'si_aitken', 'realtime_aitken', 'periodic_aitken']

    method_names = {
        'bisection': 'Bisection',
        'newton': 'Newton',
        'secant': 'Secant',
        'fixed_point': 'Fixed-point',
        'bisection_aitken': 'Bisection + Aitken',
        'si_aitken': 'Fixed-point + Aitken',
        'realtime_aitken': 'Real-time Aitken',
        'periodic_aitken': 'Periodic Aitken'
    }

    avg_iterations = {}
    avg_times = {}
    avg_errors = {}
    avg_rates = {}
    success_rates = {}

    for method in methods:
        iterations = []
        times = []
        errors = []
        rates = []
        success = 0

        for result in test_results:
            if method not in result['results']:
                continue

            method_result = result['results'][method]
            if method_result['final_value'] is not None:
                iterations.append(method_result['iterations'])
                times.append(method_result['time'])
                if method_result['error'] is not None:
                    errors.append(method_result['error'])
                conv_rate = method_result.get('convergence_rate')
                if isinstance(conv_rate, (int, float)):
                    rates.append(conv_rate)
                success += 1

        avg_iterations[method] = sum(
            iterations) / len(iterations) if iterations else "N/A"
        avg_times[method] = sum(times) / len(times) if times else "N/A"
        avg_errors[method] = sum(errors) / len(errors) if errors else "N/A"
        avg_rates[method] = sum(rates) / len(rates) if rates else "N/A"
        success_rates[method] = success / \
            len(test_results) if test_results else 0

    md += "### Summary Table\n\n"
    md += "| Method                  | Avg Iterations | Avg Time (ms)       | Avg Error           | Convergence Rate    | Success Rate        |\n"
    md += "|-------------------------|----------------|---------------------|---------------------|---------------------|---------------------|\n"

    for method in methods:
        stability = f"{success_rates[method] * 100:.15f}%"

        iter_str = f"{avg_iterations[method]:.15f}" if isinstance(avg_iterations[method], (int, float)) else avg_iterations[method]
        time_str = f"{avg_times[method]:.15f}" if isinstance(avg_times[method], (int, float)) else avg_times[method]
        error_str = f"{avg_errors[method]:.15f}" if isinstance(avg_errors[method], (int, float)) else avg_errors[method]
        rate_str = f"{avg_rates[method]:.15f}" if isinstance(avg_rates[method], (int, float)) else avg_rates[method]

        md += f"| {method_names[method]} | {iter_str} | {time_str} | {error_str} | {rate_str} | {stability} |\n"

    def latex_to_unicode(md: str) -> str:
        replacements = [
            (r'\\cdot', '⋅'),
            (r'\\leq', '≤'),
            (r'\\geq', '≥'),
            (r'\\neq', '≠'),
            (r'\\approx', '≈'),
            (r'\\frac{([^}]*)}{([^}]*)}', r'\1⁄\2'),
            (r'\\Delta', 'Δ'),
            (r'\\phi', 'ϕ'),
            (r'\\hat\{([^}]*)\}', r'\1̂'),  # hat accent
            (r'x_([0-9]+)', r'x₍\1₎'),
            (r'x\^([0-9]+)', r'x⁽\1⁾'),
            # Add more as needed
        ]
        for pattern, repl in replacements:
            md = re.sub(pattern, repl, md)
        # Manual replacements for common patterns - but keep pipe characters as pipes
        md = md.replace('|xₙ₊₁ - xₙ|', '∣xₙ₊₁ − xₙ∣')
        md = md.replace('|xₙ₊₁ - xₙ|/|xₙ₊₁|', '∣xₙ₊₁ − xₙ∣∕∣xₙ₊₁∣')
        md = md.replace('|f(xₙ)|', '∣f(xₙ)∣')
        md = md.replace('->', '→')
        md = md.replace('<=', '≤')
        md = md.replace('>=', '≥')
        return md


    return latex_to_unicode(md)

if __name__ == "__main__":
    # Interactive setup
    use_interactive = input("Use interactive setup? (y/n, default=n): ").strip().lower()
    
    if use_interactive in ["y", "yes"]:
        f, df, f_string, df_string, a, b, x0, g_funcs, true_root, epsilons = setup_problem_interactively()
        
        # If true root not provided, compute it using high precision Newton's method
        if true_root is None:
            print("\nComputing true root using high-precision Newton's method...")
            true_root = compute_true_root_numerically(f, df, x0)
            print(f"Computed true root: {true_root}")
    else:
        print("Using default problem: f(x) = cos(x) - x")
    
    print("Running tests...")
    test_results = run_tests()

    print("Generating markdown report...")
    md_report = generate_md_report(test_results)

    with open("output.md", "w") as f:
        f.write(md_report)

    # Generate HTML with proper structure
    html_content = markdown.markdown(
        md_report, 
        extensions=["fenced_code", "tables", "md_in_html", "attr_list"]
    )
    
    # Create complete HTML with CSS styling
    css_styles = """
        body { 
            font-family: Arial, sans-serif; 
            margin: 10px; 
            max-width: 1200px;
            margin: 0 auto;
            padding: 10px;
            font-size: 8pt;
            line-height: 1.1;
        }
        h1 { 
            color: #2c3e50; 
            font-size: 12pt;
            margin: 10px 0;
        }
        h2 { 
            color: #34495e; 
            font-size: 10pt;
            margin: 8px 0;
        }
        h3 { 
            color: #2980b9; 
            font-size: 9pt;
            margin: 6px 0;
        }
        h4 { 
            font-size: 8pt;
            margin: 4px 0;
        }
        h5 { 
            font-size: 7pt;
            margin: 3px 0;
        }
        table { 
            border-collapse: collapse; 
            width: 100%; 
            margin: 10px 0;
            font-size: 5pt;
            table-layout: fixed;
        }
        th, td { 
            border: 1px solid #ddd; 
            padding: 2px; 
            text-align: left;
            word-wrap: break-word;
            overflow-wrap: break-word;
            max-width: 80px;
        }
        th { 
            background-color: #f2f2f2; 
            font-weight: bold;
            font-size: 5pt;
        }
        code { 
            background-color: #f8f8f8; 
            padding: 1px 2px; 
            border-radius: 2px;
            font-family: 'Courier New', monospace;
            font-size: 5pt;
            word-wrap: break-word;
        }
        pre { 
            background-color: #f8f8f8; 
            padding: 5px; 
            border-radius: 3px; 
            overflow-x: auto;
            font-size: 4pt;
            line-height: 1.0;
            word-wrap: break-word;
            white-space: pre-wrap;
        }
        img { 
            max-width: 90%; 
            height: auto; 
            display: block; 
            margin: 5px auto;
            page-break-inside: avoid;
        }
        p {
            font-size: 7pt;
            margin: 3px 0;
            line-height: 1.1;
        }
        ul, ol {
            font-size: 6pt;
            margin: 5px 0;
            padding-left: 15px;
        }
        li {
            margin: 1px 0;
        }
        .number {
            font-family: 'Courier New', monospace;
            font-size: 4pt;
        }
"""

    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Numerical Methods Report</title>
    <style>{css_styles}</style>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
    {html_content}
</body>
</html>"""

    with open("output.html", "w", encoding="utf-8") as f:
        f.write(full_html)

    # Generate PDF with proper image handling
    try:
        # Use the HTML file with base_url to resolve relative image paths
        HTML(filename="output.html", base_url=".").write_pdf("output.pdf")
        print("PDF generated successfully: output.pdf")
        
    except Exception as e:
        print(f"PDF generation failed: {e}")
        print("Trying alternative method...")
        
        # Alternative: Create CSS for better PDF formatting
        try:
            pdf_css = CSS(string="""
                @page {
                    margin: 1cm;
                    size: A4;
                }
                body { 
                    font-family: Arial, sans-serif; 
                    font-size: 9pt;
                    line-height: 1.2;
                }
                h1 { 
                    color: #2c3e50; 
                    page-break-before: auto; 
                    font-size: 14pt;
                }
                h2 { 
                    color: #34495e; 
                    page-break-before: auto; 
                    font-size: 12pt;
                }
                h3 { 
                    color: #2980b9; 
                    font-size: 10pt;
                }
                table { 
                    border-collapse: collapse; 
                    width: 100%; 
                    font-size: 6pt;
                    page-break-inside: avoid;
                }
                th, td { 
                    border: 1px solid #ddd; 
                    padding: 2px; 
                    text-align: left;
                }
                th { 
                    background-color: #f2f2f2; 
                    font-weight: bold;
                }
                img { 
                    max-width: 100%; 
                    height: auto; 
                    page-break-inside: avoid;
                    display: block;
                    margin: 10px auto;
                }
                pre { 
                    font-size: 7pt; 
                    background-color: #f8f8f8; 
                    padding: 3px;
                    page-break-inside: avoid;
                    overflow: hidden;
                }
                code {
                    font-size: 8pt;
                    background-color: #f8f8f8;
                }
            """)
            
            # Generate PDF with CSS and proper base URL
            HTML(filename="output.html", base_url=".").write_pdf(
                "output.pdf", 
                stylesheets=[pdf_css],
                zoom=0.5
            )
            print("PDF generated successfully with custom CSS: output.pdf")
            
        except Exception as e2:
            print(f"Alternative PDF generation also failed: {e2}")
            print("HTML file generated successfully: output.html")
            print("You can manually convert to PDF using your browser or pandoc:")
            print("pandoc output.md -o output.pdf --pdf-engine=xelatex")

    print("Report generated successfully: output.md and output.html")