from graph.graph import Graph
import pulp
from itertools import combinations


def __ore_dirak_condition(graph: Graph):
    num_vertexes = len(graph.nodes.keys())
    p = num_vertexes/2
    # Условие Дирака (достаточное): если в графе с n вершинами каждая вершина имеет степень не менее n/2, то в графе существует гамильтонов цикл
    # Условие Оре (достаточное): если для каждой пары вершин (u, v) графа,  не связанных между собой, выполняется условие: deg(u) + deg(v) >= n, то граф содержит гамильтонов цикл.
    for vertex1, vertexes1 in graph.nodes.items():
        if len(vertexes1.edges) < p:
            return False
        for vertex2, vertexes2 in graph.nodes.items():
            if vertex1 != vertex2 and not graph.is_adjacent(vertex1, vertex2):
                if len(vertexes1.edges) + len(vertexes2.edges) < num_vertexes:
                    return False
    return True


def __necessary_condition(graph: Graph):
    # Необходимое условие: если для какой-либо вершины степень меньше 2, гамильтонов цикл невозможен,
    # так как цикл должен проходить через все вершины.
    for vertexes in graph.nodes.values():
        if len(vertexes.edges) < 2:
            return False
    return True


def make_closure_bondi(graph: Graph):
    # Замыкание графа по теореме Бонди-Хваталя
    num_vertexes = len(graph.nodes.keys())
    for vertex1, vertexes1 in graph.nodes.items():
        for vertex2, vertexes2 in graph.nodes.items():
            if vertex1 != vertex2:
                if len(vertexes1.edges) + len(vertexes2.edges) >= num_vertexes:
                    # Проверим, являются ли они смежными
                    if not graph.is_adjacent(vertex1, vertex2):
                        # Добавляем ребро
                        graph.add_edge(vertex1, vertex2)


def make_closure(graph: Graph):
    # Строим замыкание графа для получения гамильтонова цикла
    vertices = list(graph.nodes.keys())
    num_vertices = len(vertices)
    added_edges = list()

    # Пока граф не удовлетворяет условиям для гамильтонова цикла, добавляем ребра
    while not __ore_dirak_condition(graph):
        # Найти пару несмежных вершин с максимальной суммой степеней
        for i in range(num_vertices):
            for j in range(i + 1, num_vertices):
                u, v = vertices[i], vertices[j]
                if not graph.is_adjacent(u, v) and ((len(graph.get_neighbors(u)) + len(graph.get_neighbors(v)) < num_vertices)
                                                    or len(graph.get_neighbors(u)) < num_vertices/2 or len(graph.get_neighbors(v)) < num_vertices/2):
                    if (u, v) not in added_edges:
                        graph.add_edge(u, v)
                        added_edges.append((u, v))
        if added_edges:
            print("Добавленные ребра:", added_edges)


def has_hamiltonial_cycle(graph: Graph):
    num_vertexes = len(graph.nodes.keys())

    # Если число вершин в графе меньше 3, то гамильтонов цикл невозможен
    if num_vertexes < 3:
        return False

    # Если условия Дирака или Оре выполняются, значит гамильтонов цикл есть, однако если они не выполняются это не гарантирует его отсутствия, т.к эти условия достаточные, а не необходимые

    if __ore_dirak_condition(graph):
        print("Выполнилось условия Дирака-Оре")
        return True

    # Если необходимое условие выполняется, нельзя гарантировать, что гамильтонов цикл есть, однако если это условие не выполняется, то цикла точно нет

    if not __necessary_condition(graph):
        print("Необходимое условие не выполнилось.")
        return False

    # Задача сводится к нахождению хода через все вершины без подциклов, что соответствует гамильтоновому циклу.

    normalize_edges = []
    for vertex, vertexes in graph.nodes.items():
        for v, _ in vertexes:
            normalize_edges.append((v, vertex))

    problem = pulp.LpProblem("Hamiltonial_cycle", pulp.LpMinimize)

    x = pulp.LpVariable.dicts("x", normalize_edges, cat="Binary")

    # Условие, что для каждой вершины должно быть по одному входящему и одному исходящему ребру
    # Это необходимо для построения гамильтонова цикла, так как каждая вершина должна быть посещена ровно один раз
    for u in range(num_vertexes):
        problem += (pulp.lpSum([x[u, v]
                    for u_, v in normalize_edges if u_ == u]) == 1, f"Out_Degree_{u}")
    for v in range(num_vertexes):
        problem += (pulp.lpSum([x[u, v]
                    for u, v_ in normalize_edges if v_ == v]) == 1, f"In_Degree_{v}")

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

