import math
import os
import random
import string
import time
from typing import List, Tuple

import numpy as np

settings = {
    # first player is human
    'characters': ['X', 'O', ' '],
    'size': 4,
    'simulations': 600,
    'depth': 4
}


def print_board(board: np.ndarray) -> None:
    # because it's a square matrix, we ignore the second dimension
    n = board.shape[0]
    line_size = n * 4 + 1  # 4 = 3 characters + 1 separator

    os.system('clear')

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

    # calculate score of each row and sum them up
    for i in range(n):
        row = list(board[i, :])  # i-th row
        score = count_score(row)
        sum_score = [s + t for s, t in zip(score, sum_score)]

    # calculate score of each column and sum them up
    for j in range(n):
        col = list(board[:, j])  # j-th column
        score = count_score(col)
        sum_score = [s + t for s, t in zip(score, sum_score)]

    # flip the matrix, it makes it easier to find the counter-diagonals
    # counter-diagoanls are the main diagonals of the flipped matrix
    board_flipped = np.fliplr(board)
    # calculate score of each subdiagonal and superdiagonal and sum them up
    # diagonal index in numpy are from -n + 1 to n, the main diangonal is 0
    for k in range(-n + 1, n):
        main_diag = list(board.diagonal(k))
        coun_diag = list(board_flipped.diagonal(k))
        # ignore diagonals with less than 3 elements
        if len(main_diag) >= 3:
            score = count_score(main_diag)
            sum_score = [s + t for s, t in zip(score, sum_score)]

            score = count_score(coun_diag)
            sum_score = [s + t for s, t in zip(score, sum_score)]

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


# =========================== MCTS + UCT Helpers ===========================
class MCTSNode:
    def __init__(self, board: np.ndarray, current_player: int, move: Tuple[int, int] = None, parent=None):
        self.board = board
        self.current_player = current_player
        self.move = move  # The move that led to this node
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0  # We'll increment/decrement this based on outcomes

    @property
    def untried_moves(self) -> List[Tuple[int, int]]:
        # Return any moves not yet expanded as children
        all_moves = list(zip(*np.where(self.board == settings['characters'][2])))
        tried = [child.move for child in self.children]
        return [mv for mv in all_moves if mv not in tried]

    def is_terminal(self) -> bool:
        return who_won(self.board) != -1

    def add_child(self, board: np.ndarray, current_player: int, move: Tuple[int, int]):
        """
        Create a new child node for a given move.
        """
        child_node = MCTSNode(board, current_player, move=move, parent=self)
        self.children.append(child_node)
        return child_node


def uct_value(child: MCTSNode) -> float:
    """
    Upper Confidence Bound (UCT) score for balancing exploitation & exploration.
    """
    if child.visits == 0:
        return float('inf')
    # Exploitation term:
    exploitation = child.wins / child.visits
    # Exploration term:
    exploration = math.sqrt(2.0 * math.log(child.parent.visits) / child.visits)
    return exploitation + exploration


def mcts_selection(node: MCTSNode) -> MCTSNode:
    """
    Select child with highest UCT value until reaching a node that can be expanded or is terminal.
    """
    while not node.is_terminal() and not node.untried_moves:
        # All moves tried, pick the best child by UCT
        node = max(node.children, key=uct_value)
    return node


def mcts_expansion(node: MCTSNode) -> MCTSNode:
    """
    Expand one child from untried moves (if any).
    """
    untried = node.untried_moves
    if not untried or node.is_terminal():
        return node

    move = random.choice(untried)
    new_board = node.board.copy()
    new_board[move] = settings['characters'][node.current_player]
    next_player = 1 - node.current_player
    child_node = node.add_child(new_board, next_player, move)
    return child_node


def mcts_simulation(node: MCTSNode) -> int:
    """
    Play out a random simulation from 'node' until terminal.
    Return winner (0 or 1) or draw (2).
    """
    sim_board = node.board.copy()
    current_player = node.current_player
    winner = who_won(sim_board)

    while winner == -1:
        moves = list(zip(*np.where(sim_board == settings['characters'][2])))
        if not moves:
            break
        chosen_move = random.choice(moves)
        sim_board[chosen_move] = settings['characters'][current_player]
        current_player ^= 1
        winner = who_won(sim_board)

    return winner


def mcts_backpropagation(node: MCTSNode, result: int, root_player: int) -> None:
    """
    Update node statistics up the chain.
    If 'result' == root_player, we increment wins;
    if 'result' == 2 (draw), we can increment by 0.5 to indicate a partial success;
    otherwise, do nothing or subtract if you prefer for a loss.
    """
    while node is not None:
        node.visits += 1
        if result == root_player:
            # Win for root_player
            node.wins += 1
        elif result == 2:
            # Draw
            node.wins += 0.5
        # If loss, do nothing or subtract if you want to penalize
        node = node.parent


def mcts_best_move(root_board: np.ndarray, player: int, simulations: int) -> Tuple[int, int]:
    """
    Build an MCTS tree from 'root_board' for 'simulations' iterations,
    then pick the child with the highest visits.
    Return the best move.
    """
    root_node = MCTSNode(root_board.copy(), player)

    for _ in range(simulations):
        # 1) Selection
        leaf = mcts_selection(root_node)
        # 2) Expansion
        child = mcts_expansion(leaf)
        # 3) Simulation
        result = mcts_simulation(child)
        # 4) Backpropagation
        mcts_backpropagation(child, result, player)

    if not root_node.children:
        return (-1, -1)

    # Pick the child with the most visits (or best average)
    best_child = max(root_node.children, key=lambda c: c.visits)
    return best_child.move


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
            moves = list(zip(*np.where(new_board == settings['characters'][2])))

            # Instead of random choice, call MCTS with UCT to decide the next move
            if moves:
                # Feel free to adjust number of MCTS simulations here:
                best_mv = mcts_best_move(new_board, current_player, 50)
                if best_mv == (-1, -1):
                    # fallback to random in case MCTS can't find a move
                    selected_move = random.choice(moves)
                else:
                    selected_move = best_mv
            else:
                # no available moves
                break

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

    # we can play randomly if we are in beggining of the game to make it faster
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
            best_move = list(move)

        # alpha-beta pruning
        if best_score >= beta:
            return best_score, best_move

        alpha = max(alpha, best_score)

    return best_score, best_move


def min_value(board: np.ndarray, depth: int, simulations: int, alpha: float, beta: float) -> Tuple[float, List[int]]:
    # available moves are the empty cells
    moves = list(zip(*np.where(board == settings['characters'][2])))

    # we can play randomly if we are in beggining of the game to make it faster
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
            best_move = list(move)

        # alpha-beta pruning
        if best_score <= alpha:
            return best_score, best_move

        beta = min(beta, best_score)

    return best_score, best_move


def main():
    n = settings['size']
    # create an empty n*n board
    board = np.full((n, n), " ")

    # randomly choose the first player
    who = random.randint(0, 1)

    winner = -1
    # until the game is not finished yet
    while winner == -1:
        print_board(board)

        # human player
        if who == 0:
            # get the move from the user until it's a valid move
            while True:
                try:
                    choice = input("Enter your move as 'ij' (example: a1): ").strip()

                    if choice == "":
                        continue

                    # convert the input to the index of the board
                    # i is the row and j is the column
                    i, j = string.ascii_lowercase.index(choice[0]), int(choice[1:]) - 1

                    # check if the move is valid or not
                    # if valid then place the character in the board and break the loop
                    if (0 <= i < n) and (0 <= j < n) and board[i, j] == " ":
                        board[i, j] = settings["characters"][who]
                        break
                    else:
                        print("Invalid move")

                except Exception:
                    print("Invalid input format")

        else:
            print("AI is thinking...")
            now = time.time()
            # call the max function to get the best move for the ai
            # with the specified depth and number of simulations from the settings
            _, move = max_value(board,
                                depth=settings['depth'],
                                simulations=settings['simulations'],
                                alpha=-math.inf, beta=math.inf)

            if move == [-1, -1]:
                print("AI didn't make a move")
                break

            print("AI made a move in", time.time() - now, "seconds")
            time.sleep(0.5)

            board[move[0], move[1]] = settings["characters"][who]

        # switch the player, using xor for toggling between 0 and 1
        who ^= 1

        # update the winner after each move
        winner = who_won(board)

    print_board(board)
    if winner == 0:
        print("You won")
    elif winner == 1:
        print("AI won")
    else:
        print("It's a draw!")


if __name__ == "__main__":
    main()
