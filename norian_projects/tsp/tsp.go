package main

// Javad Bajelan - 4011833206

import (
	"fmt"
	"math"
)

func count_bits(n uint64) uint64 {
	// brian kernighan's algorithm
	c := uint64(0)
	for ; n > 0; c++ {
		n &= n - 1
	}
	return c
}

func remove_from_subset(subset uint64, x uint64) uint64 {
	return subset &^ (1 << x)
}

func is_subset_contains(subset uint64, x uint64) bool {
	return (subset>>x)&1 == 1
}

func generate_subsets(n uint64, k uint64, start uint64) []uint64 {
	subsets := []uint64{}
	for i := range uint64(1 << n) {
		if count_bits(i) == k && !is_subset_contains(i, start) {
			subsets = append(subsets, i)
		}
	}

	return subsets
}

func hamiltonian_path(P map[uint64]map[uint64]uint64, start uint64, subset uint64) []uint64 {
	path := []uint64{start}
	save_start := start
	for subset != 0 {
		next := P[start][subset]
		path = append(path, next)
		subset = remove_from_subset(subset, next)
		start = next
	}

	return append(path, save_start)
}

func init_tsp(W [][]float64, n uint64, start uint64) (map[uint64]map[uint64]float64, map[uint64]map[uint64]uint64) {
	D := make(map[uint64]map[uint64]float64)
	P := make(map[uint64]map[uint64]uint64)

	for i := range n {
		D[i] = make(map[uint64]float64)
		P[i] = make(map[uint64]uint64)

		if i != start {
			D[i][0] = W[i][start]
		}
	}

	return D, P
}

func tsp(W [][]float64, n uint64, start uint64) (float64, []uint64) {
	D, P := init_tsp(W, n, start)

	for k := uint64(1); k <= n-2; k++ {
		subsets := generate_subsets(n, k, start)

		for _, subset := range subsets {
			for i := range n {
				if i == start || is_subset_contains(subset, i) {
					continue
				}

				min_cost := math.Inf(1)
				min_j := uint64(0)

				for j := uint64(0); j < n; j++ {
					if j == start || !is_subset_contains(subset, j) {
						continue
					}

					cost := W[i][j] + D[j][remove_from_subset(subset, j)]

					if cost <= min_cost {
						min_cost = cost
						min_j = j
					}
				}

				D[i][subset] = min_cost
				P[i][subset] = min_j
			}
		}
	}

	full_set := remove_from_subset((1<<n)-1, start)

	min_cost := math.Inf(1)
	min_prev := uint64(0)

	for j := uint64(0); j < n; j++ {
		if j == start {
			continue
		}

		cost := W[start][j] + D[j][remove_from_subset(full_set, j)]
		if cost < min_cost {
			min_cost = cost
			min_prev = j
		}
	}

	D[start][full_set] = min_cost
	P[start][full_set] = min_prev

	return D[start][full_set], hamiltonian_path(P, start, full_set)
}

func main() {
	x, p := tsp([][]float64{
		{0, 2, 9, math.Inf(0)},
		{1, 0, 6, 4},
		{math.Inf(0), 7, 0, 8},
		{6, 3, math.Inf(0), 0},
	}, 4, 0)

	fmt.Printf("Length of the shortest hamiltonian path: %f\n", x)
	fmt.Printf("Hamiltonian path: %v\n", p)
}
