from dataclasses import dataclass, field


@dataclass(unsafe_hash=True)
class Node:
    __slots__ = "name"
    name: str

    def __str__(self) -> str:
        return self.name


@dataclass
class Edge:
    # TODO: add support for journal title as attribute of edge
    # TODO: want weight to track number of connections on each edge
    __slots__ = "src", "dest"
    src: Node
    dest: Node

    def __str__(self) -> str:
        return f"{self.src} -> {self.dest}"


@dataclass
class Digraph:
    edges: dict[Node, list[Node]] = field(default_factory=dict)

    def add_node(self, node: Node):
        if node not in self.edges:
            self.edges[node] = []
        else:
            pass

    def add_edge(self, edge: Edge):
        if not (edge.src in self.edges and edge.dest in self.edges):
            raise ValueError("Node not in graph")
        self.edges[edge.src].append(edge.dest)

    def children(self, node: Node) -> list[Node]:
        return self.edges[node]

    def has_node(self, node: Node) -> bool:
        return node in self.edges

    def get_node(self, name: str) -> Node:
        for n in self.edges:
            if n.name == name:
                return n
        raise NameError(name)

    def node_pairs(self) -> list[tuple[str, str]]:
        pairs = []
        for src in self.edges:
            for dest in self.edges[src]:
                pairs.append((src.name, dest.name))
        return pairs


@dataclass
class Graph(Digraph):
    def add_edge(self, edge: Edge):
        Digraph.add_edge(self, edge)
        rev = Edge(edge.dest, edge.src)
        Digraph.add_edge(self, rev)
