import numpy as np


def compute_optimal_bst(probabilities, n):
    cost_matrix = np.zeros((n + 1, n + 1))
    root_matrix = np.zeros((n + 1, n + 1), dtype=int)

    for i in range(n):
        cost_matrix[i][i + 1] = probabilities[i]
        root_matrix[i][i + 1] = i + 1

    for diagonal_size in range(2, n + 1):
        for start in range(n + 1 - diagonal_size):
            end = start + diagonal_size

            min_cost = float('inf')
            best_root = 0

            for root_candidate in range(start, end):
                current_cost = cost_matrix[start][root_candidate] + \
                    cost_matrix[root_candidate + 1][end]
                if current_cost < min_cost:
                    min_cost = current_cost
                    best_root = root_candidate

            cost_matrix[start][end] = min_cost + \
                sum(probabilities[start:end])
            root_matrix[start][end] = best_root + 1

    print("cost matrix:")
    print(cost_matrix)
    print("\nroot matrix:")
    print(root_matrix)
    print()

    return cost_matrix[0][n]


def main():
    test_probabilities = [0.7, 0.2, 0.1]
    result = compute_optimal_bst(test_probabilities, len(test_probabilities))
    print(f"Minimum expected search cost: {result}")


if __name__ == "__main__":
    main()
