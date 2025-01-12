import networkx as nx
import matplotlib.pyplot as plt
from copy import deepcopy


class GameState:
    def __init__(self, board, player, move=None):
        self.board = board
        self.player = player
        self.move = move

    def get_available_moves(self):
        moves = []
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == '_':
                    moves.append((r, c))
        return moves

    def make_move(self, move):
        new_board = deepcopy(self.board)
        r, c = move
        new_board[r][c] = self.player
        next_player = 'X' if self.player == 'O' else 'O'
        return GameState(new_board, next_player, move)

    def board_str(self):
        return '\n'.join([' '.join(row) for row in self.board])


def hierarchy_pos(G, root, width=1.5, vert_gap=1, vert_loc=0, xcenter=0.5, pos=None, parent=None):
    if pos is None:
        pos = {}
    pos[root] = (xcenter, vert_loc)
    children = list(G.successors(root))
    if not children:
        return pos
    dx = width / len(children)
    nextx = xcenter - width / 2 - dx / 2
    for child in children:
        nextx += dx
        pos = hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                            vert_loc=vert_loc - vert_gap, xcenter=nextx, pos=pos, parent=root)
    return pos


x = 0


def build_game_tree_alpha_beta(state, graph, node_id, id_counter, depth=0, max_depth=6, alpha=-float('inf'), beta=float('inf')):
    global x
    if depth > max_depth:
        return None

    available_moves = state.get_available_moves()

    if not available_moves:
        value = [1, 2, 1, 1, 1, 2, 0, 2, 0, 1, 1,
                 2, 2, 1, 1, 2, 2, 2, 1, 0, 1, 1, 0, 1]
        value = value[x]
        x += 1
        label = f"{state.board_str()}\nValue: {value}"
        graph.add_node(node_id, label=label, current_player=None,
                       alpha=alpha, beta=beta, value=value, pruned=False)
        return value

    current_player = state.player
    is_maximizing = current_player == 'O'

    best_value = -float('inf') if is_maximizing else float('inf')

    label = f"{state.board_str()}\nAlpha: {alpha}\nBeta: {beta}"
    graph.add_node(node_id, label=label, current_player=current_player,
                   alpha=alpha, beta=beta, pruned=False)

    for move in available_moves:
        id_counter[0] += 1
        child_id = id_counter[0]
        child_state = state.make_move(move)

        # Determine pruning condition based on the node type
        if alpha >= beta:
            # if (not is_maximizing and best_value >= beta) or (is_maximizing and best_value <= alpha):
            graph.add_node(child_id, label=None,
                           current_player=current_player, pruned=True)
            graph.add_edge(node_id, child_id)
            x += len(child_state.get_available_moves())
            continue

        child_value = build_game_tree_alpha_beta(
            child_state, graph, child_id, id_counter, depth + 1, max_depth, alpha, beta)

        if is_maximizing:
            best_value = max(best_value, child_value)
            alpha = max(alpha, best_value)
        else:
            best_value = min(best_value, child_value)
            beta = min(beta, best_value)

        graph.add_edge(node_id, child_id)

    graph.nodes[node_id]['label'] = f"{state.board_str()}\nAlpha: {alpha}\nBeta: {
        beta}\nValue: {best_value}"
    graph.nodes[node_id]['alpha'] = alpha
    graph.nodes[node_id]['beta'] = beta
    graph.nodes[node_id]['value'] = best_value

    return best_value


def draw_game_tree(graph, root_id):
    pos = hierarchy_pos(graph, root_id, width=2**5, vert_gap=1)

    labels = nx.get_node_attributes(graph, 'label')
    current_players = nx.get_node_attributes(graph, 'current_player')
    pruned_nodes = nx.get_node_attributes(graph, 'pruned')

    color_map = []
    for node in graph.nodes():
        if pruned_nodes.get(node, False):
            color_map.append('lightblue')  # Nodes that would be pruned
        else:
            current_player = current_players.get(node)
            if current_player == 'O':
                color_map.append('green')   # O's turn
            elif current_player == 'X':
                color_map.append('red')     # X's turn
            else:
                color_map.append('gray')    # Terminal state (Draw)

    plt.figure(figsize=(20, 15))
    nx.draw(graph, pos, with_labels=False, node_size=1500,
            node_color=color_map, edge_color='gray', arrows=True)

    for node, label in labels.items():
        if label:  # Skip labels for pruned nodes
            x, y = pos[node]
            plt.text(x, y - 0.1, label, fontsize=8,
                     ha='center', va='center', color='black')

    plt.title(
        'Tic-Tac-Toe Game Tree with Alpha-Beta Pruning (Marked Pruned Nodes)', fontsize=16)
    plt.axis('off')
    plt.show()


def main_alpha_beta():
    initial_board = [
        ['X', 'O', 'X'],
        ['O', 'X', '_'],
        ['_', '_', '_']
    ]
    initial_player = 'O'
    initial_state = GameState(initial_board, initial_player)

    G = nx.DiGraph()
    id_counter = [0]

    max_depth = 6
    build_game_tree_alpha_beta(
        initial_state, G, id_counter[0], id_counter, depth=0, max_depth=max_depth)
    draw_game_tree(G, root_id=0)


if __name__ == "__main__":
    main_alpha_beta()
