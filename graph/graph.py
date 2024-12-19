import pulp
from itertools import combinations
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

    def get_weight(self, u, v):
        # Получаем вес ребра между вершинами u и v
        for neighbor, weight in self.graph.get(u, []):
            if neighbor == v:
                return weight
        return None  # Возвращаем None, если ребро не найдено

    def is_adjacent(self, u, v):
        # Проверяем, являются ли вершины u и v смежными
        return any(neighbor == v for neighbor, _ in self.graph.get(u, []))

    def __str__(self):
        # Возвращает строковое представление графа
        result = ""
        for vertex in self.graph:
            for a, b in self.graph[vertex]:
                result += f"{vertex} -> {a}, weight: {b} | "
            result = result[:-2]
            result += '\n'
        return result
        
    def __ore_dirak_condition(self):
        num_vertexes = len(self.graph.keys())
        p = num_vertexes/2
        # Условие Дирака (достаточное): если в графе с n вершинами каждая вершина имеет степень не менее n/2, то в графе существует гамильтонов цикл
        # Условие Оре (достаточное): если для каждой пары вершин (u, v) графа,  не связанных между собой, выполняется условие: deg(u) + deg(v) >= n, то граф содержит гамильтонов цикл.
        for vertex1, vertexes1 in self.graph.items():
            if len(vertexes1) < p:
                return False
            for vertex2, vertexes2 in self.graph.items():
                if vertex1 != vertex2 and not self.is_adjacent(vertex1, vertex2):
                    if len(vertexes1) + len(vertexes2) < num_vertexes:
                        return False
        return True
    
    def __necessary_condition(self):
        # Необходимое условие: если для какой-либо вершины степень меньше 2, гамильтонов цикл невозможен,
        # так как цикл должен проходить через все вершины.
        for vertexes in self.graph.values():
            if len(vertexes) < 2:
                return False
        return True
        
    def make_closure_bondi(self):
        # Замыкание графа по теореме Бонди-Хваталя
        num_vertexes = len(self.graph.keys())
        for vertex1, vertexes1 in self.graph.items():
            for vertex2, vertexes2 in self.graph.items():
                if vertex1 != vertex2:
                    if len(vertexes1) + len(vertexes2) >= num_vertexes:
                        # Проверим, являются ли они смежными
                        if not self.is_adjacent(vertex1, vertex2):
                            # Добавляем ребро
                            self.add_edge(vertex1, vertex2)
                            
    def make_closure(self):
        # Строим замыкание графа для получения гамильтонова цикла
        vertices = list(self.graph.keys())
        num_vertices = len(vertices)
        added_edges = list()

        # Пока граф не удовлетворяет условиям для гамильтонова цикла, добавляем ребра
        while not self.__ore_dirak_condition():
            # Найти пару несмежных вершин с максимальной суммой степеней
            for i in range(num_vertices):
                for j in range(i + 1, num_vertices):
                    u, v = vertices[i], vertices[j]
                    if not self.is_adjacent(u, v) and ((len(self.get_neighbors(u)) + len(self.get_neighbors(v)) < num_vertices) \
                    or len(self.get_neighbors(u)) < num_vertices/2 or len(self.get_neighbors(v)) < num_vertices/2):
                        if (u, v) not in added_edges:
                          self.add_edge(u, v)
                          added_edges.append((u, v))
            if added_edges:
                print("Добавленные ребра:", added_edges)
                            
    def has_hamiltonial_cycle(self):
        num_vertexes = len(self.graph.keys())
        
        
        # Если число вершин в графе меньше 3, то гамильтонов цикл невозможен
        if num_vertexes < 3:
            return False
        
        # Если условия Дирака или Оре выполняются, значит гамильтонов цикл есть, однако если они не выполняются это не гарантирует его отсутствия, т.к эти условия достаточные, а не необходимые
            
        if self.__ore_dirak_condition():
            print("Выполнилось условия Дирака-Оре")
            return True
        
                    
        # Если необходимое условие выполняется, нельзя гарантировать, что гамильтонов цикл есть, однако если это условие не выполняется, то цикла точно нет

        if not self.__necessary_condition():
            print("Необходимое условие не выполнилось.")
            return False
            
        # Задача сводится к нахождению хода через все вершины без подциклов, что соответствует гамильтоновому циклу.
        
        normalize_edges = []
        for vertex, vertexes in self.graph.items():
            for v, _ in vertexes:
                normalize_edges.append((v, vertex))

        problem = pulp.LpProblem("Hamiltonial_cycle", pulp.LpMinimize)
        
        x = pulp.LpVariable.dicts("x", normalize_edges, cat="Binary")
                
        # Условие, что для каждой вершины должно быть по одному входящему и одному исходящему ребру
        # Это необходимо для построения гамильтонова цикла, так как каждая вершина должна быть посещена ровно один раз
        for u in range(num_vertexes):
            problem += (pulp.lpSum([x[u, v] for u_, v in normalize_edges if u_ == u]) == 1, f"Out_Degree_{u}")
        for v in range(num_vertexes):
            problem += (pulp.lpSum([x[u, v] for u, v_ in normalize_edges if v_ == v]) == 1, f"In_Degree_{v}")

        subsets = []
        for size in range(2, num_vertexes):
            for comb in combinations(range(num_vertexes), size):
                subsets.append(set(comb))
        
        # Исключаем подциклы, чтобы гарантировать, что цикл будет проходить по всем вершинам.
        for subset in subsets:
            # Если в каждом подмножестве ребер меньше, чем количество вершин подмножества, 
            # то все вершины подключаются единственным циклом и значит подциклов нет
            problem += (
                pulp.lpSum([x[u, v] for u in subset for v in subset if (
                    u, v) in normalize_edges]) <= len(subset) - 1,
                f"Subcycle_Elimination_{subset}"
            )

        solver = pulp.PULP_CBC_CMD(msg=False)
        status = problem.solve(solver)

        print(status)
        # Если задача решена и решение оптимальное, значит, граф содержит гамильтонов цикл.
        if pulp.LpStatus[status] == "Optimal":
            return True
        else:
            return False
            
