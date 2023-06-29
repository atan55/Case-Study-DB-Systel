"""A graph path discovery coding task.

In this file, you are presented with the task to implement the function `compute_shortest_paths`
which discovers some shortest paths from a start node to an end node in an undirected weighted graph
with strictly positive edge lengths. The function is marked with "TODO: Write" below and carries a
more precise specification of the expected behavior in its docstring.

Please write the implementation with the highest quality standards in mind which you would also use
for production code. Functional correctness is the most important criterion. After that it will be
evaluated in terms of maintainability and wall clock runtime for large graphs (in decreasing order
of importance). Please submit everything you have written, including documentation and tests.

Your implementation of `compute_shortest_paths` should target Python 3.9 and not use any external
dependency except for the Python standard library. Outside of the implementation of
`compute_shortest_paths` itself, you are free to use supporting libraries as long as they are
available on PyPi.org. If you use additional packages, please add a requirements.txt file which
lists them with their precise versions ("packageA==1.2.3").
"""
from functools import total_ordering
from typing import Any, List, Optional, List, Tuple, cast
import time as t

class Node:
    """A node in a graph."""

    def __init__(self, id: int):
        self.id: int = id
        self.adjacent_edges: List["UndirectedEdge"] = []

    def edge_to(self, other: "Node") -> Optional["UndirectedEdge"]:
        """Returns the edge between the current node and the given one (if existing)."""
        matches = [edge for edge in self.adjacent_edges if edge.other_end(self) == other]
        return matches[0] if len(matches) > 0 else None

    def is_adjacent(self, other: "Node") -> bool:
        """Returns whether there is an edge between the current node and the given one."""
        return other in {edge.other_end(self) for edge in self.adjacent_edges}

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Node) and self.id == other.id

    def __le__(self, other: Any) -> bool:
        return isinstance(other, Node) and self.id <= other.id

    def __hash__(self) -> int:
        return self.id

    def __repr__(self) -> str:
        return f"Node({self.id})"


class UndirectedEdge:
    """An undirected edge in a graph."""

    def __init__(self, end_nodes: Tuple[Node, Node], length: float):
        self.end_nodes: Tuple[Node, Node] = end_nodes
        if 0 < length:
            self.length: float = length
        else:
            raise ValueError(
                f"Edge connecting {end_nodes[0].id} and {end_nodes[1].id}: "
                f"Non-positive length {length} not supported."
            )

        if any(e.other_end(end_nodes[0]) == end_nodes[1] for e in end_nodes[0].adjacent_edges):
            raise ValueError("Duplicate edges are not supported")

        if self.end_nodes[0] != self.end_nodes[1]:
            self.end_nodes[0].adjacent_edges.append(self)
            self.end_nodes[1].adjacent_edges.append(self)
            self.end_node_set = set(self.end_nodes)

    def other_end(self, start: Node) -> Node:
        """Returns the other end of the edge, given one of the end nodes."""
        return self.end_nodes[0] if self.end_nodes[1] == start else self.end_nodes[1]

    def is_adjacent(self, other_edge: "UndirectedEdge") -> bool:
        """Returns whether the current edge shares an end node with the given edge."""
        return len(self.end_node_set.intersection(other_edge.end_node_set)) > 0

    def __repr__(self) -> str:
        return (
            f"UndirectonalEdge(({self.end_nodes[0].__repr__()}, "
            f"{self.end_nodes[1].__repr__()}), {self.length})"
        )


class UndirectedGraph:
    """A simple undirected graph with edges attributed with their length."""

    def __init__(self, edges: List[UndirectedEdge]):
        self.edges: List[UndirectedEdge] = edges
        self.nodes_by_id = {node.id: node for edge in self.edges for node in edge.end_nodes}


@total_ordering
class UndirectedPath:
    """An undirected path through a given graph."""

    def __init__(self, nodes: List[Node]):
        assert all(
            node_1.is_adjacent(node_2) for node_1, node_2 in zip(nodes[:-1], nodes[1:])
        ), "Path edges must be a chain of adjacent nodes"
        self.nodes: List[Node] = nodes
        self.length = sum(
            cast(UndirectedEdge, node_1.edge_to(node_2)).length
            for node_1, node_2 in zip(nodes[:-1], nodes[1:])
        )

    @property
    def start(self) -> Node:
        return self.nodes[0]

    @property
    def end(self) -> Node:
        return self.nodes[-1]

    def prepend(self, edge: UndirectedEdge) -> "UndirectedPath":
        if self.start not in edge.end_nodes:
            raise ValueError("Edge is not adjacent")
        return UndirectedPath([edge.other_end(self.start)] + self.nodes)

    def append(self, edge: UndirectedEdge) -> "UndirectedPath":
        if self.end not in edge.end_nodes:
            raise ValueError("Edge is not adjacent")
        return UndirectedPath(self.nodes + [edge.other_end(self.end)])

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, UndirectedPath) and self.nodes == other.nodes

    def __le__(self, other: Any) -> bool:
        return isinstance(other, UndirectedPath) and self.length <= other.length

    def __hash__(self) -> int:
        return hash(n.id for n in self.nodes)

    def __repr__(self) -> str:
        nodestr: str = ", ".join([node.__repr__() for node in self.nodes])
        return f"UndirectedPath([{nodestr}])"

listerAllerPfadeVonAZuAllenKnoten = {}

def compute_shortest_paths(
    graph: UndirectedGraph, start: Node, end: Node, length_tolerance_factor: float
) -> List[UndirectedPath]:
    """Computes and returns the N shortest paths between the given end nodes."""

    if (start, end) in listerAllerPfadeVonAZuAllenKnoten:
        return listerAllerPfadeVonAZuAllenKnoten[(start,end)]
    else:


        distances = {}
        for _, node in graph.nodes_by_id.items():
            
            distances[node] = float("inf")

        distances[start] = 0
        warteschlange = []
        erledigt = []
        ausgewählt = start
        vorgänger = {}
        zähleDurchläufe = 0
        listeKnoten = []

        while True:
            zähleDurchläufe += 1
            nachfolger = []

            for edge in ausgewählt.adjacent_edges:
                if edge.other_end(ausgewählt) not in erledigt:
                    nachfolger.append(edge.other_end(ausgewählt))
                if (edge.other_end(ausgewählt) not in warteschlange) and (edge.other_end(ausgewählt) not in erledigt):
                    warteschlange.append(edge.other_end(ausgewählt))

            for n in nachfolger:
                if (ausgewählt.edge_to(n) not in erledigt) and (ausgewählt.edge_to(n) not in vorgänger):
                    new_distance = distances[ausgewählt] + ausgewählt.edge_to(n).length

                    if new_distance < distances[n]:
                        distances[n] = new_distance
                        vorgänger[n] = ausgewählt

            if ausgewählt not in erledigt:
                erledigt.append(ausgewählt)

            if len(erledigt) == 5:
                break

            if ausgewählt in warteschlange:
                warteschlange.remove(ausgewählt)

            if len(warteschlange) > 1:
                nHilf = warteschlange[0]
                for n in warteschlange[1:]:
                    if distances[nHilf] > distances[n]:
                        nHilf = n
                ausgewählt = nHilf
            elif len(warteschlange) == 1:
                ausgewählt = warteschlange[0]
            else:
                break

        vorgänger_umgedreht = {}
        for schlüssel, wert in vorgänger.items():
            vorgänger_umgedreht.setdefault(wert, []).append(schlüssel)
        #print("vorgänger_umgedreht Ende: ", vorgänger_umgedreht)

        #vorgänger_umgedreht = {wert: schlüssel for schlüssel, wert in vorgänger.items()}
        print("vorgänger Ende: ", vorgänger)
        print("vorgänger_umgedreht: ", vorgänger_umgedreht)

        listeKnoten.append(end)
        knotenHilf = vorgänger[end]

        for i in range(len(vorgänger)-1):
            listeKnoten.append(knotenHilf)
            if knotenHilf in vorgänger:
                knotenHilf = vorgänger[knotenHilf]
            else:
                break

        listeKnoten.reverse()
        print("Liste des Pfades: ", listeKnoten)

        p = UndirectedPath(listeKnoten)

        s = start
        e = end
        listerAllerPfadeVonAZuAllenKnoten[(s,e)]=p

        listeSchlüssel = vorgänger.keys()
        for i in listeSchlüssel: 
            listeNeuerPfad = [i]
            e = i
            if i == end or i == start:
                continue
            else:
                while True:
                    if i in vorgänger:
                        listeNeuerPfad.append(vorgänger[i])
                        i = vorgänger[i]
                    else:
                        listeNeuerPfad.reverse()
                        if not (s,e) in listerAllerPfadeVonAZuAllenKnoten: 
                            listerAllerPfadeVonAZuAllenKnoten[(s,e)] = (UndirectedPath(listeNeuerPfad))
                        break

        return [p]

    

# Usage example
n1, n2, n3, n4, n5 = Node(1), Node(2), Node(3), Node(4), Node(5)
demo_graph = UndirectedGraph(
    [
        UndirectedEdge((n1, n2), 20),
        UndirectedEdge((n1, n5), 10),
        UndirectedEdge((n2, n5), 20),
        UndirectedEdge((n2, n4), 50),
        UndirectedEdge((n2, n3), 20),
        UndirectedEdge((n3, n4), 10),
        UndirectedEdge((n5, n4), 50),
        
    ]
)

print("n4->n1: ", compute_shortest_paths(demo_graph, n4, n1, 1.0))
print("n4->n2: ", compute_shortest_paths(demo_graph, n4, n2, 1.0))
print("n1->n3: ", compute_shortest_paths(demo_graph, n1, n3, 1.0))
print("n2->n5: ", compute_shortest_paths(demo_graph, n2, n5, 1.0))
print("n3->n5: ", compute_shortest_paths(demo_graph, n3, n5, 1.0))


print("\n\n\nAlle Pfade von A zu allen anderen Knoten: ", listerAllerPfadeVonAZuAllenKnoten)               
print("\nLänge von der Liste mit Allen Pfaden: ", len(listerAllerPfadeVonAZuAllenKnoten))
#In der Liste listeAllerPfadeVonAZuAllenKnoten sind jetzt alle Knoten von A zu allen anderen Knoten vorhanden.
#Sobald ich den kürzesten Pfad von A nach B suche, liefert die Methode diesen Pfad. Zusätzlich werden die kürzesten Wege
#zu allen anderen Knoten mit dem Dijkstra-Algorithmus berechnet und in der eben genannten Liste abgespeichert. 
#Somit müssen diese Pfade nicht erneut berechnet werden. Dieser Algorthmus ist sehr effektiv, denn
#indem man den kürzesten Pfad von A nach B berechnet, muss man sowieso alle Wege betrachten. 

# Should print the paths [1, 2, 4], [1, 3, 4], [1, 2, 4, 2, 4], [1, 2, 1, 2, 4], [1, 2, 4, 3, 4]
#print(compute_shortest_paths(demo_graph, n1, n4, 2.0))



