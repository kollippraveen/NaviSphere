import math

def calculate_distance(p1, p2):
    # Standard Euclidean distance formula: sqrt((x2-x1)^2 + (y2-y1)^2)
    return math.sqrt((p2['x'] - p1['x'])**2 + (p2['y'] - p1['y'])**2)

def get_shortest_path(nodes, edges, start_node_name, end_node_name):
    # Create an adjacency list: { "NodeA": [("NodeB", weight), ("NodeC", weight)] }
    graph = {node['name']: [] for node in nodes}
    node_data = {node['name']: node for node in nodes}

    for edge in edges:
        n1, n2 = edge['start_node'], edge['end_node']
        dist = calculate_distance(node_data[n1], node_data[n2])
        graph[n1].append((n2, dist))
        graph[n2].append((n1, dist)) # Bidirectional path

    # Simple Dijkstra Implementation
    import heapq
    queue = [(0, start_node_name, [])]
    visited = set()
    distances = {node['name']: float('inf') for node in nodes}
    distances[start_node_name] = 0

    while queue:
        (cost, current_node, path) = heapq.heappop(queue)

        if current_node in visited:
            continue

        path = path + [current_node]
        visited.add(current_node)

        if current_node == end_node_name:
            return path

        for neighbor, weight in graph[current_node]:
            if neighbor not in visited:
                old_cost = distances.get(neighbor, float('inf'))
                new_cost = cost + weight
                if new_cost < old_cost:
                    distances[neighbor] = new_cost
                    heapq.heappush(queue, (new_cost, neighbor, path))

    return None