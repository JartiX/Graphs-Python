import heapq


class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v, weight=1):
        # Добавляем ребро с весом между вершинами u и v
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight)) # неориентированный

    def remove_edge(self, u, v):
        # Удаляем ребро между вершинами u и v
        if u in self.graph and v in self.graph:
            self.graph[u] = [item for item in self.graph[u] if item[0] != v]
            self.graph[v] = [item for item in self.graph[v] if item[0] != u]

    def add_vertex(self, v):
        # Добавляем вершину v, если она отсутствует
        if v not in self.graph:
            self.graph[v] = []

    def remove_vertex(self, v):
        # Удаляем вершину и все инцидентные ей ребра
        if v in self.graph:
            for neighbor, _ in list(self.graph[v]):
                self.graph[neighbor] = [
                    item for item in self.graph[neighbor] if item[0] != v]
            del self.graph[v]

    def get_neighbors(self, v):
        # Получаем соседей вершины v
        return self.graph.get(v, [])

    def dijkstra(self, start, end):
        # Алгоритм Дейкстры для нахождения кратчайшего пути с учётом весов
        distances = {vertex: float('inf') for vertex in self.graph}
        distances[start] = 0
        priority_queue = [(0, start)]
        heapq.heapify(priority_queue)

        while priority_queue:
            curr_dist, curr_vertex = heapq.heappop(priority_queue)

            if curr_vertex == end:
                return curr_dist

            if curr_dist > distances[curr_vertex]:
                continue

            for neighbor, weight in self.graph[curr_vertex]:
                distance = curr_dist + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))

        return float('inf')  # Если путь не найден

    def __str__(self):
        # Возвращает строковое представление графа
        result = ""
        for vertex in self.graph:
            result += f"{vertex}: {self.graph[vertex]}\n"
        return result
