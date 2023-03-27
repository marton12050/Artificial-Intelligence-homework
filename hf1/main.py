import sys
import math
from collections import defaultdict


def make_graph(edge_list):
    graph = defaultdict(list)
    for src, dst, weight in edge_list:
        graph[src].append((dst, weight))
        graph[dst].append((src, weight))
    return graph


def dijkstra(graph, src, dst):
    que = set(graph)
    print(que)
    print(graph)
    dist = dict()
    for n in que:
        dist[n] = sys.maxsize

    dist[src] = 0

    while que:
        kövi = min(que, key=dist.get)
        que.remove(kövi)

        if kövi == dst:
            return dist[dst]

        for nxt, dis in graph.get(kövi):
            alt = dist[kövi] + dis
            if alt < dist[nxt]:
                dist[nxt] = alt

    return sys.maxsize


def distance(node1, node2):
    x = x_y[node1][0] - x_y[node2][0]
    y = x_y[node1][1] - x_y[node2][1]
    return math.sqrt(x**2+y**2)


data = sys.stdin.read().split("\n\n")

p, n, e = (int(x) for x in data[0].split("\n"))

ide_oda = [[int(y) for y in x.split("\t")] for x in data[1].split("\n")]
x_y = [[int(y) for y in x.split("\t")] for x in data[2].split("\n")]
neighbours = [[int(y) for y in x.split("\t")] for x in data[3].split("\n") if x != ""]

graphneighbour = []
for i in range(e):
    graphneighbour.append((neighbours[i][0], neighbours[i][1], distance(neighbours[i][0], neighbours[i][1])))

g = make_graph(graphneighbour)

for src, des in ide_oda:
    print("{}\t".format(round(dijkstra(g, src, des), 2)), end="")
