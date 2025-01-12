import argparse
import os
import time
from typing import List, Optional, Tuple

import numpy as np


class NumMatrix:
    def __init__(self, matrix: np.ndarray, row_sums: np.ndarray, col_sums: np.ndarray, verbose: bool):
        self.matrix = matrix
        self.row_sums = row_sums
        self.col_sums = col_sums
        self.verbose = verbose

        self.n, self.m = self.matrix.shape

        self.assignment = np.full((self.n, self.m), -1, dtype=int)

        self.row_current_sum = [0] * self.n
        self.col_current_sum = [0] * self.m

        self.row_remaining_cells_sum = list(np.sum(self.matrix, axis=1))
        self.col_remaining_cells_sum = list(np.sum(self.matrix, axis=0))

        self.degrees = np.full(
            (self.n, self.m), self.n + self.m - 2, dtype=int)

        self.variables_sorted = sorted(
            [(i, j) for i in range(self.n) for j in range(self.m)],
            key=lambda var: self.degrees[var])

    def print_current(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        text = ''
        for i in range(self.n):
            for j in range(self.m):
                if self.assignment[i, j] == 1:
                    text += str(self.matrix[i, j]) + ' '

                elif self.assignment[i, j] == 0:
                    text += '0 '

                else:
                    text += '? '

            text += '\n'

        print(text)

    def select_unassigned_variable(self) -> Optional[Tuple[int, int]]:
        min_options = 3
        candidates = []

        for row, col in self.variables_sorted:
            if self.assignment[row, col] != -1:
                continue

            val = self.matrix[row, col]

            max_possible_row = self.row_remaining_cells_sum[row] - val
            max_possible_col = self.col_remaining_cells_sum[col] - val

            feasible_values = []
            for mask in (1, 0):
                new_val = val * mask

                new_row_sum = self.row_current_sum[row] + new_val
                new_col_sum = self.col_current_sum[col] + new_val

                if new_row_sum > self.row_sums[row] or new_col_sum > self.col_sums[col]:
                    continue

                remaining_row = self.row_sums[row] - new_row_sum
                remaining_col = self.col_sums[col] - new_col_sum

                if remaining_row > max_possible_row or remaining_col > max_possible_col:
                    continue

                feasible_values.append(mask)

            num_options = len(feasible_values)
            if num_options < min_options:
                min_options = num_options
                candidates = [(row, col)]

            elif num_options == min_options:
                candidates.append((row, col))

            if min_options == 0:
                break

        if not candidates:
            return None

        return max(candidates,
                   key=lambda var: self.degrees[var])

    def update_degree(self, pos: Tuple[int, int], delta: int):
        row, col = pos
        unassigned_col = (self.assignment[:, col] == -1)
        self.degrees[unassigned_col, col] += delta

        unassigned_row = (self.assignment[row, :] == -1)
        self.degrees[row, unassigned_row] += delta

    def backtrack(self) -> bool:
        if np.all(self.assignment != -1):
            return True

        var = self.select_unassigned_variable()
        if var is None:
            return False

        row, col = var
        val = self.matrix[row, col]

        max_possible_row = self.row_remaining_cells_sum[row] - val
        max_possible_col = self.col_remaining_cells_sum[col] - val

        for mask in (1, 0):
            new_val = val * mask

            new_row_sum = self.row_current_sum[row] + new_val
            new_col_sum = self.col_current_sum[col] + new_val

            if new_row_sum > self.row_sums[row] or new_col_sum > self.col_sums[col]:
                continue

            remaining_row = self.row_sums[row] - new_row_sum
            remaining_col = self.col_sums[col] - new_col_sum

            if remaining_row > max_possible_row or remaining_col > max_possible_col:
                continue

            self.assignment[row, col] = mask

            self.row_current_sum[row] += new_val
            self.col_current_sum[col] += new_val

            self.row_remaining_cells_sum[row] -= val
            self.col_remaining_cells_sum[col] -= val

            self.update_degree(var, -1)

            if self.verbose:
                self.print_current()

            if self.backtrack():
                return True

            self.assignment[row, col] = -1

            self.row_current_sum[row] -= new_val
            self.col_current_sum[col] -= new_val

            self.row_remaining_cells_sum[row] += val
            self.col_remaining_cells_sum[col] += val

            self.update_degree(var, +1)

        return False

    def solve(self) -> Optional[List[List[int]]]:
        result = self.backtrack()
        if result:
            return self.assignment.tolist()

        else:
            return None


def check_solution(solution: np.ndarray, row_sums: np.ndarray, col_sums: np.ndarray) -> bool:
    return np.array_equal(np.sum(solution, axis=1), row_sums) and \
        np.array_equal(np.sum(solution, axis=0), col_sums)


def read_puzzle(filepath: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    with open(filepath, 'r') as f:
        size = list(map(int,
                        f.readline().strip().split(',')))
        if len(size) == 1:
            size = size * 2

        row_sums = np.array(
            list(map(int, f.readline().strip().split(','))), dtype=int)

        col_sums = np.array(
            list(map(int, f.readline().strip().split(','))), dtype=int)

        matrix = np.array([
            list(map(int, f.readline().strip().split(',')))
            for _ in range(size[0])
        ], dtype=int)

    return matrix, row_sums, col_sums


def write_puzzle(matrix: np.ndarray, filepath: str) -> None:
    with open(filepath, 'w') as f:
        for i in range(matrix.shape[0]):
            f.write(','.join(map(str,
                                 matrix[i, :])) + '\n')


def main():
    parser = argparse.ArgumentParser(description='number puzzle with csp')
    # parser.add_argument('filepath', type=str, help='filepath to puzzle')
    parser.add_argument('-v', action='store_true', help='verbose mode')
    args = parser.parse_args()

    # matrix, row_sums, col_sums = read_matrix(args.filepath)
    matrix, row_sums, col_sums = read_puzzle('puzzle.txt')

    solver = NumMatrix(matrix, row_sums, col_sums, verbose=args.v)

    now = time.time()
    solution = solver.solve()
    print(f'I found the solution in {time.time() - now} seconds')

    if solution is not None:
        v = matrix * np.array(solution)
        print(v)
        if check_solution(v, row_sums, col_sums):
            write_puzzle(v, 'solution.txt')
            print('Solution is valid')

        else:
            print('Solution is not valid')

    else:
        print('No solution found')


if __name__ == '__main__':
    main()
