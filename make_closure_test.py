from graph.graph import Graph
from algorithm.ant_algorithm import AntColony

# Поиск кратчайшего гамильтонова цикла используя муравьиный алгоритм
gr1 = Graph(False)
gr1.add_edge(0, 2, 6)
gr1.add_edge(2, 5, 2)
gr1.add_edge(3, 6, 6)
gr1.add_edge(3, 7, 3)
gr1.add_edge(4, 5, 7)
gr1.add_edge(4, 3, 7)
gr1.add_edge(5, 6, 3)
gr1.add_edge(5, 3, 3)
gr1.add_edge(6, 1, 4)
gr1.add_edge(7, 8, 4)
gr1.add_edge(8, 0, 6)

print('Граф до замыкания:\n', gr1)

has_cycle = gr1.has_hamiltonial_cycle()

if not has_cycle:
    gr1.make_closure()

    print('\n\nГраф после замыкания: \n', gr1.graph)

    if gr1.has_hamiltonial_cycle():
        print('Граф имеет гамильтонов цикл')
    else:
        print('Граф не имеет гамильтонова цикла')

    num_ants = 30
    num_iterations = 10
    alpha = 1
    beta = 2
    evaporation_rate = 0.3

    aco = AntColony(gr1, num_ants, num_iterations,
                    alpha, beta, evaporation_rate)

    best_route, best_distance = aco.run(visualize=False)

    print("Лучший маршрут:", best_route)
    print("Лучшее расстояние:", best_distance)
