import pickle

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd


from scholar_network import graphing, helpers

# TODO: make section to select two authors and make their networks
# to see if they have connections at layer level 1
# ? expand to more depth then?
# ? how to visualize with authors at sides?


def load_data() -> pd.DataFrame:
    return pd.read_csv("data/COPscholars.csv")


scholars_df = load_data()


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

fig = px.bar(
    scholars_df,
    x="Name",
    y="Citations",
    color="Group",
    barmode="group",
    title="Scholar Counts",
    height=600,
)


app.layout = html.Div(
    children=[
        html.H1(children="Hello Dash"),
        dcc.Dropdown(
            id="author-dropdown",
            options=[
                {"label": person, "value": person}
                for person in scholars_df.Name.values[:16]
            ],
            value=scholars_df.Name.values[0],
        ),
        dcc.Dropdown(
            id="depth-selector",
            options=[{"label": val, "value": val} for val in range(5)],
            value=1,
        ),
        html.Div(id="selected-author"),
        # dcc.Loading(
        #     id="loading-graph",
        #     type="circle",
        #     children=dcc.Graph(id="network-graph", figure=fig)
        # ),
        dcc.Graph(id="network-graph", figure=fig),
    ]
)


@app.callback(
    Output(component_id="selected-author", component_property="children"),
    Input(component_id="author-dropdown", component_property="value"),
)
def update_output_div(input_value: str) -> str:
    return "Output: {}".format(input_value)


@app.callback(
    Output(component_id="network-graph", component_property="figure"),
    [
        Input(component_id="author-dropdown", component_property="value"),
        Input(component_id="depth-selector", component_property="value"),
    ],
)
def update_graph(input_value: str, selected_depth: int) -> go.Figure:
    scholar_graph = helpers.build_graph()
    connections = scholar_graph.node_pairs()
    print(input_value)
    print(any(input_value in conn for conn in connections))
    print(f"depth: {selected_depth}")
    filtered_connections = graphing.filter_connections(
        root=input_value, connections=connections, depth=selected_depth
    )
    if len(filtered_connections) == 0:
        return go.Figure()  # empty figure
    print(len(filtered_connections))
    network = graphing.build_network(list(filtered_connections))
    graph = graphing.draw_network(*network)
    return graph


if __name__ == "__main__":
    app.run_server(debug=True)
