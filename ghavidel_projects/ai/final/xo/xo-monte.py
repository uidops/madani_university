import math
import os
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple

import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

settings = {
    'characters': ['X', 'O', ' '],  # first character is human
    'size': 10,  # size of the board
    'min_simulations': 10,  # min simulations when we are sure
    'max_simulations': 30,  # max simulations when depth reached
    'max_depth': 1,  # max depth for end of game
    'top_moves': 3,  # limit the number of nodes in each depth
    'max_workers': os.cpu_count(),  # max workers for parallel game simulations
}


# ---------------------------------------------------------------------------------
# GAME LOGIC FUNCTIONS
# (Identical to your original logic, minus the console/TUI usage)
# ---------------------------------------------------------------------------------
def count_score(line: np.ndarray) -> List[int]:
    scores = [0, 0]  # [human_score, AI_score]
    counts = [0, 0]  # [human_count, AI_count]
    for char in line:
        if char == settings['characters'][0]:  # human
            scores[1] += max(0, 2 * counts[1] - 5)
            counts[1] = 0
            counts[0] += 1
        elif char == settings['characters'][1]:  # AI
            scores[0] += max(0, 2 * counts[0] - 5)
            counts[0] = 0
            counts[1] += 1
        else:  # empty
            scores[0] += max(0, 2 * counts[0] - 5)
            scores[1] += max(0, 2 * counts[1] - 5)
            counts = [0, 0]

    # at the end, add what's left
    scores[0] += max(0, 2 * counts[0] - 5)
    scores[1] += max(0, 2 * counts[1] - 5)
    return scores


def calculate_scores(board: np.ndarray) -> List[int]:
    n = board.shape[0]
    total_score = [0, 0]  # [human_score, AI_score]

    for i in range(n):
        row_score = count_score(board[i, :])
        col_score = count_score(board[:, i])
        total_score = list(map(sum, zip(total_score, row_score, col_score)))

    board_flipped = np.fliplr(board)
    for k in range(-n + 1, n):
        diag_score = count_score(board.diagonal(k))
        flip_score = count_score(board_flipped.diagonal(k))
        total_score = list(map(sum, zip(total_score, diag_score, flip_score)))

    return total_score


def who_won(board: np.ndarray) -> Tuple[int, List[int]]:
    """
    Returns (winner, score):
      - winner = -1 if game not done
      - winner = 0 if human
      - winner = 1 if AI
      - winner = 2 if draw
    """
    # If any empty spots remain, game isn't over
    if np.any(board == settings['characters'][2]):
        return -1, [0, 0]

    score = calculate_scores(board)
    if score[0] > score[1]:
        return 0, score
    elif score[0] < score[1]:
        return 1, score
    else:
        return 2, score  # draw


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
        tasks = [executor.submit(simulate_game, board, player)
                 for _ in range(simulations)]
        results = [t.result() for t in tasks]

    return sum(results) / simulations


def order_moves(board: np.ndarray, moves: List[Tuple[int, int]], player: int) -> List[Tuple[int, int]]:
    # sort moves based on current score of board
    def heuristic_key(move):
        i, j = move
        board[i, j] = settings['characters'][player]
        scores = calculate_scores(board)
        board[i, j] = settings['characters'][2]
        return scores[player] - scores[player ^ 1]

    moves.sort(key=lambda x: x[0], reverse=True)
    return moves[:settings['top_moves']]


def max_value(board: np.ndarray, alpha: float, beta: float, depth: int) -> Tuple[float, Tuple[int, int]]:
    """
    AI player ('O') tries to maximize the outcome.
    """
    moves = list(zip(*np.where(board == settings['characters'][2])))

    # If no moves or depth limit is reached, do a Monte Carlo estimate
    if depth <= 0 or not moves:
        sims = settings['max_simulations'] if depth == 0 else settings['min_simulations']
        val = monte_carlo_evaluation(board, 1, sims)
        return val, (-1, -1)

    best_score = -math.inf
    best_move = (-1, -1)

    moves = order_moves(board, moves, 1)
    for move in moves:
        board[move] = settings['characters'][1]  # AI
        score, _ = min_value(board, alpha, beta, depth - 1)
        board[move] = settings['characters'][2]  # revert

        if score > best_score:
            best_score = score
            best_move = move

        if best_score >= beta:
            return best_score, best_move

        alpha = max(alpha, best_score)

    return best_score, best_move


def min_value(board: np.ndarray, alpha: float, beta: float, depth: int) -> Tuple[float, Tuple[int, int]]:
    """
    Human player ('X') tries to minimize the outcome (from the AI's perspective).
    """
    moves = list(zip(*np.where(board == settings['characters'][2])))

    # If no moves or depth limit is reached, do a Monte Carlo estimate
    if depth <= 0 or not moves:
        sims = settings['max_simulations'] if depth == 0 else settings['min_simulations']
        val = monte_carlo_evaluation(board, 0, sims)
        return val, (-1, -1)

    best_score = math.inf
    best_move = (-1, -1)

    moves = order_moves(board, moves, 0)
    for move in moves:
        board[move] = settings['characters'][0]  # human
        score, _ = max_value(board, alpha, beta, depth - 1)
        board[move] = settings['characters'][2]  # revert

        if score < best_score:
            best_score = score
            best_move = move

        if best_score <= alpha:
            return best_score, best_move

        beta = min(beta, best_score)

    return best_score, best_move


# ---------------------------------------------------------------------------------
# DIALOG TO GET USER SETTINGS (Board Size, Simulations, Depth, etc.)
# ---------------------------------------------------------------------------------
class SettingsDialog(QDialog):
    """
    A simple dialog for the user to input Tic-Tac-Toe settings.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tic Tac Toe Settings")

        # Create input fields
        self.board_size_edit = QLineEdit(str(settings['size']))
        self.min_sims_edit = QLineEdit(str(settings['min_simulations']))
        self.max_sims_edit = QLineEdit(str(settings['max_simulations']))
        self.max_depth_edit = QLineEdit(str(settings['max_depth']))

        # Layout the form
        form_layout = QFormLayout()
        form_layout.addRow("Board size:", self.board_size_edit)
        form_layout.addRow("Min simulations:", self.min_sims_edit)
        form_layout.addRow("Max simulations:", self.max_sims_edit)
        form_layout.addRow("Max depth:", self.max_depth_edit)

        # OK/Cancel buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(button_box)
        self.setLayout(layout)

    def accept(self):
        """
        Called when user presses "OK". We read from the input fields,
        update `settings`, then close with QDialog.Accepted.
        """
        global settings
        try:
            size = int(self.board_size_edit.text())
            min_sims = int(self.min_sims_edit.text())
            max_sims = int(self.max_sims_edit.text())
            max_depth = int(self.max_depth_edit.text())

            # Basic validation
            if size < 3:
                QMessageBox.warning(self, "Error", "Board size must be >= 3.")
                return
            if min_sims < 1:
                QMessageBox.warning(
                    self, "Error", "Min simulations must be >= 1.")
                return
            if max_sims < min_sims:
                QMessageBox.warning(
                    self, "Error", "Max sims must be >= Min sims.")
                return
            if max_depth < 0:
                QMessageBox.warning(self, "Error", "Max depth must be >= 0.")
                return

            # Update global settings
            settings['size'] = size
            settings['min_simulations'] = min_sims
            settings['max_simulations'] = max_sims
            settings['max_depth'] = max_depth

        except ValueError:
            QMessageBox.warning(
                self, "Error", "Please enter valid integer values.")
            return

        # If everything is valid, accept dialog
        super().accept()


# ---------------------------------------------------------------------------------
# MAIN GUI CLASS FOR THE GAME
# ---------------------------------------------------------------------------------
class TicTacToeGUI(QMainWindow):
    """
    PyQt5 GUI for Tic-Tac-Toe, using the logic above.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tic Tac Toe")

        # Prepare an n x n board filled with blank
        self.n = settings['size']
        self.board = np.full((self.n, self.n), settings['characters'][2])

        # Decide who goes first at random: 0 -> human (X), 1 -> AI (O)
        self.current_player = random.randint(0, 1)
        self.initUI()

    def initUI(self):
        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout()
        central_widget.setLayout(self.main_layout)

        # A label on top to show status messages
        self.status_label = QLabel("Let's play Tic-Tac-Toe!")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.status_label)

        # A grid layout for the board
        self.grid_layout = QGridLayout()
        self.main_layout.addLayout(self.grid_layout)

        # Create buttons for each cell
        self.buttons = {}
        for i in range(self.n):
            for j in range(self.n):
                btn = QPushButton(" ")
                btn.setFixedSize(80, 80)
                btn.setStyleSheet("font-size: 24px;")
                self.grid_layout.addWidget(btn, i, j)
                self.buttons[(i, j)] = btn
                # connect each button to a handler
                btn.clicked.connect(lambda checked, row=i,
                                    col=j: self.on_human_move(row, col))

        self.update_status()

        # If the AI was chosen to go first, let it move immediately
        if self.current_player == 1:
            self.ai_move()

    def update_status(self):
        """
        Update the GUI text of each button and check if game is over.
        """
        for i in range(self.n):
            for j in range(self.n):
                self.buttons[(i, j)].setText(self.board[i, j])

        winner, _ = who_won(self.board)
        if winner == -1:
            # Game not over
            if self.current_player == 0:
                self.status_label.setText("Your turn (X).\nAI is thinking...")
            else:
                self.status_label.setText("AI's turn (O)...")
        else:
            # Game is over
            if winner == 0:
                QMessageBox.information(self, "Game Over", "You won!")
            elif winner == 1:
                QMessageBox.information(self, "Game Over", "AI won!")
            else:
                QMessageBox.information(self, "Game Over", "It's a draw!")
            self.disable_all_buttons()

    def disable_all_buttons(self):
        for btn in self.buttons.values():
            btn.setEnabled(False)

    def on_human_move(self, row, col):
        """
        Handle the human clicking on a cell (if it's indeed the human's turn).
        """
        winner, _ = who_won(self.board)
        if winner == -1 and self.current_player == 0:
            # If this cell is empty, let the human place 'X'
            if self.board[row, col] == settings['characters'][2]:
                self.board[row, col] = settings['characters'][0]
                self.update_status()
                self.current_player ^= 1  # switch to AI

                # Check again if the game ended
                winner, _ = who_won(self.board)
                if winner == -1:
                    self.ai_move()

    def ai_move(self):
        """
        The AI picks a move (using alpha-beta + Monte Carlo) and updates the board.
        """
        winner, _ = who_won(self.board)
        if winner == -1 and self.current_player == 1:
            self.status_label.setText("AI is thinking...")
            QApplication.processEvents()  # let the label update

            empty_count = (self.board == settings['characters'][2]).sum()
            # Use a deeper search only if more than 9 cells remain
            depth = settings['max_depth'] if empty_count <= 9 else 9

            start_time = time.time()
            best_score, move = max_value(
                self.board, -math.inf, math.inf, depth)
            elapsed = time.time() - start_time

            if move != (-1, -1):
                self.board[move] = settings['characters'][1]
            else:
                # No valid move (should rarely happen if the board isn't full)
                print("AI couldn't make a move!")

            self.current_player ^= 1  # switch to human
            self.update_status()
            print(f"AI made a move in {elapsed:.2f} seconds")


# ---------------------------------------------------------------------------------
# MAIN FUNCTION (RUNS THE GUI)
# ---------------------------------------------------------------------------------
def run_gui():
    """
    1. Opens a dialog for user to set board size, simulation counts, etc.
    2. Launches the TicTacToeGUI with those settings.
    """
    app = QApplication(sys.argv)

    # 1) Prompt user for settings
    dialog = SettingsDialog()
    result = dialog.exec_()

    if result == QDialog.Accepted:
        # 2) If user confirmed, start the game
        gui = TicTacToeGUI()
        gui.show()
        sys.exit(app.exec_())
    else:
        # User canceled
        sys.exit(0)


if __name__ == "__main__":
    # Just run the GUI
    run_gui()
