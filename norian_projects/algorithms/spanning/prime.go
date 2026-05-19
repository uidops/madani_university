package main

// Javad Bajelan - 4011833206

import (
	"fmt"
	"math"
)

func init_prime(n int64) ([][3]float64, []int64) {
	F := make([][3]float64, 0, n-1)
	Y := make([]int64, n)

	for i := int64(0); i < n; i++ {
		Y[i] = -1
	}

	return F, Y
}

func prime_algorithm(G [][]float64, n int64) ([]int64, [][3]float64, float64) {
	F, Y := init_prime(n)

	Y[0] = 0

	total_weight := 0.0
	edges_added := int64(0)

	for edges_added < n-1 {
		min_weight := math.Inf(1)
		var u, v int64

		for i := int64(0); i < n; i++ {
			if Y[i] == -1 {
				continue
			}

			for j := int64(0); j < n; j++ {
				if Y[j] == -1 && G[i][j] > 0 && G[i][j] < min_weight {
					min_weight = G[i][j]
					u = i
					v = j
				}
			}
		}

		Y[v] = int64(v)
		F = append(F, [3]float64{float64(u), float64(v), min_weight})

		total_weight += min_weight
		edges_added += 1
	}

	return Y, F, total_weight
}

func main() {
	vertices, edges, total_weight := prime_algorithm(
		[][]float64{
			{0, 1, 3, 0, 0},
			{1, 0, 3, 6, 0},
			{3, 3, 0, 4, 2},
			{0, 6, 4, 0, 5},
			{0, 0, 2, 5, 0},
		}, 5)

	spanning_tree := make([][]float64, len(vertices))
	for i, _ := range vertices {
		spanning_tree[i] = make([]float64, len(vertices))
	}

	for _, edge := range edges {
		spanning_tree[int64(edge[0])][int64(edge[1])] = edge[2]
		spanning_tree[int64(edge[1])][int64(edge[0])] = edge[2]
	}

	for _, row := range spanning_tree {
		fmt.Println(row)
	}

	fmt.Println("weight = ", total_weight)
}
