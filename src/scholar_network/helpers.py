from . import models
import json


ENCODING = "utf-8-sig"

# TODO: add functionality to compare authors/coauthor list and check
# string similarity to avoid duplicate authors
# --> probably build the name standardization package and use here


def load_scholars():
    with open("data/scraped.json", "r", encoding=ENCODING) as f:
        scholars = json.load(f)
    return scholars


def build_graph() -> models.Graph:
    scholars = load_scholars()
    graph = models.Graph()
    for name in scholars.keys():
        for pub in scholars[name]:
            co_authors = [c.strip() for c in pub.get("authors").split(",")]
            # TODO: add support for journal title as attribute of edge
            # TODO: want weight to track number of connections on each edge
            # TODO: look at speed enhancements
            # journal = scholars[name].get("journal_title").strip()
            for co in co_authors:
                graph.add_node(models.Node(co))
                for other in co_authors:
                    if other == co:
                        continue
                    graph.add_node(models.Node(other))
                    graph.add_edge(
                        models.Edge(graph.get_node(co), graph.get_node(other))
                    )
    return graph
