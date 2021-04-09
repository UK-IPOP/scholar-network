"""
This package is intended for people wanting to scrape Google Scholar
to build graph networks of Google Scholar authors and identify network
connections as opportunities for collaboration.
"""
__version__ = "0.1.8"

from .helpers import build_graph
from .models import CustomCounter, Graph, Digraph, Edge, Node
from .scraping import scrape_single_author
