def n_queens(N=8):
    a = [True] * N  # Columns
    b = [True] * (2 * N - 1)  # Major diagonals
    c = [True] * (2 * N - 1)  # Minor diagonals
    x = [0] * N  # Positions of queens in each row
    solutions = []

    def solve(i):
        for j in range(N):
            if a[j] and b[i + j] and c[i - j + N - 1]:
                x[i] = j
                a[j] = b[i + j] = c[i - j + N - 1] = False
                if i < N - 1:
                    solve(i + 1)
                else:
                    solutions.append(x.copy())
                    return
                a[j] = b[i + j] = c[i - j + N - 1] = True

    solve(0)
    return solutions


# Example usage:
N = 20  # You can change N to any positive integer
solutions = n_queens(N)
print(f"Number of solutions for {N}-queens problem: {len(solutions)}")
for solution in solutions:
    print(solution)

# [3, 6, 4, 2, 0, 5, 7, 1]
