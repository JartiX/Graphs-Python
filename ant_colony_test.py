from graph.graph import Graph
from algorithm.ant_algorithm import AntColony


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
