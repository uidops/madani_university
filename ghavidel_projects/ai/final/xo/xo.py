import os
import random
import string
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple

import numpy as np

settings = {
    'characters': ['X', 'O', ' '],  # first character is human
    'size': 10,  # size of the board
    'min_simulations': 10,  # min simulations when we are sure
    'max_simulations': 100,  # max simulations when depth reached
    'max_depth': 9,  # max depth for end of game
    'top_moves': 1,  # limit the number of nodes in each depth
    'max_workers': os.cpu_count(),  # max workers for parallel game simulations
}


def print_board(board: np.ndarray) -> None:
    n = board.shape[0]

    # 4 = (1 player char) + (2 dim char) + (1 space char)
    # and we have n cells per row
    line_size = n * 4 + 1

    os.system('clear' if os.name == 'posix' else 'cls')

    # print the column numbers and top line
    print('    ' + ''.join(f'{i}   ' for i in range(1, n + 1)))
    print('  ' + '─' * line_size)

    for row in range(n):
        # format each row in form "a-z | A | B | C | D | .... |"
        # and print the line after each row
        srow = '｜'.join([f' {board[row, col]}' for col in range(n)])
        print(f'{string.ascii_lowercase[row]} ｜{srow}｜')
        print('  ' + '─' * line_size)


def count_score(line: np.ndarray) -> List[int]:
    scores = [0, 0]  # human, AI
    counts = [0, 0]  # human, AI
    for char in line:
        if char == settings['characters'][0]:  # when reached human
            # calculate the score of AI if there is any then count the human
            # max is because if counts is below 3,
            # it'll be negative and that means the score is zero
            scores[1] += max(0, 2 * counts[1] - 5)
            counts[1] = 0

            counts[0] += 1

        elif char == settings['characters'][1]:  # when reached AI
            # calculate the score of human if there is any then count the AI
            scores[0] += max(0, 2 * counts[0] - 5)
            counts[0] = 0

            counts[1] += 1

        else:  # when reached empty cell
            # calculate scores of both human and AI
            # then reset the counter
            scores[0] += max(0, 2 * counts[0] - 5)
            scores[1] += max(0, 2 * counts[1] - 5)

            counts = [0, 0]

    # calculate scores of both human and AI in the end of counting
    scores[0] += max(0, 2 * counts[0] - 5)
    scores[1] += max(0, 2 * counts[1] - 5)

    return scores


def calculate_scores(board: np.ndarray) -> List[int]:
    n = board.shape[0]
    total_score = [0, 0]  # human, AI

    for i in range(n):
        row_score = count_score(board[i, :])
        col_score = count_score(board[:, i])

        # zip makes a tuple of elements of arrays with same index
        # and makes it easy to summation. a functional method.
        total_score = list(map(sum,
                               zip(total_score, row_score, col_score)))

    # flip the board horizontally.
    # it changes the order of cloumns from first-to-last to last-to-first
    # this makes it easy to extract counter-diagonals
    # as they will be main-diagonals of the flipped matrix
    board_flipped = np.fliplr(board)
    for k in range(-n + 1, n):
        main_diag_score = count_score(board.diagonal(k))
        counter_diag_score = count_score(board_flipped.diagonal(k))

        total_score = list(map(sum,
                               zip(total_score, main_diag_score, counter_diag_score)))

    return total_score


def who_won(board: np.ndarray) -> Tuple[int, List[int]]:
    # the game is not over yet if there is an empty cell
    if np.any(board == settings['characters'][2]):
        return -1, [0, 0]

    score = calculate_scores(board)

    # human > AI, human
    if score[0] > score[1]:
        return 0, score

    # human < AI, AI
    elif score[0] < score[1]:
        return 1, score

    # human == AI, draw
    return 2, score


def simulate_game(board: np.ndarray, player: int) -> int:
    # copy of the board
    # this avoids memory manipulation from another threads
    # and the main board remains unchanged
    board = board.copy()

    current_player = player
    winner, score = who_won(board)
    # empty cells are allowed moves
    # np.where returns tuple of two array that
    # first element is row indices array
    # second element is column indices array
    # by zip, we convert indices to a (row, column) array
    moves = list(zip(*np.where(board == settings['characters'][2])))
    # play the game randomly until the game is over
    while winner == -1 or any(moves):
        # choose a move randomly from allowed moves
        # and place the char of palyer in board
        move = random.choice(moves)
        board[move] = settings['characters'][current_player]
        moves.remove(move)

        # toggle the current player (switches between 0 and 1)
        # 0^1 -> 1  ,  1^1 -> 0
        # we use xor for this because it's fast
        current_player ^= 1
        winner, score = who_won(board)

    # human - AI if we are in min depth (player is AI)
    # AI - human if we are in max depth (player is human)
    return score[player ^ 1] - score[player]


def monte_carlo_evaluation(board: np.ndarray, player: int, simulations: int) -> float:
    # run simulate_game 'simulations' times parallely
    # and return the avarage score
    results = []
    with ThreadPoolExecutor(max_workers=settings['max_workers']) as executor:
        results = executor.map(
            simulate_game, [board] * simulations, [player] * simulations)

    return sum(results) / simulations


def order_moves(board: np.ndarray, moves: List[Tuple[int, int]], player: int) -> List[Tuple[int, int]]:
    # sort moves based on current score of board
    def heuristic_key(move):
        board[move] = settings['characters'][player]
        # scores = calculate_scores(board)
        scores = monte_carlo_evaluation(
            board, player ^ 1, settings['max_simulations'])
        board[move] = settings['characters'][2]
        return scores

    moves.sort(key=heuristic_key, reverse=True)
    return moves[:settings['top_moves']]


def max_value(board: np.ndarray, alpha: float, beta: float, depth: int) -> Tuple[float, Tuple[int]]:
    # empty cells are allowed moves
    moves = list(zip(*np.where(board == settings['characters'][2])))

    # random select early moves (first three moves)
    if (settings['size'] ** 2) - len(moves) < 3:
        return -1, random.choice(moves)

    # call monte-carlo if depth is reached or game is over
    if depth <= 0 or not any(moves):
        # use max_simulations when depth is limited else use the min_simulations
        simulations = settings['max_simulations'] if depth == 0 else settings['min_simulations']
        return monte_carlo_evaluation(board, 1, simulations), (-1, -1)

    best_score = -np.inf
    best_move = (-1, -1)

    # sort moves based on scores
    # this makes alpha-beta pruning works better
    moves = order_moves(board, moves, 1)
    for move in moves:
        board[move] = settings['characters'][1]
        score, _ = min_value(board, alpha, beta, depth - 1)

        # reset board to previous state
        board[move] = settings['characters'][2]

        # maximizing score
        if score > best_score:
            best_score = score
            best_move = move

        # alpha-beta pruning
        if best_score >= beta:
            return best_score, best_move

        alpha = max(alpha, best_score)

    return best_score, best_move


def min_value(board: np.ndarray, alpha: float, beta: float, depth: int) -> Tuple[float, Tuple[int]]:
    global pruned
    # empty cells are allowed moves
    moves = list(zip(*np.where(board == settings['characters'][2])))

    # call monte-carlo if depth is reached or game is over
    if depth <= 0 or not any(moves):
        # use max_simulations when depth is limited else use the min_simulations
        simulations = settings['max_simulations'] if depth == 0 else settings['min_simulations']
        return monte_carlo_evaluation(board, 0, simulations), (-1, -1)

    best_score = np.inf
    best_move = (-1, -1)

    # sort moves based on scores
    # this makes alpha-beta pruning works better
    moves = order_moves(board, moves, 0)
    for move in moves:
        board[move] = settings['characters'][0]
        score, _ = max_value(board, alpha, beta, depth - 1)

        # reset board to previous state
        board[move] = settings['characters'][2]

        # minimzing score
        if score < best_score:
            best_score = score
            best_move = move

        # alpha-beta pruning
        if best_score <= alpha:
            return best_score, best_move

        beta = min(beta, best_score)

    return best_score, best_move


def main():
    # shape of the board from settings
    n = settings['size']

    # create a full n*n board with empty character
    board = np.full((n, n), settings['characters'][2])

    # we choose first player randomly
    # 0 -> human   ,   1 -> AI
    who = random.randint(0, 1)

    # winner -> -1 game is not over
    # winner -> 0 human won
    # winner -> 1 AI won
    # winner -> 2 draw
    winner = -1
    while winner == -1:
        # print the board before choosing
        print_board(board)

        # human's turn
        if who == 0:
            # loop until user enters a valid move
            while True:
                try:
                    choice = input(
                        "Enter your move as 'ij' (example: a1): ").strip()

                    # row is from lowercase characters
                    # col is from 1 to n, -1 because the index starts from 0
                    i, j = string.ascii_lowercase.index(choice[0]), \
                        int(choice[1:]) - 1

                    # if i and j are in valid range and the cell is empty, then put the character of human into the cell
                    if (0 <= i < n) and (0 <= j < n) and board[i, j] == settings['characters'][2]:
                        board[i, j] = settings['characters'][0]
                        break

                    else:
                        print('Invalid move')

                except Exception:
                    print('Invalid input format')

        # AI's turn
        else:
            print("I'm thinking...")

            # to measure the move making from ai
            now = time.time()

            # use 9 as depth if number of remaining empty cells are below 9 (like it's 3x3)
            depth = settings['max_depth'] if (
                board == settings['characters'][2]).sum() <= 9 else 9

            # call max_value for a move that maximize the score of AI
            _, move = max_value(board, -np.inf, np.inf, depth)
            if move == (-1, -1):
                print("AI couldn't make a move!")
                break

            print(f'AI made a move in {time.time() - now: .2f} seconds')
            time.sleep(2)

            # put the character of AI into the cell
            board[move] = settings['characters'][1]

        # toggle the current player (switches between 0 and 1)
        # 0^1 -> 1  ,  1^1 -> 0
        # we use xor for this because it's fast
        who ^= 1

        # update winner after each move from human or AI
        winner, _ = who_won(board)

    # print the board when game is over and announce the winner
    print_board(board)
    human, ai = calculate_scores(board)
    print(f'human = {human}   ai = {ai}')
    if winner == 0:
        print('You won!')

    elif winner == 1:
        print('AI won!')

    else:
        print('draw!')


if __name__ == '__main__':
    main()
