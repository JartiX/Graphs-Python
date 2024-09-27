
class Graph:
    is_oriented: bool = None
    def __init__(self, is_oriented=False):
        self.graph = {}
        self.is_oriented = is_oriented

    def add_edge(self, u, v, weight=1):
        # Добавляем ребро с весом между вершинами u и v
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        self.graph[u].append((v, weight))
        if not self.is_oriented:
            self.graph[v].append((u, weight)) # неориентированный

    def remove_edge(self, u, v):
        # Удаляем ребро между вершинами u и v
        if u in self.graph:
            self.graph[u] = [item for item in self.graph[u] if item[0] != v]
        if not self.is_oriented and v in self.graph:
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

    def __str__(self):
        # Возвращает строковое представление графа
        result = ""
        for vertex in self.graph:
            result += f"{vertex}: {self.graph[vertex]}\n"
        return result
