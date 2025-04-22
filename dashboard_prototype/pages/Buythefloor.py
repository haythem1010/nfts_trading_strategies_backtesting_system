from pprint import pprint
import pandas
from dash import Input, Output, dcc, html, ctx, Dash, dash, callback_context
import dash_bootstrap_components as dbc
from dash import html, register_page , callback
from importers.collections_importers import CollectionsByAPI
col = CollectionsByAPI().get_available_collections(local_data=True)
from dash.exceptions import PreventUpdate
from strategies.buy_the_floor.buy_the_floor import BuyTheFloor
from strategies.buy_the_floor.plotter import plot_data
import plotly.express as px
import plotly.graph_objects as go

register_page(
    __name__,
    name='Triple RSI',
    top_nav=True,
    path='/Buythefloor.py'
)



layout = html.Div([
    html.H2([" This page is for the strategy called 'Buy The Floor' : "
            ]),
    dbc.Row([
        dbc.Col([
            html.H6(["Collection"]),
            dcc.Dropdown(
                    options=[i for i in col],
                    value=['AUROR'],
                    multi=False,
                    id="drop_collection",
                    style={'width': '200px', 'min-width': '150px'}, ),
                ], style={'align': 'center'}),
        dbc.Col([
            html.H6(["Moving Average"], style={'left-margin': '10px'}),
            dcc.Slider(min=0,
                        max=15,
                        step=1,
                        marks={i: str(i) for i in range(0, 16)},
                        value=7,
                        id='btf',
                        included=False,
                        )
            ], style={'padding': '10px', 'align': 'center'}),
        dbc.Col([
                dbc.Button("Apply", id='apply', color="dark", outline=True, style={'weight': '70px', 'height': '45px'}),
                dbc.Button("Clear", id='clear', color="dark", outline=True, style={'weight': '70px', 'height': '45px'})
        ], className="d-grid gap-2 d-md-flex justify-content-md-end")
    ], style={'padding': '10px'}),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='graph'),
            dbc.Col([
                dbc.Tabs([
                    dbc.Tab(dbc.Table(id='btf_data_table'), label="Trades Simulation", style={'padding': '10px'}),
                    dbc.Tab(children=[
                        html.H5("The outcome of this strategy would be : "),
                        dbc.Row(html.Div(id='btf_output_number')),
                        html.H5("The number of transactions would be : "),
                        dbc.Row(html.Div(id='btf_trades'))
                    ], label='Outcome', style={'padding': '100px'}),
                ]),
            ])
        ])
    ])
])

@callback(
    [Output(component_id='graph', component_property='figure', allow_duplicate=True),
     Output(component_id='btf_data_table', component_property='children', allow_duplicate=True),
     Output(component_id='btf_output_number', component_property='children', allow_duplicate=True),
     Output(component_id='btf_trades', component_property='children', allow_duplicate=True)],
    Input(component_id='drop_collection', component_property='value'),
    Input(component_id="btf", component_property='value'),
    Input(component_id="apply", component_property='n_clicks'),
    prevent_initial_call=True
)

def update_graph(collection_value, window_value, n_clicks):
    # triggered_id = ctx.triggered_id
    if n_clicks is None:
        raise PreventUpdate
    else:
        bck = BuyTheFloor()
        df_trading, trades, profit, fig = bck.buy_sell(collection_value, 24, window_value, local_data=True)
        df_tr = pandas.DataFrame(trades)
        df_table = dbc.Table.from_dataframe(df_tr, striped=True, bordered=True, hover=True)
    return fig, df_table, profit, len(trades)
#
# def update_graph(collection_value, window_value, b1, b2):
#     triggered_id = ctx.triggered_id
#     print(triggered_id)
#     if triggered_id == 'clear':
#          return reset_graph()
#     elif triggered_id == 'apply':
#          return draw_graph(collection_value, window_value)
#
# def draw_graph(collection_value, window_value):
#     bck = BuyTheFloor()
#     trades, data, income = bck.buy_sell(collection_value, 24, window_value, local_data=True)
#     fig = plot_data(data)
#     return fig
#
# def reset_graph():
#     return go.Figure()
