import heapq
from Vertex import Vertex

"""
Graph Class
----------

This class represents the Graph modelling our courier network. 

Each Graph consists of the following properties:
    - vertices: A list of vertices comprising the graph

The class also supports the following functions:
    - add_vertex(vertex): Adds the vertex to the graph
    - remove_vertex(vertex): Removes the vertex from the graph
    - add_edge(vertex_A, vertex_B): Adds an edge between the two vertices
    - remove_edge(vertex_A, vertex_B): Removes an edge between the two vertices
    - send_message(s, t): Returns a valid path from s to t containing at most one untrusted vertex
    - check_security(s, t): Returns the set of edges that, if any are removed, would result in any s-t path having to use an untrusted edge

Your task is to complete the following functions which are marked by the TODO comment.
Note that your modifications to the structure of the Graph should be correctly updated in the underlying Vertex class!
You are free to add properties and functions to the class as long as the given signatures remain identical.
"""


class Graph():
    # These are the defined properties as described above
    vertices: 'list[Vertex]'

    def __init__(self) -> None:
        """
        The constructor for the Graph class.
        """
        self.vertices = []

    

    def add_vertex(self, vertex: Vertex) -> None:
        """
        Adds the given vertex to the graph.
        If the vertex is already in the graph or is invalid, do nothing.
        :param vertex: The vertex to add to the graph.
        """

        if vertex not in self.vertices:
            self.vertices.append(vertex)

        return

    def remove_vertex(self, vertex: Vertex) -> None:
        """
        Removes the given vertex from the graph.
        If the vertex is not in the graph or is invalid, do nothing.
        :param vertex: The vertex to remove from the graph.
        """

        if vertex in self.vertices:
            self.vertices.remove(vertex)
        return

    def add_edge(self, vertex_A: Vertex, vertex_B: Vertex) -> None:
        """
        Adds an edge between the two vertices.
        If adding the edge would result in the graph no longer being simple or the vertices are invalid, do nothing.
        :param vertex_A: The first vertex.
        :param vertex_B: The second vertex.
        """

        vertex_A.add_edge(vertex_B)
        return

    def remove_edge(self, vertex_A: Vertex, vertex_B: Vertex) -> None:
        """
        Removes an edge between the two vertices.
        If an existing edge does not exist or the vertices are invalid, do nothing.
        :param vertex_A: The first vertex.
        :param vertex_B: The second vertex.
        """

        vertex_A.remove_edge(vertex_B)
        return

    def send_message(self, s: Vertex, t: Vertex) -> 'list[Vertex]':
        """
        Returns a valid path from s to t containing at most one untrusted vertex.
        Any such path between s and t satisfying the above condition is acceptable.
        Both s and t can be assumed to be unique and trusted vertices.
        If no such path exists, return None.
        :param s: The starting vertex.
        :param t: The ending vertex.
        :return: A valid path from s to t containing at most one untrusted vertex.
        """
        D = {v:float('inf') for v in self.vertices}
        parents = {v:None for v in self.vertices}

        D[s] = 0
        visited = []
    
        pq = [(0, s)]
    
        while len(pq) > 0:
            (current_distance, current_vertex) = heapq.heappop(pq)
            visited.append(current_vertex)

            for neighbour in current_vertex.get_edges() :
                distance = current_distance + int(not neighbour.get_is_trusted())
                if distance < D[neighbour]:
                    D[neighbour] = distance
                    heapq.heappush(pq, (distance,neighbour))
                    parents[neighbour] = current_vertex
        
        if D[t] <= 1:
            #Found
            path = []
            current_vertex = t
            while current_vertex != s:
                path.append(current_vertex)
                current_vertex = parents[current_vertex]
            path.append(s)
            path.reverse()
            return path


        return None

    def send_message_max(self, s: Vertex, t: Vertex) -> 'list[Vertex]':

        D = {v:float('inf') for v in self.vertices}
        parents = {v:None for v in self.vertices}

        D[s] = 0
        visited = []
    
        pq = [(0, s)]
    
        while len(pq) > 0:
            (current_distance, current_vertex) = heapq.heappop(pq)
            visited.append(current_vertex)

            for neighbour in current_vertex.get_edges():
                if neighbour.get_is_trusted() == False and current_vertex.get_is_trusted() == False:
                    continue
                distance = current_distance + int(not neighbour.get_is_trusted())
                if distance < D[neighbour]:
                    D[neighbour] = distance
                    heapq.heappush(pq, (distance,neighbour))
                    parents[neighbour] = current_vertex
        
        if D[t] != float('inf'): 
            #Found
            path = []
            current_vertex = t
            while current_vertex != s:
                path.append(current_vertex)
                current_vertex = parents[current_vertex]
            path.append(s)
            path.reverse()
            return path


        return None


    def check_security(self, s: Vertex, t: Vertex) -> 'list[(Vertex, Vertex)]':
        """
        Returns the list of edges as tuples of vertices (v1, v2) such that the removal 
        of the edge (v1, v2) means a path between s and t is not possible or must use
        two or more untrusted vertices in a row. v1 and v2 must also satisfy the criteria
        that exactly one of v1 or v2 is trusted and the other untrusted.        
        Both s and t can be assumed to be unique and trusted vertices.
        :param s: The starting vertex
        :param t: The ending vertex
        :return: A list of edges which, if removed, means a path from s to t uses an untrusted edge or is no longer possible. 
        Note these edges can be returned in any order and are unordered.
        """
        cut_edges = []

        all_edges = []

        for v in self.vertices:
            for e in v.get_edges():
                if (e,v) not in all_edges and (v,e) not in all_edges:
                    all_edges.append((v,e))

        for e in all_edges:
            if (e[0].get_is_trusted() ^ e[1].get_is_trusted()):
                self.remove_edge(e[0], e[1])
                if self.send_message_max(s,t) == None:
                    cut_edges.append(e)
                            
                self.add_edge(e[0], e[1])
            else:
                continue

        return cut_edges