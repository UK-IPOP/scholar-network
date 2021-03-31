from typing import Union
from . import models
import json
import networkx as nx
import pickle

ENCODING = "utf-8-sig"

# TODO: add functionality to compare authors/coauthor list and check
# string similarity to avoid duplicate authors
# --> probably build the name standardization package and use here


def load_scholars_json():
    with open("data/flattened-scraped.json", "r", encoding=ENCODING) as f:
        scholars = json.load(f)
    return scholars


def build_graph(
    author1: Union[str, None] = None, author2: Union[str, None] = None
) -> models.Graph:
    publications = load_scholars_json()
    graph = models.Graph()
    for pub in publications:
        co_authors = set([c.strip() for c in pub.get("authors").split(",")])

        if not author1 and not author2:  # make whole graph
            for co in co_authors:
                graph.add_node(models.Node(co))
                for other in co_authors:
                    graph.add_node(models.Node(co))
                    for other in co_authors:
                        if other == co:
                            continue
                        graph.add_node(models.Node(other))
                        graph.add_edge(
                            models.Edge(graph.get_node(co), graph.get_node(other))
                        )

        # otherwise at least one author passed
        # if author in coauthors set then add that network
        if author1 in co_authors or author2 in co_authors:
            for co in co_authors:
                graph.add_node(models.Node(co))
                for other in co_authors:
                    graph.add_node(models.Node(co))
                    for other in co_authors:
                        if other == co:
                            continue
                        graph.add_node(models.Node(other))
                        graph.add_edge(
                            models.Edge(graph.get_node(co), graph.get_node(other))
                        )

        # TODO: add support for journal title as attribute of edge
        # TODO: want weight to track number of connections on each edge
        # TODO: look at speed enhancements
        # journal = scholars[name].get("journal_title").strip()

    return graph


def save_graph(connections: list[tuple[str, str]]):
    G = nx.Graph()
    G.add_edges_from(connections)
    positions = nx.spring_layout(G)
    with open("data/COP-graph.pkl", "wb") as f:
        pickle.dump(G, f)
    with open("data/COP-graph-positions.pkl", "wb") as f:
        pickle.dump(positions, f)
    return


def load_graph_from_files() -> tuple[nx.Graph, nx.layout.spring_layout]:
    with open("data/COP-graph.pkl", "rb") as f:
        g = pickle.load(f)
    with open("data/COP-graph-positions.pkl", "rb") as f:
        positions = pickle.load(f)
    return g, positions