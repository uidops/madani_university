from math import inf


class SpanningTreeFinder:
    def __init__(self, graph_matrix, vertex_count):
        self.graph = graph_matrix
        self.n_vertices = vertex_count
        self.visited = None
        self.mst_edges = None
        self.total_cost = 0

    def initialize_structures(self):
        self.visited = [-1] * self.n_vertices
        self.mst_edges = []
        self.visited[0] = 0
        self.total_cost = 0

    def find_minimum_spanning_tree(self):
        self.initialize_structures()

        edges_needed = self.n_vertices - 1
        edges_added = 0

        while edges_added < edges_needed:
            min_weight = inf
            u, v = -1, -1

            for i in range(self.n_vertices):
                if self.visited[i] == -1:
                    continue

                for j in range(self.n_vertices):
                    if (self.visited[j] == -1 and
                        self.graph[i][j] > 0 and
                            self.graph[i][j] < min_weight):
                        min_weight = self.graph[i][j]
                        u, v = i, j

            self.visited[v] = v

            self.mst_edges.append((u, v, min_weight))

            self.total_cost += min_weight
            edges_added += 1

        return self.visited, self.mst_edges, self.total_cost

    def construct_tree_matrix(self):
        tree_matrix = [[0.0 for _ in range(self.n_vertices)]
                       for _ in range(self.n_vertices)]

        for u, v, weight in self.mst_edges:
            tree_matrix[u][v] = weight
            tree_matrix[v][u] = weight

        return tree_matrix


def main():
    example_graph = [
        [0, 1, 3, 0, 0],
        [1, 0, 3, 6, 0],
        [3, 3, 0, 4, 2],
        [0, 6, 4, 0, 5],
        [0, 0, 2, 5, 0]
    ]

    mst_finder = SpanningTreeFinder(example_graph, 5)

    vertices, edges, total_weight = mst_finder.find_minimum_spanning_tree()

    spanning_tree = mst_finder.construct_tree_matrix()

    for row in spanning_tree:
        print(row)

    print("weight =", total_weight)


if __name__ == "__main__":
    main()
