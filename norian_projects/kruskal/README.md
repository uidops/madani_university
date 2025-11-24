# Kruskal's Minimum Spanning Tree Algorithm in Go

This repository contains a complete implementation of Kruskal's algorithm for finding the Minimum Spanning Tree (MST) of a weighted undirected graph in Go.

## What is Kruskal's Algorithm?

Kruskal's algorithm is a greedy algorithm that finds a minimum spanning tree for a connected weighted graph. A spanning tree is a subgraph that includes all vertices of the original graph and is a tree (connected and acyclic). A minimum spanning tree is a spanning tree with the minimum possible total edge weight.

### Algorithm Steps:
1. Sort all edges in ascending order by weight
2. Initialize a Union-Find data structure to detect cycles
3. For each edge in sorted order:
   - If the edge connects two different components (doesn't create a cycle), add it to the MST
   - Otherwise, skip the edge
4. Continue until we have V-1 edges (where V is the number of vertices)

## Implementation Features

### Data Structures

- **Edge**: Represents a weighted edge between two vertices
- **Graph**: Represents a weighted undirected graph with vertices and edges
- **SetCollection**: Collection of sets for efficient cycle detection using set operations

### Key Components

1. **Set-based Cycle Detection**:
   - Efficient set operations for component tracking
   - Smart merging of smaller sets into larger ones

2. **Graph Representation**:
   - Edge list representation for efficient sorting
   - Support for both manual graph construction and adjacency matrix input

3. **Multiple Usage Patterns**:
   - Direct graph construction with `AddEdge`
   - Adjacency matrix conversion
   - Legacy function compatibility

## Usage Examples

### Example 1: Manual Graph Construction

```go
graph := NewGraph(4)
graph.AddEdge(0, 1, 10)
graph.AddEdge(0, 2, 6)
graph.AddEdge(0, 3, 5)
graph.AddEdge(1, 3, 15)
graph.AddEdge(2, 3, 4)

mst, totalWeight := graph.KruskalMST()
PrintMST(mst, totalWeight)
```

### Example 2: Using Adjacency Matrix

```go
matrix := [][]float64{
    {0, 2, 0, 6, 0},
    {2, 0, 3, 8, 5},
    {0, 3, 0, 0, 7},
    {6, 8, 0, 0, 9},
    {0, 5, 7, 9, 0},
}

graph := CreateGraphFromAdjacencyMatrix(matrix)
mst, totalWeight := graph.KruskalMST()
```

### Example 3: Legacy Function

```go
mstMatrix := kruskal(adjacencyMatrix)
```

## Time and Space Complexity

- **Time Complexity**: O(E log E) where E is the number of edges
  - Sorting edges: O(E log E)
  - Set operations: O(V) per operation in worst case, often much better

- **Space Complexity**: O(V + E) where V is the number of vertices
  - Graph storage: O(E)
  - SetCollection structure: O(V)

## Running the Code

### Execute the main program:
```bash
go run main.go
```

This will run several examples demonstrating different ways to use the algorithm.

### Run tests:
```bash
go test -v
```

### Run benchmarks:
```bash
go test -bench=.
```

## Test Coverage

The implementation includes comprehensive tests covering:

- Basic functionality (simple graphs, complete graphs)
- Edge cases (single vertex, empty graph, disconnected graph)
- Data structure correctness (Union-Find operations)
- Performance benchmarks for different graph sizes
- Input validation and matrix conversion

## Algorithm Properties

### Correctness
- **Greedy Choice**: Always selecting the minimum weight edge that doesn't create a cycle is optimal
- **Cycle Detection**: Set-based approach efficiently detects cycles by checking component membership
- **Optimality**: The algorithm is guaranteed to find the minimum spanning tree

### Applications
- Network design (telecommunications, computer networks)
- Clustering algorithms
- Approximation algorithms for traveling salesman problem
- Circuit design
- Transportation planning

## Implementation Details

### Set-based Optimizations

1. **Smart Merging**: When joining two sets, we always merge the smaller set into the larger one
2. **Direct Membership**: Sets provide direct membership testing for efficient component checking

These optimizations ensure that set operations remain efficient even for large graphs.

### Edge Sorting

The algorithm sorts all edges by weight using Go's built-in `sort.Slice` function, which uses an efficient comparison-based sorting algorithm.

### Memory Efficiency

- The graph uses an edge list representation, which is memory-efficient for sparse graphs
- The SetCollection structure uses only O(V) additional space
- No redundant edge storage (undirected edges stored once)

## Future Enhancements

Possible improvements to consider:
- Support for directed graphs (minimum spanning arborescence)
- Parallel edge sorting for very large graphs
- Custom comparison functions for different edge weight types
- Visualization output (DOT format for Graphviz)
- Integration with other graph algorithms

## References

- Introduction to Algorithms (CLRS), Chapter 23: Minimum Spanning Trees
- Robert Sedgewick and Kevin Wayne, "Algorithms", 4th Edition
- Original paper: Kruskal, J. B. (1956). "On the shortest spanning subtree of a graph and the traveling salesman problem"