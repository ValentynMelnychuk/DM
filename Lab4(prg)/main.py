import re
from collections import defaultdict
import PySimpleGUI as sg


class Graph:
    def __init__(self, graph):
        self.graph = graph  # residual graph
        self.ROW = len(graph)

    def BFS(self, s, t, parent):
        visited = [False] * self.ROW
        queue = []
        queue.append(s)
        visited[s] = True

        while queue:
            u = queue.pop(0)
            for ind, val in enumerate(self.graph[u]):
                if not visited[ind] and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u

        return visited[t]

    def FordFulkerson(self, source, sink):
        parent = [-1] * self.ROW
        max_flow = 0

        while self.BFS(source, sink, parent):
            path_flow = float("Inf")
            s = sink
            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            max_flow += path_flow

            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

        return max_flow


def load_file():
    layout = [[sg.Text('Choose a file')],
              [sg.In(), sg.FileBrowse()],
              [sg.Open(), sg.Cancel()]]
    window = sg.Window('Maximum Flow', layout)
    event, values = window.read(close=True)
    filename = values[0] if event == 'Open' else None
    return filename


def process_file(filename):
    if not filename:
        raise SystemExit("Cancelling: no filename supplied...")
    with open(filename, "r") as f:
        contents = f.read()
        contents = re.split(r'[,\s]\s*', contents)

    a = contents[0::8]
    b = contents[1::8]
    c = contents[2::8]
    d = contents[3::8]
    e = contents[4::8]
    f = contents[5::8]
    g = contents[6::8]
    h = contents[7::8]

    graphset = []
    for item in range(len(a)):
        graph = [int(a[item]), int(b[item]), int(c[item]), int(d[item]), int(e[item]), int(f[item]), int(g[item]), int(h[item])]
        graphset.append(graph)

    return Graph(graphset)


filename = load_file()
g = process_file(filename)
source = 0
sink = 7
print("The maximum possible flow is %d " % g.FordFulkerson(source, sink))