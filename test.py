
from collections import deque

# Code by Eryk Kopczyński
def find_shortest_path(graph, start, end):
    dist = {start: [start]}
    q = deque(start)
    while len(q):
        at = q.popleft()
        for next in graph[at]:
            if next not in dist:
                dist[next] = [dist[at], next]
                print(dist)
                q.append(next)
    return dist.get(end)

print('Hello World')
a = 10;
print(a)

#https://www.python.org/doc/essays/graphs/

graph = {'A': ['B', 'C'],
            'B': ['C', 'D'],
            'C': ['D'],
            'D': ['C','F'],
            'E': ['F'],
            'F': ['C','D']}
print(graph)

print(find_shortest_path(graph, 'A', 'D'))



