from graph.graph import Graph
import heapq


def dijkstra(graph: Graph, start: int | str, end: int | str):
    distances = {vertex: float('inf') for vertex in graph.graph}
    distances[start] = 0
    priority_queue = [(0, start)]  # (расстояние, вершина)
    # Для восстановления пути
    previous_vertices = {vertex: None for vertex in graph.graph}

    while priority_queue:
        # Извлекаем вершину с наименьшим расстоянием
        current_distance, current_vertex = heapq.heappop(priority_queue)

        # Если мы достигли конечной вершины, восстанавливаем путь
        if current_vertex == end:
            path = []
            while current_vertex:
                path.insert(0, current_vertex)
                current_vertex = previous_vertices[current_vertex]
            return distances[end], path  # Возвращаем расстояние и сам путь

        # Если текущее расстояние больше записанного, пропускаем
        if current_distance > distances[current_vertex]:
            continue

        # Обходим соседей текущей вершины
        for neighbor, weight in graph.graph[current_vertex]:
            distance = current_distance + weight

            # Если найден более короткий путь, обновляем его
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_vertices[neighbor] = current_vertex
                # Добавляем соседа в очередь с приоритетом по расстоянию
                heapq.heappush(priority_queue, (distance, neighbor))

    return float('inf'), []
