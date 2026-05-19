package main

// javad bajelan - 4011833206

import "fmt"

func is_safe(matrix [][]bool, row, col int) bool {
	n := len(matrix)

	for i := range row {
		if matrix[i][col] {
			return false
		}
	}

	for i, j := row-1, col-1; i >= 0 && j >= 0; i, j = i-1, j-1 {
		if matrix[i][j] {
			return false
		}
	}

	for i, j := row-1, col+1; i >= 0 && j < n; i, j = i-1, j+1 {
		if matrix[i][j] {
			return false
		}
	}

	return true
}

func n_queen(matrix [][]bool) [][]bool {
	n := len(matrix)
	if n == 0 {
		return matrix
	}

	var solver func(row int) bool
	solver = func(row int) bool {
		if row == n {
			return true
		}

		for col := range n {
			if is_safe(matrix, row, col) {
				matrix[row][col] = true
				if solver(row + 1) {
					return true
				}

				matrix[row][col] = false
			}
		}

		return false
	}

	if solver(0) {
		return matrix
	}

	return nil
}

func main() {
	n := 10
	matrix := make([][]bool, n)
	for i := range matrix {
		matrix[i] = make([]bool, n)
	}

	solution := n_queen(matrix)
	for i := range n {
		for j := range n {
			if solution[i][j] {
				fmt.Print("Q ")
			} else {
				fmt.Print("T ")
			}
		}

		fmt.Println()
	}
}
