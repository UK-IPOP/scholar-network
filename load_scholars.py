
import jmespath
import networkx as nx
import pandas as pd
from rich.progress import track
from scholarly import scholarly
import plotly.graph_objects as go


def load() -> pd.DataFrame:
    """Loads COP scholar dataframe.

    Returns:
        df: pandas dataframe for scholars
    """
    df = pd.read_csv("data/COPscholars.csv")
    return df


def search_network(author: str) -> set[tuple[str, str]]:
    search = scholarly.search_author(author)
    results = scholarly.fill(next(search))
    coauthors = jmespath.search("coauthors[*].name", results)
    connections = set([(author, coauthor) for coauthor in coauthors])  # one depth
    for lvl2_author in track(coauthors, total=len(coauthors)):  # second depth
        lvl_2_search = scholarly.search_author(lvl2_author)
        try:
            lvl2_results = scholarly.fill(next(lvl_2_search))
        except StopIteration:
            continue
        lvl2_coauthors = jmespath.search("coauthors[*].name", lvl2_results)
        for a in lvl2_coauthors:
            connections.add((lvl2_author, a))
    return connections


def build_network(connections: list[tuple[str, str]]) -> tuple[go.Scatter, go.Scatter]:
    G = nx.Graph()
    G.add_edges_from(connections)

    edge_x = []
    edge_y = []
    positions = nx.kamada_kawai_layout(G)
    for edge in G.edges():
        x0, y0 = positions[edge[0]]
        x1, y1 = positions[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    node_name = []
    for node in G.nodes():
        x, y = positions[node]
        node_x.append(x)
        node_y.append(y)
        node_name.append(node)

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append(f'# of connections: {str(len(adjacencies[1]))}')

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        hovertext=node_name,
        customdata=node_text,
        hovertemplate='%{hovertext}<br>%{customdata}<extra></extra>',
        marker=dict(
            showscale=True,
            # colorscale options
            # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    node_trace.marker.color = node_adjacencies

    return node_trace, edge_trace


def draw_network(edge_trace: go.Scatter, node_trace: go.Scatter) -> go.Figure:
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Network graph made with Python',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        annotations=[dict(
                            showarrow=True,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002)],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    return fig
