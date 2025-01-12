
import sys
import math
import os
import random
import string
import time
from typing import List, Tuple

import numpy as np
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QGridLayout,
    QMessageBox,
    QLabel,
    QVBoxLayout,
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

# Game settings
settings = {
    # first player is human
    'characters': ['X', 'O', ' '],
    'size': 4,
    'simulations': 600,
    'depth': 2
}


def print_board(board: np.ndarray) -> None:
    # because it's a square matrix, we ignore the second dimension
    n = board.shape[0]
    line_size = n * 4 + 1  # 4 = 3 characters + 1 separator

    os.system('clear')  # Use 'cls' if on Windows

    print('    ' + ''.join(str(i) + '   ' for i in range(1, n + 1)))
    print('  ' + '─' * line_size)

    for i in range(n):
        row = '｜'.join([f' {board[i, j]}' for j in range(n)])
        print(string.ascii_lowercase[i] + f' ｜{row}｜')
        print('  ' + '─' * line_size)


def count_score(line: np.ndarray) -> List[int]:
    scores = [0, 0]  # human, ai
    counts = [0, 0]  # human, ai

    for cell in line:
        # human character found
        if cell == settings['characters'][0]:
            # if ai has more than 3 consecutive characters
            # we add the score to the ai then reset the count
            # and continue for counting the human characters
            if counts[1] >= 3:
                scores[1] += 2 * counts[1] - 5

            counts[1] = 0
            counts[0] += 1

        # ai character found
        elif cell == settings['characters'][1]:
            # if human has more than 3 consecutive characters
            # we add the score to the human then reset the count
            # and continue for counting the ai characters
            if counts[0] >= 3:
                scores[0] += 2 * counts[0] - 5

            counts[0] = 0
            counts[1] += 1

        # empty cell found
        else:
            # score of human
            if counts[0] >= 3:
                scores[0] += 2 * counts[0] - 5

            # score of ai
            if counts[1] >= 3:
                scores[1] += 2 * counts[1] - 5

            # reset counter
            counts = [0, 0]

    # calculate remaining scores
    # score of human
    if counts[0] >= 3:
        scores[0] += 2 * counts[0] - 5

    # score of ai
    if counts[1] >= 3:
        scores[1] += 2 * counts[1] - 5

    return scores


def calculate_scores(board: np.ndarray) -> List[int]:
    n = board.shape[0]
    sum_score = [0, 0]  # human, ai

    # calculate score of each row and column and sum them up
    for i in range(n):
        # row score
        sum_score = list(map(sum,
                             zip(count_score(board[i, :])),
                             sum_score))
        # zip make a tuple of two elements from two lists
        # then map function, maps the sum function to the tuple
        # this code is functional equivalent to the following commented code
        # score = count_score(board[i, :])
        # sum_score[0] = sum_score[0] + score[0]
        # sum_score[1] = sum_score[1] + score[1]

        # column score
        sum_score = list(map(sum,
                             zip(count_score(board[:, i]),
                                 sum_score)))

    # flip the matrix, it makes it easier to find the counter-diagonals
    # counter-diagoanls are the main diagonals of the flipped matrix
    board_flipped = np.fliplr(board)
    # calculate score of each subdiagonal and superdiagonal and sum them up
    # diagonal index in numpy are from -n + 1 to n, the main diangonal is 0
    for k in range(-n + 1, n):
        # main-diagonal score
        sum_score = list(map(sum,
                             zip(count_score(board.diagonal(k)),
                                 sum_score)))
        # counter-diagonal score
        sum_score = list(map(sum,
                             zip(count_score(board_flipped.diagonal(k)),
                                 sum_score)))

    return sum_score


def who_won(board: np.ndarray) -> int:
    # 0: human, 1: ai, 2: draw, -1: not finished
    # if there is any empty cell, the game is not finished yet
    if np.any(board == ' '):
        return -1

    score = calculate_scores(board)
    winner = 2

    if score[0] > score[1]:
        winner = 0

    elif score[0] < score[1]:
        winner = 1

    return winner


def simulate_random_games(board: np.ndarray, player: int, simulations: int) -> float:
    # simulates random games and returns the average score
    # based on monte-carlo method, the first player in each game is *player
    total_score = 0
    for _ in range(simulations):
        # copy the board to avoid changing the original board
        new_board = board.copy()

        current_player = player
        winner = who_won(new_board)
        if winner != -1:
            return 2 if winner == player else 2 if winner == 2 else -2

        # until the game is not finished yet
        while winner == -1:
            # available moves are the empty cells
            moves = list(
                zip(*np.where(new_board == settings['characters'][2])))

            if not moves:
                break  # No moves left

            selected_move = random.choice(moves)

            new_board[selected_move] = settings['characters'][current_player]
            # switch the player, using xor for toggling between 0 and 1
            current_player ^= 1

            # update the winner after each move
            winner = who_won(new_board)

        if winner == player:
            total_score += 2
        elif winner == 2:
            total_score += 2
        else:
            total_score -= 2

    return total_score / simulations


def max_value(board: np.ndarray, depth: int, simulations: int, alpha: float, beta: float) -> Tuple[float, List[int]]:
    # available moves are the empty cells
    moves = list(zip(*np.where(board == settings['characters'][2])))

    # we can play randomly if we are in beginning of the game to make it faster
    # if board.shape[0] * board.shape[1] - len(moves) < 3 and depth >= 1:
    #    return 0, random.choice(moves)

    # we should call the evaluation function if the game is finished or we reached the depth
    if not any(moves) or depth <= 0:
        return simulate_random_games(board, 1, simulations), [-1, -1]

    # default values for the best move and best score
    best_move = [-1, -1]
    best_score = -math.inf

    # for each move (the childs of the current node) we should call min function
    for move in moves:
        # the ai character is the first player in maximizing
        board[move] = settings['characters'][1]

        score, _ = min_value(board, depth - 1, simulations, alpha, beta)

        # restore the board to the previous state
        board[move] = ' '

        # maximize the score
        if score > best_score:
            best_score = score
            best_move = move

        # alpha-beta pruning
        if best_score >= beta:
            return best_score, best_move

        alpha = max(alpha, best_score)

    return best_score, best_move


def min_value(board: np.ndarray, depth: int, simulations: int, alpha: int, beta: int) -> Tuple[float, List[int]]:
    # available moves are the empty cells
    moves = list(zip(*np.where(board == ' ')))

    # we can play randomly if we are in beginning of the game to make it faster
    # if moves == board.shape[0] * board.shape[1] and depth >= 1:
    #    return 0, random.choice(moves)

    # we should call the evaluation function if the game is finished or we reached the depth
    if not any(moves) or depth <= 0:
        return simulate_random_games(board, 0, simulations), [-1, -1]

    # default values for the best move and best score
    best_move = [-1, -1]
    best_score = math.inf

    # for each move (the childs of the current node) we should call max function
    for move in moves:
        # the human character is the second player in minimizing
        board[move] = settings["characters"][0]

        score, _ = max_value(board, depth - 1, simulations, alpha, beta)

        # restore the board to the previous state
        board[move] = " "

        # minimize the score
        if score < best_score:
            best_score = score
            best_move = move

        # alpha-beta pruning
        if best_score <= alpha:
            return best_score, best_move

        beta = min(beta, best_score)

    return best_score, best_move


class AIThread(QThread):
    move_made = pyqtSignal(tuple)  # Emits the AI's move as (row, col)

    def __init__(self, board: np.ndarray):
        super().__init__()
        self.board = board

    def run(self):
        # AI is player 1
        score, move = max_value(
            self.board,
            depth=settings['depth'],
            simulations=settings['simulations'],
            alpha=-math.inf,
            beta=math.inf
        )
        if move == [-1, -1]:
            # No valid move found, it's a draw
            self.move_made.emit((-1, -1))
        else:
            self.move_made.emit(tuple(move))


class GameBoardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Tic-Tac-Toe")
        self.setFixedSize(400, 450)  # Adjust window size as needed

        # Initialize the game board
        self.board = np.full((settings['size'], settings['size']), " ")
        self.current_player = 0  # 0: Human, 1: AI

        # Set up the UI components
        self.initUI()

        # Initialize AI thread
        self.ai_thread = None

    def initUI(self):
        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Status label
        self.status_label = QLabel("Your turn (X)")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 16px;")
        main_layout.addWidget(self.status_label)

        # Grid layout for buttons
        grid_widget = QWidget()
        grid_layout = QGridLayout()
        grid_widget.setLayout(grid_layout)
        main_layout.addWidget(grid_widget)

        # Create buttons for the grid
        self.buttons = {}
        for i in range(settings['size']):
            for j in range(settings['size']):
                button = QPushButton(" ")
                button.setFixedSize(80, 80)
                button.setStyleSheet("font-size: 24px;")
                button.clicked.connect(
                    lambda checked, x=i, y=j: self.handle_move(x, y))
                grid_layout.addWidget(button, i, j)
                self.buttons[(i, j)] = button

    def handle_move(self, row: int, col: int):
        if self.board[row, col] != " ":
            QMessageBox.warning(self, "Invalid Move",
                                "This cell is already occupied.")
            return

        # Human move
        self.board[row, col] = settings['characters'][0]
        self.buttons[(row, col)].setText(settings['characters'][0])
        self.buttons[(row, col)].setEnabled(False)

        # Check for a winner
        winner = who_won(self.board)
        if winner != -1:
            self.end_game(winner)
            return

        # Update status
        self.current_player = 1
        self.status_label.setText("AI's turn (O)")

        # Trigger AI move
        self.ai_move()

    def ai_move(self):
        # Disable all buttons to prevent user interaction during AI's turn
        for button in self.buttons.values():
            button.setEnabled(False)

        # Start AI computation in a separate thread
        self.ai_thread = AIThread(self.board.copy())
        self.ai_thread.move_made.connect(self.process_ai_move)
        self.ai_thread.start()

    def process_ai_move(self, move: Tuple[int, int]):
        if move == (-1, -1):
            QMessageBox.information(self, "Draw", "It's a draw!")
            self.reset_game()
            return

        row, col = move
        self.board[row, col] = settings['characters'][1]
        self.buttons[(row, col)].setText(settings['characters'][1])
        self.buttons[(row, col)].setEnabled(False)

        # Check for a winner
        winner = who_won(self.board)
        if winner != -1:
            self.end_game(winner)
            return

        # Update status
        self.current_player = 0
        self.status_label.setText("Your turn (X)")

        # Re-enable available buttons
        for (i, j), button in self.buttons.items():
            if self.board[i, j] == " ":
                button.setEnabled(True)

    def end_game(self, winner: int):
        if winner == 0:
            QMessageBox.information(self, "Game Over", "You won!")
        elif winner == 1:
            QMessageBox.information(self, "Game Over", "AI won!")
        else:
            QMessageBox.information(self, "Game Over", "It's a draw!")
        self.reset_game()

    def reset_game(self):
        self.board = np.full((settings['size'], settings['size']), " ")
        self.current_player = 0
        self.status_label.setText("Your turn (X)")
        for (i, j), button in self.buttons.items():
            button.setText(" ")
            button.setEnabled(True)


def main():
    app = QApplication(sys.argv)
    window = GameBoardWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
