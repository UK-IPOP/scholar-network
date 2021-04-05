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
    data.extend(publication_info)
    with open("data/scraped.json", "w", encoding=ENCODING) as f:
        json.dump(data, f, indent=4, sort_keys=True)


def build_graph(
    author1: Union[str, None] = None, author2: Union[str, None] = None
) -> models.Graph:
    # TODO: add support for journal title as attribute of edge
    # TODO: want weight to track number of connections on each edge
    # TODO: look at speed enhancements
    # journal = scholars[name].get("journal_title").strip()

    publications = load_publications()
    graph = models.Graph()
    if not author1 and not author2:  # make whole graph
        for pub in publications:
            co_authors = set([c.strip() for c in pub.get("authors").split(",")])

            for first in co_authors:
                n1 = models.Node(first)
                graph.add_node(n1)
                for second in co_authors:
                    if second == first:
                        continue
                    n2 = models.Node(second)
                    graph.add_node(n2)
                    graph.add_edge(
                        models.Edge(n1, n2)
                    )
        return graph
    else:  # otherwise at least one author passed
        for pub in publications:
            co_authors = set([c.strip() for c in pub.get("authors").split(",")])
            # if author in coauthors set then add that network
            if author1 in co_authors or author2 in co_authors:
                for first in co_authors:
                    n1 = models.Node(first)
                    graph.add_node(n1)
                    for second in co_authors:
                        if second == first:
                            continue
                        n2 = models.Node(second)
                        graph.add_node(second)
                        graph.add_edge(
                            models.Edge(n1, n2)
                        )
        return graph
