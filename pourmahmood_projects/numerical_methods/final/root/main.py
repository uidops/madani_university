#!/usr/bin/env python3

import inspect
import math


def func_to_string_simple(func):
    try:
        source = inspect.getsource(func)

        lines = source.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('lambda'):
                expression = line[10:-1].strip()
                return expression

        return func.__name__ if hasattr(func, '__name__') else "unknown_function"

    except Exception:
        return getattr(func, '__name__', "unknown_function")


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
    best_error = float('inf')

    for i, g in enumerate(all_g_functions):
        if i < len(custom_g_functions or []):
            g_name = f"User {i + 1}"
        else:
            g_name = func_to_string_simple(g)

        converges, error = evaluate_g_function(g, f, x0)

        convergence_status = "Yes" if converges else "No"
        error_str = f"{error:.10f}" if error != float('inf') else "∞"

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

    results['bisection'] = {'sequence': sequence, 'iterations': len(sequence)}
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

    results['newton'] = {'sequence': sequence, 'iterations': len(sequence)}
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

    results['secant'] = {'sequence': sequence, 'iterations': len(sequence)}
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
                f"{i + 1: <4} {xk: <20.10f} {fxk: <15.2e} {aitken_val: <20.10f} {f_aitken: <15.2e}")
        else:
            print(
                f"{i + 1: <4} {xk: <20.10f} {fxk: <15.2e} {'N/A': <20} {'N/A': <15}")

    print(f"\nStopping condition: {stopping_reason}")
    print(f"Total iterations: {len(sequence)}")

