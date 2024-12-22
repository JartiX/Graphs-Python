import random
import numpy as np
from graph.graph import Graph

class Ant:
    def __init__(self, graph: Graph, pheromone, alpha=1, beta=1):
        self.graph = graph
        self.pheromone = pheromone
        self.alpha = alpha
        self.beta = beta
        self.route = []
        self.visited = set()

    def reset(self, start_city):
        self.route = [start_city]
        self.visited = {start_city}

    def choose_next_city(self):
        current_city = self.route[-1]
        
        neighbors = [(neighbor, weight) for neighbor, weight in self.graph.get_neighbors(current_city)
                     if neighbor not in self.visited]
        if not neighbors:
            return None

        probabilities = self.calculate_probabilities(current_city, neighbors)
        
        unvisited_neighbors = {
            city: prob for city, prob in probabilities.items() if city not in self.visited}

        if not unvisited_neighbors:
            return None

        next_city = np.random.choice(
            list(unvisited_neighbors.keys()), p=list(unvisited_neighbors.values()))
        
        return next_city

    def calculate_probabilities(self, current_city, neighbors):
        pheromone = np.array(
            [self.pheromone.get((current_city, neighbor), 0) for neighbor, _ in neighbors])
        visibility = np.array([1 / weight for _, weight in neighbors])

        # Вычисляем вероятности с учетом альфа и бета
        attractiveness = (pheromone ** self.alpha) * (visibility ** self.beta)
        total = np.sum(attractiveness)

        probabilities = attractiveness / \
            total if total > 0 else np.zeros_like(attractiveness)

        return {neighbor: prob for (neighbor, _), prob in zip(neighbors, probabilities)}

    def build_route(self):
        while len(self.visited) < len(self.graph.graph):
            next_city = self.choose_next_city()
            if not next_city:
                return None
            self.route.append(next_city)
            self.visited.add(next_city)
        
        if self.graph.is_oriented:
            if self.graph.is_adjacent(self.route[-1], self.route[0]):
                self.route.append(self.route[0])
            else:
                return None
        else:
            if self.graph.is_adjacent(self.route[-1], self.route[0]) or self.graph.is_adjacent(self.route[0], self.route[-1]):
                self.route.append(self.route[0])
            else:
                return None

        return self.route


class AlphaAnt(Ant):
    def __init__(self, graph):
        super().__init__(graph, None, alpha=0, beta=1)

    def calculate_probabilities(self, current_city, neighbors):
        visibility = np.array([1 / weight for _, weight in neighbors])

        total = np.sum(visibility)

        probabilities = visibility / \
            total if total > 0 else np.zeros_like(visibility)

        return {neighbor: prob for (neighbor, _), prob in zip(neighbors, probabilities)}