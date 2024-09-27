import numpy as np
import random
from graph.graph import Graph


class AntColony:
    def __init__(self, graph: Graph, num_ants=15, num_iterations=20, alpha=1, beta=1, evaporation_rate=0.1):
        self.graph = graph
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.alpha = alpha  # важность феромонов
        self.beta = beta    # важность расстояний
        self.evaporation_rate = evaporation_rate

        self.pheromone = {edge: 1.0 for edge in self.get_all_edges()}
        self.best_distance = float('inf')
        self.best_route = None

    def get_all_edges(self):
        edges = []
        for u in self.graph.graph:
            for v, weight in self.graph.get_neighbors(u):
                edges.append((u, v))
        return set(edges)

    def run(self):
        for _ in range(self.num_iterations):
            all_routes = self.construct_routes()
            self.update_pheromone(all_routes)
            self.update_best_route(all_routes)
        return self.best_route, self.best_distance

    def construct_routes(self):
        all_routes = []
        for _ in range(self.num_ants):
            route = self.build_route()
            all_routes.append(route)
        return all_routes

    def build_route(self):
        start_city = random.choice(list(self.graph.graph.keys()))
        route = [start_city]
        visited = set(route)

        while len(visited) < len(self.graph.graph):
            current_city = route[-1]
            probabilities = self.calculate_probabilities(current_city, visited)
            next_city = np.random.choice(
                list(probabilities.keys()), p=list(probabilities.values()))
            route.append(next_city)
            visited.add(next_city)

        return route

    def calculate_probabilities(self, current_city, visited):
        pheromone = np.array([self.pheromone.get((current_city, neighbor), 0)
                             for neighbor, _ in self.graph.get_neighbors(current_city)])
        visibility = np.array(
            [1 / weight for _, weight in self.graph.get_neighbors(current_city)])

        numerator = pheromone ** self.alpha * visibility ** self.beta
        denominator = np.sum(
            numerator[~np.isin(range(len(pheromone)), list(visited))])

        probabilities = numerator / denominator
        probabilities[np.isin(range(len(pheromone)), list(visited))] = 0
        return {neighbor: prob for neighbor, prob in zip([neighbor for neighbor, _ in self.graph.get_neighbors(current_city)], probabilities)}

    def update_pheromone(self, all_routes):
        # Испаряем феромоны
        for edge in self.pheromone.keys():
            self.pheromone[edge] *= (1 - self.evaporation_rate)

        for route in all_routes:
            distance = self.calculate_route_distance(route)
            pheromone_contribution = 1 / distance
            for i in range(len(route) - 1):
                self.pheromone[(route[i], route[i + 1])
                               ] += pheromone_contribution
                if not self.graph.is_oriented:
                    self.pheromone[(route[i + 1], route[i])
                                   ] += pheromone_contribution

    def calculate_route_distance(self, route):
        return sum(weight for i in range(len(route) - 1) for _, weight in self.graph.get_neighbors(route[i]) if _ == route[i + 1])

    def update_best_route(self, all_routes):
        for route in all_routes:
            distance = self.calculate_route_distance(route)
            if distance < self.best_distance:
                self.best_distance = distance
                self.best_route = route
