import json
from typing import Union

from . import models

ENCODING = "utf-8-sig"


def load_publications():
    with open("data/scraped.json", "r", encoding=ENCODING) as f:
        scholars = json.load(f)
    return scholars


def append_pub_data_to_json(publication_info: list[dict[str, str]]):
    with open("data/scraped.json", "r", encoding=ENCODING) as f:
        data = json.load(f)
    data.append(publication_info)
    with open("data/scraped.json", "w", encoding=ENCODING) as f:
        json.dump(data, f, indent=4, sort_keys=True)


def build_graph(
    author1: Union[str, None] = None, author2: Union[str, None] = None
) -> models.Graph:
    publications = load_publications()
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
