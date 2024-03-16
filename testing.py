from Graph import Graph
from Vertex import Vertex

G = Graph()
A = Vertex(True)
A.name = 'A'
B = Vertex(False)
B.name = 'B'
C = Vertex(False)
C.name = 'C'
D = Vertex(True)
D.name = 'D'
E = Vertex(False)
E.name = 'E'
F = Vertex(True)
F.name = 'F'
H = Vertex(True)
H.name = 'H'

G.add_vertex(A)
G.add_vertex(B)
G.add_vertex(C)
G.add_vertex(D)
G.add_edge(A, B)
G.add_edge(A, C)
G.add_edge(B, D)
G.add_edge(C, D)

list = G.send_message(A,G)
for v in list:
    print(v.name)