from graph.graph import Graph
from algorithm.dijkstra_algorithm import dijkstra
from algorithm.ant_algorithm import AntColony
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


# Поиск кратчайшего гамильтонова цикла используя муравьиный алгоритм
gr = Graph(True)
gr.add_edge('a', 'b', 3)
gr.add_edge('b', 'a', 3)
gr.add_edge('g', 'a', 3)
gr.add_edge('g', 'b', 3)
gr.add_edge('b', 'g', 3)
gr.add_edge('b', 'c', 8)
gr.add_edge('c', 'b', 3)
gr.add_edge('c', 'g', 1)
gr.add_edge('g', 'c', 3)
gr.add_edge('g', 'd', 5)
gr.add_edge('c', 'd', 1)
gr.add_edge('d', 'c', 8)
gr.add_edge('g', 'f', 4)
gr.add_edge('d', 'f', 1)
gr.add_edge('f', 'd', 3)
gr.add_edge('f', 'a', 3)
gr.add_edge('a', 'f', 1)
print(gr.graph)

num_ants = 10
num_iterations = 40
alpha = 1.0
beta = 2.0
evaporation_rate = 0.1

aco = AntColony(gr, num_ants, num_iterations,
                alpha, beta, evaporation_rate)
best_route, best_distance = aco.run()

print("Лучший маршрут:", best_route)
print("Лучшее расстояние:", best_distance)
