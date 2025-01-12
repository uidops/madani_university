import os
import time
from typing import List

import numpy

settings = {
    "characters": ["X", "O", "DRAW"]
}

x = 2


def count_scores(line: List[str]) -> List[int]:
    score = [0, 0]
    count = [0, 0]

    for cell in line:
        if cell == settings["characters"][0]:
            if count[1] >= 3:
                score[1] += 2 * count[1] - 5

            count[1] = 0
            count[0] += 1

        elif cell == settings["characters"][1]:
            if count[0] >= 3:
                score[0] += 2 * count[0] - 5

            count[0] = 0
            count[1] += 1

        else:
            return (-1, -1)

    if count[0] >= 3:
        score[0] += 2 * count[0] - 5

    if count[1] >= 3:
        score[1] += 2 * count[1] - 5

    return score


def calculate_scores(board: numpy.ndarray) -> int:
    n = board.shape[0]
    score = [0, 0]

    for i in range(n):  # ROW
        score = list(map(sum,
                         zip(count_scores(board[i]),
                             score)))

    for j in range(n):  # COL
        score = list(map(sum,
                         zip(count_scores(board[:, j]),
                             score)))

    # Down-left diagonals
    for offset in range(-n + 1, n):
        score = list(map(sum,
                         zip(count_scores(board.diagonal(offset)),
                             score)))

    # Down-right diagonals
    board_90 = numpy.rot90(board)
    for offset in range(-n + 1, n):
        score = list(map(sum,
                     zip(count_scores(board_90.diagonal(offset)),
                         score)))

    return score


def who_won(board: numpy.ndarray):
    if numpy.any(board == " "):
        return -1

    score = calculate_scores(board)

    winer = 0
    if score[1] > score[0]:
        winer = 1
    elif score[1] == score[0]:
        winer = 2

    return winer


def print_board(board: numpy.ndarray):
    os.system("clear")
    size = board.shape[0] * 5 + 1
    print('⎯' * size)
    for i in range(board.shape[0]):
        print(
            ' '.join([f'｜ {board[i, j]}' for j in range(board.shape[1])]), end=" ｜\n")
        print('⎯' * size)


def min_value(board: numpy.ndarray, alpha: float, beta: float, depth: int):
    moves = list(zip(*numpy.where(board == " ")))
    moves.sort(reverse=True)
    if not any(moves):
        x_score, o_score = calculate_scores(board)
        # print(board)
        # print(f'alpha: {alpha} , beta = {beta} , v = {x_score - o_score}')
        return x_score - o_score, [-1, -1]

    best_score = numpy.inf
    best_move = [-1, -1]

    for i, j in moves:
        board[i, j] = settings["characters"][0]
        score, _ = max_value(board, alpha, beta, depth + 1)

        if score < best_score:
            best_move = [i, j]
            best_score = score

        if best_score <= alpha:
            if len(moves) == 3:
                print(board)
                print(f'alpha: {alpha} , beta = {beta} , v = {score}')
                print('pruned\n\n')
            board[i, j] = " "
            return best_score, best_move

        board[i, j] = " "
        beta = min(beta, best_score)

        # print(board)
        # print(f'alpha: {alpha} , beta = {beta} , v = {score}')

    return best_score, best_move


def max_value(board: numpy.ndarray, alpha: float, beta: float, depth: int):
    moves = list(zip(*numpy.where(board == " ")))
    moves.sort(reverse=True)
    if not any(moves):
        x_score, o_score = calculate_scores(board)
        # print(board)
        # print(f'alpha: {alpha} , beta = {beta} , v = {o_score - x_score}')
        return o_score - x_score, [-1, -1]

    best_score = -numpy.inf
    best_move = [-1, -1]

    # board = board.copy()
    for i, j in moves:
        board[i, j] = settings["characters"][1]
        score, _ = min_value(board, alpha, beta, depth + 1)
        if score > best_score:
            best_move = [i, j]
            best_score = score

        if best_score >= beta:
            if len(moves) == 3:
                print(board)
                print(f'alpha: {alpha} , beta = {beta} , v = {score}')
                print('pruned\n\n')
            board[i, j] = " "
            return best_score, best_move

        board[i, j] = " "
        alpha = max(alpha, best_score)
        # print(board)
        # print(f'alpha: {alpha} , beta = {beta} , v = {score}')

    return best_score, best_move


n = 4
board = numpy.full((n, n), " ")

board = numpy.array([['X', 'O', 'X'], ['O', 'X', ' '], [' ', ' ', ' ']])

print(max_value(board, -numpy.inf, numpy.inf, 0))

exit()

v = -numpy.inf
who = 0
while (v < 0):
    print_board(board)

    if who == 0:
        choice = input("i,j >> ").split(",")
        i, j = int(choice[0]), int(choice[1])
        board[i, j] = settings["characters"][who]

    else:
        i, j = max_value(board, -numpy.inf, numpy.inf, numpy.inf)[1]
        print(i, j)
        board[i, j] = settings["characters"][who]
        time.sleep(1)

    who ^= 1
    v = who_won(board)

print(board)

if v >= 0:
    print(settings["characters"][v])

else:
    print("Game is not over")
