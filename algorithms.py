"""The remainder of this is probably accessory."""


from typing import Union
from models import Digraph, Graph, Node, Edge


def build_city_graph(graph_type: Union[Digraph, Graph]):
    g = graph_type()
    for name in (
        "Boston",
        "Providence",
        "New York",
        "Chicago",
        "Denver",
        "Phoenix",
        "Los Angeles",
    ):
        g.add_node(Node(name))
    g.add_edge(Edge(g.get_node("Boston"), g.get_node("Providence")))
    g.add_edge(Edge(g.get_node("Boston"), g.get_node("New York")))
    g.add_edge(Edge(g.get_node("Providence"), g.get_node("Boston")))
    g.add_edge(Edge(g.get_node("Providence"), g.get_node("New York")))
    g.add_edge(Edge(g.get_node("New York"), g.get_node("Chicago")))
    g.add_edge(Edge(g.get_node("Chicago"), g.get_node("Denver")))
    g.add_edge(Edge(g.get_node("Chicago"), g.get_node("Phoenix")))
    g.add_edge(Edge(g.get_node("Denver"), g.get_node("Phoenix")))
    g.add_edge(Edge(g.get_node("Denver"), g.get_node("New York")))
    g.add_edge(Edge(g.get_node("Los Angeles"), g.get_node("Boston")))
    return g


def depth_fist_search(
    graph: Union[Digraph, Graph], start: Node, end: Node, path, shortest, to_print=False
):
    path = path + [start]
    if to_print:
        print(f"Current DFS path: {[p.name for p in path]}")
    if start == end:
        return path
    for node in graph.children(start):
        if node not in path:
            if shortest == None or len(path) < len(shortest):
                new_path = depth_fist_search(graph, node, end, path, shortest, to_print)
                if new_path != None:
                    shortest = new_path
        elif to_print:
            print("Already visited node.")
    return shortest


def breadth_fist_search(
    graph: Union[Digraph, Graph], start: Node, end: Node, to_print=False
):
    initial_path = [start]
    path_queue = [initial_path]
    while len(path_queue) != 0:
        # get and remove oldest element in path_queue
        temp_path = path_queue.pop(0)
        if to_print:
            print(f"Current BFS path {[p.name for p in temp_path]}")
        last_node = temp_path[-1]
        if last_node == end:
            return temp_path
        for next_node in graph.children(last_node):
            if next_node not in temp_path:
                new_path = temp_path + [next_node]
                path_queue.append(new_path)
    return None
