import argparse
import os
import time
from typing import List, Optional, Tuple

import numpy as np


class NumMatrix:
    def __init__(self, matrix: np.ndarray, row_sums: np.ndarray, col_sums: np.ndarray, verbose: bool):
        # input: matrix and the target rows and cols sums. verbose for printing the steps
        self.matrix = matrix
        self.row_sums = row_sums
        self.col_sums = col_sums
        self.verbose = verbose

        # number of rows and columns
        self.n, self.m = self.matrix.shape

        # mask matrix of the matrix
        # -1: default value, currently we don't it's 0 or the number
        # 0: zero
        # 1: the number
        self.masks = np.full((self.n, self.m), -1, dtype=int)

        # current sums of the matrix based on changing masks matrix
        # default: zero
        self.row_current_sum = np.zeros(self.n, dtype=int)
        self.col_current_sum = np.zeros(self.m, dtype=int)

        # sum of remaining sum based on chaning masks matrix
        self.row_remaining_sum = np.sum(self.matrix, axis=1).astype(int)
        self.col_remaining_sum = np.sum(self.matrix, axis=0).astype(int)

        # degrees matrix for heuristics
        self.degrees = np.full(
            (self.n, self.m), self.n + self.m - 2, dtype=int)

        # list of elements (variables) in order for selection
        self.variables = [(i, j) for i in range(self.n)
                          for j in range(self.m)]

    def print_current(self):
        # print current matrix based on masks matrix
        # we store it to a string then print it because of text tearing
        os.system('clear' if os.name == 'posix' else 'cls')
        text = ''
        for i in range(self.n):
            for j in range(self.m):
                # if mask == 1 then we keep the number
                if self.masks[i, j] == 1:
                    text += f'{self.matrix[i, j]} '

                # if mask == 0 then it's zero
                elif self.masks[i, j] == 0:
                    text += '0 '

                else:
                    text += '□ '

            text += '\n'

        print(text)

    def select_variable(self) -> Optional[Tuple[Tuple[int, int], List[int]]]:
        min_options = np.inf
        candidates = []

        for row, col in self.variables:
            # check next element if the value of the element is known
            if self.masks[row, col] != -1:
                continue

            val = self.matrix[row, col]

            # subtract the element from remaining_sum, because we are going to give it a value

            max_possible_row = self.row_remaining_sum[row] - val
            max_possible_col = self.col_remaining_sum[col] - val

            possible_values = []
            # possible values, first we keep it and in second iter we zero it
            for mask in (1, 0):
                # val: 1 -> keep and val: 0 -> zero
                new_val = val * mask

                # add the element to current_sum because the element have a value now
                new_row_sum = self.row_current_sum[row] + new_val
                new_col_sum = self.col_current_sum[col] + new_val

                # the value is invalid if the new current_sum exceeds the target sum
                if new_row_sum > self.row_sums[row] or new_col_sum > self.col_sums[col]:
                    continue

                # calculate how much of the target sum is left to find
                remaining_row = self.row_sums[row] - new_row_sum
                remaining_col = self.col_sums[col] - new_col_sum

                # the valus is invalid if we can't reach the target sum (remaining) with the remaining elements in matrix
                # the remaining elements in matrix are elements with -1's in masks matrix
                if remaining_row > max_possible_row or remaining_col > max_possible_col:
                    continue

                # if the conditions we says holds, it's a candidate
                possible_values.append(mask)

            num_possible = len(possible_values)

            # we don't continue if there is a element that have no value
            # there is a problem with previous selections
            if num_possible == 0:
                return None, None

            # if the values of the element is fewer than other elements have found
            # we discard other candidates
            if num_possible < min_options:
                min_options = num_possible
                candidates = [((row, col), possible_values)]

            elif num_possible == min_options:
                candidates.append(((row, col), possible_values))

            # we discard elements with more values too

        if not candidates:
            return None, None

        return max(candidates, key=lambda var: self.degrees[var[0]])

    def update_degree(self, var: Tuple[int, int], delta: int):
        row, col = var

        # update degrees for unassigned variables in the same row
        row_mask = (self.masks[row, :] == -1)
        # row_mask[col] = False
        self.degrees[row, row_mask] += delta

        # update degrees for unassigned variables in the same column
        col_mask = (self.masks[:, col] == -1)
        # col_mask[row] = False
        self.degrees[col_mask, col] += delta

    def forward_checking(self, var: Tuple[int, int], mask: int) -> bool:
        row, col = var

        # check all unassigned variables in the same row
        for j in range(self.m):
            if self.masks[row, j] == -1 and j != col:
                val = self.matrix[row, j]
                max_possible_row = self.row_remaining_sum[row] - val
                flag = True
                # determine if there's at least one possible value for the variable
                for mask in (1, 0):
                    new_val = val * mask
                    new_row_sum = self.row_current_sum[row] + new_val
                    if new_row_sum > self.row_sums[row]:
                        continue

                    remaining_row = self.row_sums[row] - new_row_sum
                    if remaining_row > max_possible_row:
                        continue

                    flag = False
                    break

                if flag:
                    return False

        # check all unassigned variables in the same column
        for i in range(self.n):
            if self.masks[i, col] == -1 and i != row:
                val = self.matrix[i, col]
                max_possible_col = self.col_remaining_sum[col] - val

                flag = True
                for mask in (1, 0):
                    new_val = val * mask
                    new_col_sum = self.col_current_sum[col] + new_val
                    if new_col_sum > self.col_sums[col]:
                        continue

                    remaining_col = self.col_sums[col] - new_col_sum
                    if remaining_col > max_possible_col:
                        continue

                    flag = False
                    break

                if flag:
                    return False

        return True

    def lcv(self, var: Tuple[int, int], domain: List[int]) -> List[int]:
        row, col = var
        impacts = [np.inf, np.inf]
        for mask in domain:
            impact = 0
            for j in range(self.m):
                if self.masks[row, j] == -1 and j != col:
                    cell_val = self.matrix[row, j]
                    if self.row_current_sum[row] + cell_val > self.row_sums[row]:
                        impact += 1

            for i in range(self.n):
                if self.masks[i, col] == -1 and i != row:
                    cell_val = self.matrix[i, col]
                    if self.col_current_sum[col] + cell_val > self.col_sums[col]:
                        impact += 1

            impacts[mask] = impact

        return impacts

    def backtrack(self) -> bool:
        # end the process if all elements have value
        if np.all(self.masks != -1):
            return True

        # select an element that have fewer value among elements
        var, domain = self.select_variable()

        # no element found, so there is a problem with previous selections
        if var is None:
            return False

        row, col = var

        val = self.matrix[row, col]
        # impacts = self.lcv(var, domain)
        # domain.sort(key=lambda mask: impacts[mask])

        for mask in domain:
            # val: 1 -> keep and val: 0 -> zero
            new_val = val * mask

            # put tha value in masks matrix
            self.masks[row, col] = mask

            # update the current_sum
            self.row_current_sum[row] += new_val
            self.col_current_sum[col] += new_val

            # update the remaining_sum
            self.row_remaining_sum[row] -= val
            self.col_remaining_sum[col] -= val

            # update degrees
            self.update_degree(var, -1)

            # forward checking
            # if a variable have no value in its domain
            # there is a problem in previous selection
            if not self.forward_checking(var, mask):
                # unset the value in masks matrix
                self.masks[row, col] = -1

                # undo the current_sum
                self.row_current_sum[row] -= new_val
                self.col_current_sum[col] -= new_val

                # undo the remaining_sum
                self.row_remaining_sum[row] += val
                self.col_remaining_sum[col] += val

                # undo the degree update
                self.update_degree(var, +1)

                # check next mask
                continue

            # print the matrix in each backtracking step
            if self.verbose:
                self.print_current()

            # backtrack!
            if self.backtrack():
                return True

            # if self.backtrack() returned False, that means there is a problem with previous selections
            # so we unset this value and reset current_sum and remaining_sum

            # unset the value in masks matrix
            self.masks[row, col] = -1

            # undo the current_sum
            self.row_current_sum[row] -= new_val
            self.col_current_sum[col] -= new_val

            # undo the remaining_sum
            self.row_remaining_sum[row] += val
            self.col_remaining_sum[col] += val

            # undo the degree update
            self.update_degree(var, +1)

        # there is a problem with previous selections
        return False

    def solve(self) -> Optional[np.ndarray]:
        # call result and return masks matrix
        result = self.backtrack()
        if result:
            return self.masks

        else:
            return None


def check_solution(solution: np.ndarray, row_sums: np.ndarray, col_sums: np.ndarray) -> bool:
    # check if the sum of rows and cols of solutions are equal to target sums
    return np.array_equal(np.sum(solution, axis=1), row_sums) and \
        np.array_equal(np.sum(solution, axis=0), col_sums)


def read_puzzle(filepath: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    with open(filepath, 'r') as f:
        # first line is size
        size = list(map(int,
                        f.readline().strip().split(',')))
        # if there is only one number, we assume it's a square matrix
        if len(size) == 1:
            size = size * 2

        # second line is row sums
        row_sums = np.array(
            list(map(int, f.readline().strip().split(','))), dtype=int)

        # third line is col sums
        col_sums = np.array(
            list(map(int, f.readline().strip().split(','))), dtype=int)

        # remaining lines are rows of matrix
        matrix = np.array([
            list(map(int, f.readline().strip().split(',')))
            for _ in range(size[0])
        ], dtype=int)

    return matrix, row_sums, col_sums


def write_puzzle(matrix: np.ndarray, filepath: str) -> None:
    # write in format a11,a12,a13...a1m
    #                 a21,a22,a23...a2m
    #                 .................
    #                 an1,an2,an2...anm
    with open(filepath, 'w') as f:
        for i in range(matrix.shape[0]):
            f.write(','.join(map(str,
                                 matrix[i, :])) + '\n')


def main():
    parser = argparse.ArgumentParser(description='number puzzle with csp')
    parser.add_argument('-f', default='puzzle.txt',
                        type=str, help='filepath to the puzzle')
    parser.add_argument('-v', default=False,
                        action='store_true', help='verbose mode')
    args = parser.parse_args()

    matrix, row_sums, col_sums = read_puzzle(args.f)

    solver = NumMatrix(matrix, row_sums, col_sums, verbose=args.v)

    now = time.time()
    solution = solver.solve()
    print(f'I found the solution in {time.time() - now} seconds')

    if solution is not None:
        masked = matrix * np.array(solution)
        print(masked)
        if check_solution(masked, row_sums, col_sums):
            write_puzzle(masked, 'solution.txt')
            print('Solution is valid')

        else:
            print('Solution is not valid')

    else:
        print('No solution found')


if __name__ == '__main__':
    main()
