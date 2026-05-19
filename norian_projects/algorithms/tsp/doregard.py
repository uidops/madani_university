from typing import List, Tuple

import numpy as np


class TravelingSalesmanProblem:
    def __init__(self, distance_matrix: List[List[float]], start_city: int = 0):
        self.distances = np.array(distance_matrix)
        self.num_cities = len(distance_matrix)
        self.start = start_city
        self.memoization = {}
        self.best_path = {}

    def solve(self) -> Tuple[float, List[int]]:
        all_cities = (1 << self.num_cities) - 1
        all_cities_except_start = all_cities & ~(1 << self.start)

        min_distance = self._compute_min_distance(
            self.start, all_cities_except_start)

        tour = self._reconstruct_path(self.start, all_cities_except_start)

        return min_distance, tour

    def _compute_min_distance(self, current: int, remaining_cities: int) -> float:
        if remaining_cities == 0:
            return self.distances[current][self.start]

        state = (current, remaining_cities)
        if state in self.memoization:
            return self.memoization[state]

        min_cost = float('inf')
        best_next_city = -1

        city = 0
        while city < self.num_cities:
            if (remaining_cities >> city) & 1:
                new_remaining = remaining_cities & ~(1 << city)
                cost = self.distances[current][city] + \
                    self._compute_min_distance(city, new_remaining)

                if cost < min_cost:
                    min_cost = cost
                    best_next_city = city

            city += 1

        self.best_path[state] = best_next_city

        self.memoization[state] = min_cost
        return min_cost

    def _reconstruct_path(self, start: int, cities: int) -> List[int]:
        tour = [start]
        current = start
        remaining = cities

        while remaining:
            state = (current, remaining)
            next_city = self.best_path[state]
            tour.append(next_city)
            remaining &= ~(1 << next_city)
            current = next_city

        tour.append(start)
        return tour


def count_set_bits(n: int) -> int:
    count = 0
    while n:
        n &= (n - 1)
        count += 1
    return count


def solve_tsp(distance_matrix: List[List[float]], start_city: int = 0) -> Tuple[float, List[int]]:
    solver = TravelingSalesmanProblem(distance_matrix, start_city)
    return solver.solve()


if __name__ == "__main__":
    INF = float('inf')
    distance_matrix = [
        [0, 2, 9, INF],
        [1, 0, 6, 4],
        [INF, 7, 0, 8],
        [6, 3, INF, 0]
    ]

    min_dist, optimal_path = solve_tsp(distance_matrix)

    print(f"Length of the shortest Hamiltonian circuit: {min_dist}")
    print(f"Optimal tour: {optimal_path}")
