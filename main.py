from graph.graph import Graph
from algorithm.dijkstra_algorithm import dijkstra
from algorithm.ant_algorithm import AntColony
import time
import numpy as np

# # Алгоритм Дейкстры
# g = Graph()
# g.add_edge("a", "b", 1)
# g.add_edge("a", "c", 1)
# g.add_edge("c", "b", 1)
# g.add_edge("b", "d", 1)

# g1 = Graph(True)
# g1.add_edge(2, 1, 1)
# g1.add_edge(1, 3, 1)
# g1.add_edge(3, 2, 1)
# g1.add_edge(2, 4, 1)

# print(g)
# print(g1)
# # Неориентированный
# print(f"Shortest path from a to b: {dijkstra(g, 'a', 'b')}")
# # Ориентированный
# print(f"Shortest path from 1 to 3: {dijkstra(g1, 1, 3)}")


# Сложный граф
gr1 = Graph(False)
gr1.add_edge(0, 2, 6)
gr1.add_edge(0, 1, 1) #
gr1.add_edge(1, 8, 2) #
gr1.add_edge(2, 5, 2)
gr1.add_edge(2, 4, 1) #
gr1.add_edge(3, 6, 6)
gr1.add_edge(3, 1, 1) #
gr1.add_edge(3, 7, 3)
gr1.add_edge(4, 5, 7)
gr1.add_edge(4, 3, 7)
gr1.add_edge(5, 6, 3)
gr1.add_edge(5, 3, 3)
gr1.add_edge(6, 1, 4)
gr1.add_edge(7, 1, 2) #
gr1.add_edge(7, 8, 4)
gr1.add_edge(8, 0, 6)


# Поиск кратчайшего гамильтонова цикла используя муравьиный алгоритм
gr = Graph(True)
gr.add_edge('a', 'b', 3)
gr.add_edge('a', 'f', 1)
gr.add_edge('b', 'a', 3)
gr.add_edge('b', 'g', 3)
gr.add_edge('b', 'c', 18)
gr.add_edge('c', 'b', 3)
gr.add_edge('c', 'g', 1)
gr.add_edge('c', 'd', 1)
gr.add_edge('d', 'f', 1)
gr.add_edge('d', 'c', 8)
gr.add_edge('g', 'a', 3)
gr.add_edge('g', 'b', 3)
gr.add_edge('g', 'f', 4)
gr.add_edge('g', 'c', 3)
gr.add_edge('g', 'd', 5)
gr.add_edge('f', 'd', 3)
gr.add_edge('f', 'a', 3)

# print(gr1.graph)
# print(gr1.is_adjacent(1, 6))
# print(gr1.has_hamiltonial_cycle())
# print(gr.has_hamiltonial_cycle())
num_ants = 1000
num_iterations = 30
alpha = 1
beta = 2
evaporation_rate = 0.3


# print(gr1.graph)
# gr1.make_closure()
# print('\n', gr1.graph)

# print(gr1)


# aco = AntColony(gr, num_ants, num_iterations,
#                 alpha, beta, evaporation_rate)
# aco2 = AntColony(gr1, num_ants, num_iterations, alpha, beta, evaporation_rate)


# best_route, best_distance = aco2.run(visualize=True)
# print("Лучший маршрут:", best_route)
# print("Лучшее расстояние:", best_distance)
# gr1.make_closure()
# aco2 = AntColony(gr1, num_ants, num_iterations, alpha, beta, evaporation_rate)
# print(gr1)
# best_route, best_distance = aco2.run(visualize=True)
# print("Лучший маршрут:", best_route)
# print("Лучшее расстояние:", best_distance)


gr1000 = Graph()
with open('1000.txt', 'r') as f:
    for l in f:
        try:
            line = l.split()[0:3]
            if len(line) < 3:
                continue
            # print(line)
            gr1000.add_edge(int(line[0]), int(line[1]), int(line[2]))
        except:
            continue
# print(gr1000)
has_cycle = gr1000.has_hamiltonial_cycle()

if has_cycle:
    print("Гамильтонов цикл в грфе есть")
else:
    print('Гамильтонова цикла в графе нет')

gr1000.make_closure()
has_cycle = gr1000.has_hamiltonial_cycle()

if has_cycle:
    print("Гамильтонов цикл в грфе есть")
else:
    print('Гамильтонова цикла в графе нет')


# aco = AntColony(gr1000, 100000000, 1, 0.5, 0.5, 0.3)
# route, dist = aco.run(False)
# print(route, dist)
