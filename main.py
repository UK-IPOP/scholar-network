import time

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import load_scholars

scholars_df = load_scholars.load()


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
                {"label": person, "value": person} for person in scholars_df.Name.values
            ],
            value=scholars_df.Name.values[0]
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


# @app.callback(Output("loading-graph", "children"), Input("author-dropdown", "value"))
# def input_triggers_spinner(value):
#     time.sleep(1)
#     return value


@app.callback(
    Output(component_id="selected-author", component_property="children"),
    Input(component_id="author-dropdown", component_property="value"),
)
def update_output_div(input_value: str) -> str:
    return "Output: {}".format(input_value)


@app.callback(
    Output(component_id='network-graph', component_property='figure'),
    Input(component_id="author-dropdown", component_property="value"),
)
def update_graph(input_value: str) -> go.Figure:
    connections = load_scholars.search_network(input_value)
    network = load_scholars.build_network(connections)
    graph = load_scholars.draw_network(*network)
    return graph


if __name__ == "__main__":
    app.run_server(debug=True)
