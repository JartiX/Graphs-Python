from graph.graph import Graph
from algorithm.dijkstra_algorithm import dijkstra

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

gr1 = Graph(False)
gr1.add_edge(0, 2, 6)
gr1.add_edge(0, 1, 1)
gr1.add_edge(1, 8, 2)
gr1.add_edge(2, 5, 2)
gr1.add_edge(2, 4, 1)
gr1.add_edge(3, 6, 6)
gr1.add_edge(3, 1, 1)
gr1.add_edge(3, 7, 3)
gr1.add_edge(4, 5, 7)
gr1.add_edge(4, 3, 7)
gr1.add_edge(5, 6, 3)
gr1.add_edge(5, 3, 3)
gr1.add_edge(6, 1, 4)
gr1.add_edge(7, 1, 2)
gr1.add_edge(7, 8, 4)
gr1.add_edge(8, 0, 6)

# Неориентированный
print(f"Shortest path from a to d: {dijkstra(gr, 'a', 'd')}")

# Ориентированный
print(f"Shortest path from 0 to 8: {dijkstra(gr1, 1, 5)}")
