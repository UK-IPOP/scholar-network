from collections import defaultdict
from dataclasses import InitVar, dataclass, field
from typing import Union


@dataclass
class CustomCounter:
    lst: InitVar[list[tuple[str, str]]]
    counts: dict[tuple[str, str], int] = field(init=False)

    def __post_init__(self, lst):
        result = defaultdict(int)
        for pair in lst:
            # by sorting we can ensure we catch the 'reflexive tuples'
            sorted_pair = tuple(sorted(pair))
            result[sorted_pair] += 1
        self.counts = result

    def most_common(
        self, limit: Union[int, None] = None
    ) -> list[tuple[tuple[str, str], int]]:
        ordered_keys = sorted(self.counts, key=lambda x: self.counts[x], reverse=True)
        ordered_result: list[tuple[tuple[str, str], int]] = []
        for item in ordered_keys:
            ordered_result.append((item, self.counts[item]))
        return ordered_result[:limit] if limit else ordered_result


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

    # * start analytics section
    # * basics
    def vertex_count(self) -> int:
        return sum(len(self.children(node)) for node in self.edges)

    def edge_count(self) -> int:
        return len(self.edges)

    def vertex_degree(self, vertex: Union[Node, None] = None) -> Union[int, list[int]]:
        if vertex:
            return len(self.children(vertex))
        return sorted([len(self.children(n)) for n in self.edges])

    # * advanced
    def edge_rank(
        self, vertex: Union[Node, None] = None, limit: Union[int, None] = None
    ) -> list[tuple[tuple[str, str], int]]:
        if vertex:
            pairs = []
            for partner in self.edges[vertex]:
                pairs.append((vertex.name, partner.name))

            return (
                CustomCounter(pairs).most_common(limit)
                if limit
                else CustomCounter(pairs).most_common()
            )
        return (
            CustomCounter(self.node_pairs()).most_common(limit)
            if limit
            else CustomCounter(self.node_pairs()).most_common()
        )


@dataclass
class Graph(Digraph):
    def add_edge(self, edge: Edge):
        Digraph.add_edge(self, edge)
        rev = Edge(edge.dest, edge.src)
        Digraph.add_edge(self, rev)
