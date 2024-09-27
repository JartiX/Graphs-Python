from graph.graph import Graph

g = Graph()
g.add_edge(1, 2, 1)
g.add_edge(1, 3, 1)
g.add_edge(3, 2, 5)
g.add_edge(2, 4, 1)

print(g)

start = 4
end = 3
print(f"Shortest path from {start} to {end}: {g.dijkstra(start, end)}")
