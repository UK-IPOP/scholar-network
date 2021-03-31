import pickle
from typing import Container, Union

import dash
from dash_bootstrap_components._components.Card import Card
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd
import networkx as nx
import csv
import dash_bootstrap_components as dbc


from scholar_network import graphing, helpers


# TODO: performance improvements
# * only build graph with needed nodes when building pair-graph


def load_scholar_names() -> list[str]:
    with open("data/COPscholars.csv", "r") as f:
        csvreader = csv.DictReader(f)
        authors = []
        for row in csvreader:
            authors.append(row.get("Name"))
    return authors


scholar_names = load_scholar_names()

theme = "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/sketchy/bootstrap.min.css"
app = dash.Dash(__name__, external_stylesheets=[theme])
server = app.server


def create_cop_network_graph_figure():
    G, positions = helpers.load_graph_from_files()
    node_trace, edge_trace = graphing.build_network(G, positions)
    fig = graphing.draw_network(node_trace, edge_trace, title="COP Network Graph")
    return fig


def pair_graph(author1, author2):
    graph = helpers.build_graph(author1, author2)
    G = nx.Graph()
    G.add_edges_from(graph.node_pairs())
    positions = nx.spring_layout(G)
    node_trace, edge_trace = graphing.build_network(G, positions)
    title = f""
    fig = graphing.draw_network(
        node_trace,
        edge_trace,
        title=f"{author1.title() if author1 else '...'} x {author2.title() if author2 else '...'} Network Graph",
    )
    return fig


cop_network_graph = create_cop_network_graph_figure()


app.layout = dbc.Container(
    [
        html.Center(html.H1(children="UK COP Network Web App", className="pt-3")),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Author 1 Select:"),
                        dcc.Dropdown(
                            id="author-dropdown1",
                            options=[
                                {"label": person, "value": person}
                                for person in scholar_names
                            ],
                            value="",
                        ),
                    ],
                    width=4,
                ),
                dbc.Col(
                    [
                        html.Label("Author 2 Select:"),
                        dcc.Dropdown(
                            id="author-dropdown2",
                            options=[
                                {"label": person, "value": person}
                                for person in scholar_names
                            ],
                            value="",
                        ),
                    ],
                    width=4,
                ),
            ],
            className="py-5",
            justify="center",
            align="center",
        ),
        dbc.Row(
            [
                dbc.Card(
                    dbc.Spinner(
                        dcc.Graph(id="network-graph"),
                        type="grow",
                        color="info",
                        size="lg",
                    ),
                    body=True,
                )
            ],
            justify="center",
            align="center",
        ),
    ]
)


@app.callback(
    Output(component_id="author-dropdown2", component_property="options"),
    Input(component_id="author-dropdown1", component_property="value"),
)
def update_options1(input_value: str) -> list[dict[str, str]]:
    return [
        {"label": person, "value": person}
        for person in scholar_names
        if person != input_value
    ]


@app.callback(
    Output(component_id="author-dropdown1", component_property="options"),
    Input(component_id="author-dropdown2", component_property="value"),
)
def update_options2(input_value: str) -> list[dict[str, str]]:
    return [
        {"label": person, "value": person}
        for person in scholar_names
        if person != input_value
    ]


@app.callback(
    Output("network-graph", "figure"),
    [
        Input(component_id="author-dropdown1", component_property="value"),
        Input(component_id="author-dropdown2", component_property="value"),
    ],
)
def on_author_select(author1: Union[str, None], author2: Union[str, None]) -> go.Figure:
    if author1 or author2:
        return pair_graph(author1, author2)
    return cop_network_graph


if __name__ == "__main__":
    app.run_server(debug=True)
