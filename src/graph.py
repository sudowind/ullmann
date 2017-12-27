import numpy as np


class Vertex(object):

    def __init__(self, vid, label):
        self.vid = vid
        self.vlb = label
        self.neighbors = []

    def add_neighbor(self, v):
        self.neighbors.append(v)


class Edge(object):

    def __init__(self, start, end, label):
        self.start = start
        self.end = end
        self.elb = label


class Graph(object):

    def __init__(self):
        self.vertices = []
        self.edges = []
        self.matrix = None

    def add_vertex(self, vid, label):
        self.vertices.append(Vertex(int(vid), label))

    def add_edges(self, start, end, label):
        start = int(start)
        end = int(end)
        self.edges.append(Edge(start, end, label))
        self.vertices[start].add_neighbor(self.vertices[end])
        self.edges.append(Edge(end, start, label))
        self.vertices[end].add_neighbor(self.vertices[start])

    def get_matrix(self):
        if self.matrix is not None:
            return self.matrix
        else:
            self.matrix = np.zeros((len(self.vertices), len(self.vertices)))
            for v_from in self.vertices:
                for v_to in v_from.neighbors:
                    self.matrix[v_from.vid][v_to.vid] = 1
            return self.matrix

    def show(self):
        for i in self.vertices:
            print(i.vid, i.vlb,)
            for j in i.neighbors:
                print((j.vid, j.vlb), )
        print((self.get_matrix()))
