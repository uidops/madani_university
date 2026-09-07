package main

import (
	"fmt"
	"math"
	"slices"
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

func matrix_to_graph(matrix [][]float64) *Graph {
	vertices := len(matrix)
	graph := &Graph{
		Vertices: vertices,
		Edges:    make([]Edge, 0),
	}

	for i := range matrix {
		for j := range matrix[i] {
			if matrix[i][j] > 0 {
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

func (g *Graph) dijkstra(start_vertex int) [][]int {
	F := [][]int{}
	Y := []int{start_vertex}

	dist := make([]float64, g.Vertices)
	dist[start_vertex] = 0
	for i := 1; i < g.Vertices; i++ {
		dist[i] = math.Inf(1)
	}

	prev := make([]int, g.Vertices)
	for i := range prev {
		prev[i] = -1
	}

	for _, edge := range g.Edges {
		if edge.Source == start_vertex {
			dist[edge.Destination] = edge.Weight
			prev[edge.Destination] = start_vertex
		}
	}

	for len(Y) != g.Vertices {
		min_dist := math.Inf(1)
		next_vertex := -1

		for v := range g.Vertices {
			if !slices.Contains(Y, v) && dist[v] < min_dist {
				min_dist = dist[v]
				next_vertex = v
			}
		}

		if next_vertex == -1 || math.IsInf(min_dist, 1) {
			break
		}

		Y = append(Y, next_vertex)

		if prev[next_vertex] != -1 {
			path := []int{prev[next_vertex], next_vertex}
			F = append(F, path)
		}

		for _, edge := range g.Edges {
			if edge.Source == next_vertex && !slices.Contains(Y, edge.Destination) {
				new_dist := dist[next_vertex] + edge.Weight
				if new_dist < dist[edge.Destination] {
					dist[edge.Destination] = new_dist
					prev[edge.Destination] = next_vertex
				}
			}
		}
	}

	return F
}

func main() {
	matrix := [][]float64{
		{0, 7, 4, 6, 1},
		{0, 0, 0, 0, 0},
		{0, 2, 0, 0, 0},
		{0, 3, 0, 0, 0},
		{0, 0, 0, 1, 0},
	}

	graph := matrix_to_graph(matrix)
	result := graph.dijkstra(0)
	fmt.Println("F:", result)
}
