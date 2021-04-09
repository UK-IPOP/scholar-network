"""This module contains the data models for building the network graph."""

from collections import defaultdict
from dataclasses import InitVar, dataclass, field
from typing import Union


@dataclass
class CustomCounter:
    """Custom counter class built to emulate Counter from std lib.

    This class utilizes a specific use case for this program, and
    uses 'reflexive tuple matching' to get synonymous pairs.

    Parameters:
        lst (list[tuple[str, str]]): A list of author-tuple pairs.
    """
    lst: InitVar[list[tuple[str, str]]]
    counts: dict[tuple[str, str], int] = field(init=False)

    def __post_init__(self, lst: list[tuple[str, str]]):
        """Converts author pairs into counts of unique pairs.

        After initialization, converts the list of tuple pairs into keys
        in a dictionary and increments the value by the count of the key.

        Also sorts the pairs so that reflexive tuples are caught.

        Stores the built dictionary in `self.counts`.

        Parameters:
            lst (list[tuple[str, str]]): A list of author-tuple pairs.
        """
        result = defaultdict(int)
        for pair in lst:
            # by sorting we can ensure we catch the 'reflexive tuples'
            sorted_pair = tuple(sorted(pair))
            result[sorted_pair] += 1
        self.counts = result

    def most_common(
        self, limit: Union[int, None] = None
    ) -> list[tuple[tuple[str, str], int]]:
        """Sorts and returns ordered tuple pairs.

        Args:
            limit (Union[int, None], optional): Limit to return. Defaults to None.

        Returns:
            list[tuple[tuple[str, str], int]]: Returns most common tuple pairs.
        """
        ordered_keys = sorted(self.counts, key=lambda x: self.counts[x], reverse=True)
        ordered_result: list[tuple[tuple[str, str], int]] = []
        for item in ordered_keys:
            ordered_result.append((item, self.counts[item]))
        return ordered_result[:limit] if limit else ordered_result


@dataclass(unsafe_hash=True)
class Node:
    """Node is a container to hold authors.

    Attributes:
        name (str): name of the author
    """
    __slots__ = "name"
    name: str

    def __str__(self) -> str:
        """Returns the name as the string.

        Returns:
            str: Name attribute of the node.
        """
        return self.name


@dataclass
class Edge:
    """Edge connects Nodes that co-occur together in the same publication.

    Edges are directed in a DiGraph and undirected in Graph.
    ^^ Both of these cases are handled by the (Di)Graph classes not the Edge itself.

    Attributes:
        src (Node): Source node for the connection.
        dest (Node): Destination node for the connection.
    """
    # TODO: add support for journal title as attribute of edge
    # TODO: want weight to track number of connections on each edge
    __slots__ = "src", "dest"
    src: Node
    dest: Node

    def __str__(self) -> str:
        """Makes the string representation an of the edge connection.

        Returns:
            str: Connection being represented by the edge in string form.
        """
        return f"{self.src} -> {self.dest}"


@dataclass
class Digraph:
    """Directed graph class.

    This class utilizes Node and Edge to store graph connections.

    Attributes:
        edges (dict[Node, list[Node]]): Connections stored as a dict of src node mapped to a list of connected nodes.  Repeats allowed.
    """
    edges: dict[Node, list[Node]] = field(default_factory=dict)

    def add_node(self, node: Node):
        """Adds a new node to the graph.

        Args:
            node (Node): New Node to add.
        """
        if node not in self.edges:
            self.edges[node] = []
        else:
            pass

    def add_edge(self, edge: Edge):
        """Adds a new edge/connection to the graph.

        Args:
            edge (Edge): Edge to add to the graph

        Raises:
            ValueError: Raises ValueError if either src or dest Nodes not in graph.
        """
        if not (edge.src in self.edges and edge.dest in self.edges):
            raise ValueError("Node not in graph")
        self.edges[edge.src].append(edge.dest)

    def children(self, node: Node) -> list[Node]:
        """Get's Nodes that `node` is linked to.

        Args:
            node (Node): Node to extract children from.

        Returns:
            list[Node]: List of Nodes connected to the target node. Duplicates allowed.
        """
        return self.edges[node]

    def has_node(self, node: Node) -> bool:
        """Checks if the graph contains a given Node.

        Args:
            node (Node): Node to search the graph for.

        Returns:
            bool: True if the node exists, otherwise False.
        """
        return node in self.edges

    def get_node(self, name: str) -> Node:
        """Gets a Node from the graph based on the Node's name attribute.

        Args:
            name (str): Name of the Node to return from the graph.

        Raises:
            NameError: If no matching Node can be found.

        Returns:
            Node: The Node matching the search name.
        """
        for n in self.edges:
            if n.name == name:
                return n
        raise NameError(name)

    def node_pairs(self) -> list[tuple[str, str]]:
        """Generates pairs of nodes representing edge connections.  Duplicates allowed.

        Returns:
            list[tuple[str, str]]: List of node pairs.
        """
        pairs = []
        for src in self.edges:
            for dest in self.edges[src]:
                pairs.append((src.name, dest.name))
        return pairs

    # * start analytics section
    # * basics
    def vertex_count(self) -> int:
        """Counts the total number of Nodes in the graph.

        Returns:
            int: Number of Nodes in the graph.
        """
        return len(self.edges)

    def edge_count(self) -> int:
        """Counts all the edges in the graph.  Duplicates are counted.

        Returns:
            int: Number of edges/connections in the graph.
        """
        return sum(len(self.children(node)) for node in self.edges)

    def vertex_degree(self, vertex: Union[Node, None] = None) -> Union[int, list[int]]:
        """Calculates the number of Nodes connected to the target vertex.

        If no target vertex provided, calculates connected Nodes for each Node in the
        graph.

        Args:
            vertex (Union[Node, None], optional): Target vertex to search for. Defaults to None.

        Returns:
            Union[int, list[int]]: Either the degree of the target vertex or a list of the degrees of all the nodes.
        """
        if vertex:
            return len(self.children(vertex))
        return sorted([len(self.children(n)) for n in self.edges])

    # * advanced
    def edge_rank(
        self, vertex: Union[Node, None] = None, limit: Union[int, None] = None
    ) -> list[tuple[tuple[str, str], int]]:
        """Ranks the edges based on their weight.

        Ranks are calculated either for the entire graph (default) or for
        the specified Node.

        Args:
            vertex (Union[Node, None], optional): Node to run calculation on. Defaults to None.
            limit (Union[int, None], optional): Limit for the number of edges returned. Defaults to None.

        Returns:
            list[tuple[tuple[str, str], int]]: Returns a sorted (by weight) list of edges up to the limit parameter.
        """
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
    """Undirected sub-class of the Digraph."""
    def add_edge(self, edge: Edge):
        """Adds both (directed) edges to the graph."""
        Digraph.add_edge(self, edge)
        rev = Edge(edge.dest, edge.src)
        Digraph.add_edge(self, rev)
