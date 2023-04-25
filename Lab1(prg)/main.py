import sys
import re


class DisjointSet:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, vertice):
        if self.parent[vertice] != vertice:
            self.parent[vertice] = self.find(self.parent[vertice])
        return self.parent[vertice]

    def union(self, vertice1, vertice2):
        root1 = self.find(vertice1)
        root2 = self.find(vertice2)
        if root1 != root2:
            if self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            else:
                self.parent[root1] = root2
                if self.rank[root1] == self.rank[root2]:
                    self.rank[root2] += 1


def open_file():
    try:
        return open("l1_2.txt")
    except FileNotFoundError:
        print("File not exist.")
        exit()

    fileName = sys.argv[1]
    try:
        return open(fileName)
    except FileNotFoundError:
        print("File not exist.")
        exit()


def kruskal(graph):
    size = len(graph['vertices'])
    disjoint_set = DisjointSet(size)

    edges = sorted(graph['edges'])
    min_spanning_tree = []
    tree_weight = 0
    for edge in edges:
        weight, vertice1, vertice2 = edge
        if disjoint_set.find(vertice1) != disjoint_set.find(vertice2):
            disjoint_set.union(vertice1, vertice2)
            min_spanning_tree.append(edge)
            tree_weight += weight

    return min_spanning_tree, tree_weight


file = open_file()

size = int(file.readline())
vertices = list(range(size))

edges = []
for line_index, line in enumerate(file):
    for index, node in enumerate(re.split('\s', re.sub('\n', '', line))):
        if line_index == index or node == '0': continue
        edges.append((int(node), line_index, index))

graph = {'vertices': vertices, 'edges': edges}

min_spanning_tree, tree_weight = kruskal(graph)

print("Minimum spanning tree:")
for weight, vertice1, vertice2 in min_spanning_tree:
    print(f"{vertice1}->{vertice2} ({weight})", end="; ")
print(f"\nWeight of the minimum spanning tree: {tree_weight}")