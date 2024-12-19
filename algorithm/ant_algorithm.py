import matplotlib.pyplot as plt
import numpy as np
import random
from graph.graph import Graph
from itertools import permutations

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
        self.best_routes = []
        self.chances = []
        self.num_best_routes = 0
        self.distances_per_iteration = []

        # Случайные координаты для визуализации
        self.coords = self.generate_random_coords()

    def generate_random_coords(self):
        coords = {vertex: (random.uniform(0, 10), random.uniform(0, 10))
                  for vertex in self.graph.graph}

        num_iterations = 1000
        learning_rate = 0.01

        for _ in range(num_iterations):
            for u in self.graph.graph:
                for v, weight in self.graph.get_neighbors(u):
                    x1, y1 = coords[u]
                    x2, y2 = coords[v]

                    current_distance = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

                    desired_distance = weight * 2

                    error = current_distance - desired_distance

                    if current_distance > 0:
                        dx = (x1 - x2) / current_distance * \
                            error * learning_rate
                        dy = (y1 - y2) / current_distance * \
                            error * learning_rate
                        coords[u] = (x1 - dx, y1 - dy)
                        coords[v] = (x2 + dx, y2 + dy)

        return coords

    def get_all_edges(self):
        edges = []
        for u in self.graph.graph:
            for v, weight in self.graph.get_neighbors(u):
                edges.append((u, v))
        return set(edges)

    def run(self, visualize):
        if visualize:
            fig, ax_routes = plt.subplots(figsize=(8, 8))
            fig2, ax_chances = plt.subplots(figsize=(8, 8))
            fig3, ax_distances = plt.subplots(figsize=(8, 8))
            plt.ion()

        cur_best_route = self.best_route
        for iteration in range(self.num_iterations):
            all_routes = self.construct_routes()


            self.update_pheromone(all_routes)
            self.update_best_route(all_routes)

            cur_best_route = self.best_route

            if visualize:
                chance = self.calculate_best_path_chance(cur_best_route)
                self.chances.append(chance)
                self.distances_per_iteration.append(self.best_distance)

                self.visualize(ax_routes, iteration, all_routes)
                self.update_chances_plot(ax_chances, iteration)
                self.update_distance_plot(ax_distances)
            print(
                f"iteration: {iteration}, found best route: {self.best_route}")

        return self.best_route, self.best_distance

    def update_distance_plot(self, ax):
        ax.clear()
        ax.plot(range(1, len(self.distances_per_iteration) + 1),
                self.distances_per_iteration, marker='o', color='green', linestyle='-', linewidth=2)
        ax.set_title("Length of Best Path per Iteration")
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Distance")
        ax.grid(True)
        ax.set_xlim(1, self.num_iterations)
        plt.draw()
        plt.pause(0.1)

    def update_chances_plot(self, ax, iteration):
        ax.clear()
        ax.plot(range(1, len(self.chances) + 1),
                self.chances, marker='o', color='blue', linestyle='-', linewidth=2)
        ax.set_title("Chance of Following the Best Path per Iteration")
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Chance")
        ax.grid(True)
        ax.set_xlim(1, self.num_iterations)
        ax.set_ylim(0, 1)
        plt.draw()
        plt.pause(0.1)


    def get_all_possible_routes(self):
        vertices = list(self.graph.graph.keys())
        all_possible_routes = []

        for perm in permutations(vertices):
            valid_route = True
            route = list(perm) + [perm[0]]

            for i in range(len(route) - 1):
                u, v = route[i], route[i + 1]
                if not self.graph.is_adjacent(u, v):
                    valid_route = False
                    break

            if valid_route:
                all_possible_routes.append(route)

        return all_possible_routes


    def calculate_best_path_chance(self, current_best_route):
        if not current_best_route:
            return 0

        all_possible_routes = self.get_all_possible_routes()

        total_probability_all_routes = 0
        total_probability_best_routes = 0

        for route in all_possible_routes:
            probability = 1
            visited = []
            for i in range(len(route) - 1):
                u, v = route[i], route[i + 1]

                pheromone_value = self.pheromone.get((u, v), 0)
                if not self.graph.is_oriented:
                    pheromone_value += self.pheromone.get((v, u), 0)

                visibility = 1 / self.graph.get_weight(u, v)
                attractiveness = (pheromone_value ** self.alpha) * \
                    (visibility ** self.beta)

                neighbors = self.graph.get_neighbors(u)
                pheromones = np.array(
                    [self.pheromone.get((u, neighbor), 0) for neighbor, _ in neighbors if (neighbor, u) not in visited]
                    )
                
                visibilities = np.array(
                    [1 / weight for neighbor, weight in neighbors if (neighbor, u) not in visited]
                    )
                attractivenesses = (pheromones ** self.alpha) * \
                    (visibilities ** self.beta)
                denominator = np.sum(attractivenesses)

                if denominator > 0:
                    attractiveness /= denominator

                probability *= attractiveness
                visited.append((u, v))

            total_probability_all_routes += probability

            if route in self.best_routes:
                total_probability_best_routes += probability

        if total_probability_all_routes > 0:
            normalized_probability = total_probability_best_routes / total_probability_all_routes
        else:
            normalized_probability = 0

        return normalized_probability

    def construct_routes(self):
        all_routes = []
        for _ in range(self.num_ants):
            route = self.build_route()
            if route is not None:
                all_routes.append(route)
        return all_routes

    def build_route(self):
        while True:
            start_city = random.choice(list(self.graph.graph.keys()))
            route = [start_city]
            visited = set(route)

            # Строим маршрут до посещения всех городов
            while len(visited) < len(self.graph.graph):
                current_city = route[-1]
                probabilities = self.calculate_probabilities(
                    current_city, visited)
                unvisited_neighbors = {
                    city: prob for city, prob in probabilities.items() if city not in visited}

                if not unvisited_neighbors:
                    return None

                # Выбираем следующий город
                next_city = np.random.choice(
                    list(unvisited_neighbors.keys()), p=list(unvisited_neighbors.values()))
                route.append(next_city)
                visited.add(next_city)

            # Проверяем, существует ли путь от последнего города в маршруте к начальному
            if self.graph.is_oriented:
                if (route[-1], start_city) in self.pheromone:
                    route.append(start_city)
                    return route
            else:
                if (route[-1], start_city) in self.pheromone or (start_city, route[-1]) in self.pheromone:
                    route.append(start_city)
                    return route

    def calculate_probabilities(self, current_city, visited):
        neighbors = [(neighbor, weight) for neighbor, weight in self.graph.get_neighbors(
            current_city) if neighbor not in visited]

        if not neighbors:
            return {}  # Вернуть пустой словарь, если нет непосещенных соседей

        pheromone = np.array(
            [self.pheromone.get((current_city, neighbor), 0) for neighbor, _ in neighbors])
        visibility = np.array([1 / weight for _, weight in neighbors])

        # Вычисляем вероятности с учетом альфа и бета
        numerator = (pheromone ** self.alpha) * (visibility ** self.beta)
        denominator = np.sum(numerator)

        probabilities = numerator / \
            denominator if denominator > 0 else np.zeros_like(numerator)

        return {neighbor: prob for (neighbor, _), prob in zip(neighbors, probabilities)}

    def update_pheromone(self, all_routes):
        # Испаряем феромоны
        for edge in self.pheromone.keys():
            self.pheromone[edge] *= (1 - self.evaporation_rate)

        for route in all_routes:
            distance = self.calculate_route_distance(route)

            # Вклад феромона. Q/distance, где Q-фиксированная константа. Чем короче маршрут, тем больше феромонов будет оставлено
            pheromone_contribution = 1 / distance

            for i in range(len(route) - 1):
                self.pheromone[(route[i], route[i + 1])
                               ] += pheromone_contribution
                if not self.graph.is_oriented:
                    self.pheromone[(route[i + 1], route[i])
                                   ] += pheromone_contribution

    def calculate_route_distance(self, route):
        total_distance = 0
        for i in range(len(route) - 1):
            for neighbor, weight in self.graph.get_neighbors(route[i]):
                if neighbor == route[i + 1]:
                    total_distance += weight
                    break
        return total_distance
    
    def update_best_route(self, all_routes):
        for route in all_routes:
            distance = self.calculate_route_distance(route)
            if distance < self.best_distance:
                self.best_distance = distance
                self.num_best_routes = 0
                self.best_routes = []
                self.best_route = route
            if distance == self.best_distance and route not in self.best_routes:
                self.num_best_routes += 1
                self.best_routes.append(route)


    def visualize(self, ax, iteration, all_routes):
        ax.clear()

        # Нормализация феромонов, чтобы по ним корректно вычислять цвет
        max_pheromone = max(self.pheromone.values()) if self.pheromone else 1

        # Рисуем граф
        for u in self.graph.graph:
            for v, weight in self.graph.get_neighbors(u):
                x = [self.coords[u][0], self.coords[v][0]]
                y = [self.coords[u][1], self.coords[v][1]]
                # Получаем уровень феромонов и нормализуем его
                pher = self.pheromone.get((u, v), 0) / max_pheromone
                # Цвет зависит от количества феромонов (чем больше, тем ярче синий)
                color = (1 - pher, 1 - pher, 1)
                ax.plot(x, y, color=color, alpha=pher, linewidth=2)

        # Визуализируем текущие маршруты муравьев
        for i, route in enumerate(all_routes):
            x = [self.coords[city][0] for city in route]
            y = [self.coords[city][1] for city in route]
            # Разные цвета для каждого муравья
            color = plt.cm.jet(i / len(all_routes))
            ax.plot(x, y, '-', color=color, alpha=0.6, linewidth=2)

        # Визуализируем лучший маршрут красным цветом
        if self.best_route:
            x = [self.coords[city][0] for city in self.best_route]
            y = [self.coords[city][1] for city in self.best_route]
            ax.plot(x, y, 'r-', alpha=0.9, linewidth=4, label='Best Route')

        # Визуализируем города
        for city, coord in self.coords.items():
            ax.plot(coord[0], coord[1], 'bo', markersize=8)
            ax.text(coord[0], coord[1], city, fontsize=15,
                    ha='right', color='purple')

        ax.set_title(
            f"Iteration {iteration+1}\nBest distance: {self.best_distance}\nBest route: {self.best_route}")
        ax.legend()

        plt.draw()
        plt.pause(2)
