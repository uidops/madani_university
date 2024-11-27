# Wirth's algorithm
# Algorithms + Data Structures = Programs, Page 143

a, b, c, x = [True] * 8, [True] * 15, [True] * 15, [0] * 8


def eight_queens(i=0, solutions=None):
    if solutions is None:
        solutions = []

    for j in range(8):
        if a[j] and b[i + j] and c[i - j]:
            a[j], b[i + j], c[i - j], x[j] = False, False, False, i
            if i < 7:
                eight_queens(i + 1, solutions)
            else:
                solutions.append(x.copy())
            a[j], b[i + j], c[i - j] = True, True, True

    return solutions


print(eight_queens())
