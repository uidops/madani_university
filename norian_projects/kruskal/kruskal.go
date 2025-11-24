package main

// Javad Bajelan - 4011833206

import (
	"fmt"
	"sort"
)

type Edge struct {
	Source      int
	Destination int
	Weight      float64
}

type Graph struct {
	Vertices int
	Edges    []Edge
}

type Set map[int]bool

type SetCollection struct {
	sets []Set
}

func new_set_collection(n int) *SetCollection {
	sc := &SetCollection{
		sets: make([]Set, n),
	}

	for i := range n {
		sc.sets[i] = make(Set)
		sc.sets[i][i] = true
	}

	return sc
}

func (sc *SetCollection) Find(x int) int {
	for i, set := range sc.sets {
		if set != nil && set[x] {
			return i
		}
	}
	return -1
}

func (sc *SetCollection) Union(x, y int) bool {
	setX := sc.Find(x)
	setY := sc.Find(y)

	if setX == setY {
		return false
	}

	if len(sc.sets[setX]) < len(sc.sets[setY]) {
		setX, setY = setY, setX
	}

	for vertex := range sc.sets[setY] {
		sc.sets[setX][vertex] = true
	}

	sc.sets[setY] = nil

	return true
}

func matrix_to_graph(matrix [][]float64) *Graph {
	vertices := len(matrix)
	graph := &Graph{
		Vertices: vertices,
		Edges:    make([]Edge, 0),
	}

	for i := range vertices {
		for j := i + 1; j < vertices; j++ {
			if matrix[i][j] != 0 {
				graph.AddEdge(i, j, matrix[i][j])
			}
		}
	}

	return graph
}

func (g *Graph) AddEdge(source, destination int, weight float64) {
	g.Edges = append(g.Edges, Edge{
		Source:      source,
		Destination: destination,
		Weight:      weight,
	})
}

func (g *Graph) Kruskal() ([]Edge, float64) {
	result := make([]Edge, 0)
	total_weight := 0.0

	sort.Slice(g.Edges, func(i, j int) bool {
		return g.Edges[i].Weight < g.Edges[j].Weight
	})

	sets := new_set_collection(g.Vertices)

	for _, edge := range g.Edges {
		if sets.Union(edge.Source, edge.Destination) {
			result = append(result, edge)
			total_weight += edge.Weight

			if len(result)+1 == g.Vertices {
				break
			}
		}
	}

	return result, total_weight
}

func print_tree(mst []Edge, total_weight float64) {
	fmt.Println("Edge \t\tWeight")
	for _, edge := range mst {
		fmt.Printf("%d - %d \t\t%.2f\n", edge.Source, edge.Destination, edge.Weight)
	}

	fmt.Printf("\nTotal Weight: %.2f\n", total_weight)
}

func main() {
	matrix := [][]float64{
		{0, 1, 3, 0, 0},
		{1, 0, 3, 6, 0},
		{3, 3, 0, 4, 2},
		{0, 6, 4, 0, 5},
		{0, 0, 2, 5, 0},
	}

	graph := matrix_to_graph(matrix)
	mst, total_weight := graph.Kruskal()
	print_tree(mst, total_weight)
}
