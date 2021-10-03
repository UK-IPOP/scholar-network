"""This module contains helper functions for building the network
and storing data.
"""

import json
from typing import Union
import itertools

from . import models

ENCODING = "utf-8-sig"


def parse_name(name: str) -> str:
    """Extracts first and last parts of a name.

    This could be first and last name or any variation.

    Args:
        name (str): String name to be parsed

    Returns:
        str: Extracted 2-part name.
    """
    parts = name.split()
    parsed = f"{parts[0][0]} {parts[-1]}"
    return parsed


def load_publications(fpath: str = "data/scraped.json") -> list[dict[str, str]]:
    """Utility function to load publication data.

    Returns:
        (list[dict[str, str]]): List of publication data.
    """
    with open(fpath, "r", encoding=ENCODING) as f:
        scholars = json.load(f)
    return scholars


def append_pub_data_to_json(publication_info: list[dict[str, str]]):
    """Saves publication data from
    [get_publication_data][src.scholar_network.scraping.get_publication_data]
    to data/scraped.json file.

    Args:
        publication_info (list[dict[str, str]]): Publication data.
    """
    with open("data/scraped.json", "r", encoding=ENCODING) as f:
        data = json.load(f)
    data.extend(publication_info)
    with open("data/scraped.json", "w", encoding=ENCODING) as f:
        json.dump(data, f, indent=4, sort_keys=True)


def build_graph(
    author1: Union[str, None] = None,
    author2: Union[str, None] = None,
    fpath: str = "data/scraped.json",
) -> models.Graph:
    """This utility function builds the Graph for the network.

    Currently the default graph type that is built is undirected.

    If no authors are provided, then a network of all the data contained in
    `data/scraped.json` will be built.

    If one or two authors are provided, only their networks will be built.

    Args:
        author1 (Union[str, None], optional): Author name. Defaults to None.
        author2 (Union[str, None], optional): Author name. Defaults to None.

    Returns:
        models.Graph: Network graph of authors.
    """
    # TODO: add support for journal title as attribute of edge
    # TODO: want weight to track number of connections on each edge
    # TODO: look at speed enhancements
    # journal = scholars[name].get("journal_title").strip()

    publications = load_publications(fpath=fpath)
    graph = models.Graph()
    a1 = parse_name(author1) if author1 else None
    a2 = parse_name(author2) if author2 else None
    if not author1 and not author2:  # make whole graph
        for pub in publications:
            co_authors = set(
                [parse_name(c.strip()) for c in pub.get("authors", "").split(",")]
            )
            pairs = itertools.combinations(co_authors, 2)
            for pair in pairs:
                n1 = models.Node(pair[0])
                graph.add_node(n1)
                n2 = models.Node(pair[1])
                graph.add_node(n2)
                graph.add_edge(models.Edge(n1, n2))
        return graph
    else:  # otherwise at least one author passed
        for pub in publications:
            co_authors = set(
                [parse_name(c.strip()) for c in pub.get("authors", "").split(",")]
            )
            # if author in coauthors set then add that network
            if a1 in co_authors or a2 in co_authors:
                pairs = itertools.combinations(co_authors, 2)
                for pair in pairs:
                    n1 = models.Node(pair[0])
                    graph.add_node(n1)
                    n2 = models.Node(pair[1])
                    graph.add_node(n2)
                    graph.add_edge(models.Edge(n1, n2))
        return graph
