package main

// Javad Bajelan - 4011833206

import (
	"fmt"
	"math"
)

func init_obst(prob []float64, n uint64) ([][]float64, [][]uint64) {
	A := make([][]float64, n)
	R := make([][]uint64, n)

	for i := range n {
		A[i] = make([]float64, n)
		R[i] = make([]uint64, n)
	}

	for i := range n - 1 {
		A[i][i+1] = prob[i]
		R[i][i+1] = i + 1
	}

	return A, R
}

func p_m(prob []float64, n uint64, m uint64) float64 {
	sum := float64(0)
	for i := uint64(n); i < m; i++ {
		sum += prob[i]
	}
	return sum
}

func obst(prob []float64, n uint64) float64 {
	A, R := init_obst(prob, n+1)

	for diam := uint64(2); diam <= n; diam++ {
		i := uint64(0)
		j := uint64(diam)

		for i <= n && j <= n {
			best_val := math.Inf(0)
			best_k := uint64(0)
			for k := i; k < j; k++ {
				val := A[i][k] + A[k+1][j]
				if val < best_val {
					best_val = val
					best_k = k
				}
			}

			A[i][j] = best_val + p_m(prob, i, j)
			R[i][j] = best_k + 1

			i += 1
			j += 1
		}

	}

	fmt.Println("A:")
	for _, row := range A {
		fmt.Println(row)
	}

	fmt.Println("\nR:")
	for _, row := range R {
		fmt.Println(row)
	}
	fmt.Println("")

	return A[0][n]
}

func main() {
	x := obst([]float64{0.7, 0.2, 0.1}, 3)
	fmt.Println(x)
}
