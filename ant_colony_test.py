from graph.graph import Graph
from algorithm.ant_algorithm import AntColony


# Поиск кратчайшего гамильтонова цикла используя муравьиный алгоритм
gr = Graph(True)
gr.add_edge(0, 1, 3)
gr.add_edge(0, 4, 1)
gr.add_edge(1, 0, 3)
gr.add_edge(1, 5, 3)
gr.add_edge(1, 2, 18)
gr.add_edge(2, 1, 3)
gr.add_edge(2, 5, 1)
gr.add_edge(2, 3, 1)
gr.add_edge(3, 4, 1)
gr.add_edge(3, 2, 8)
gr.add_edge(5, 0, 3)
gr.add_edge(5, 1, 3)
gr.add_edge(5, 4, 4)
gr.add_edge(5, 2, 3)
gr.add_edge(5, 3, 5)
gr.add_edge(4, 3, 3)
gr.add_edge(4, 0, 3)

print(gr)

num_ants = 100
num_iterations = 100
alpha = 1
beta = 2
evaporation_rate = 0.3
alpha_ant_ratio = 0.2

aco = AntColony(gr, num_ants, num_iterations,
                alpha, beta, evaporation_rate, alpha_ant_ratio=alpha_ant_ratio)


best_route, best_distance = aco.run(visualize=False)
print("Лучший маршрут:", best_route)
print("Лучшее расстояние:", best_distance)
