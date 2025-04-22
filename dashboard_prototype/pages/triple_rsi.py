from pprint import pprint
import pandas
from dash import Input, Output, dcc, html, ctx, Dash, dash, callback_context
import dash_bootstrap_components as dbc
from dash import html, register_page , callback
from importers.collections_importers import CollectionsByAPI
col = CollectionsByAPI().get_available_collections(local_data=True)
from strategies.triple_rsi.triple_rsi import TripleRSI
from strategies.triple_rsi.plotter import plot_the_strategy
from dash.exceptions import PreventUpdate




register_page(
    __name__,
    name='Triple RSI',
    top_nav=True,
    path='/triple_rsi.py'
)


layout = html.Div([
    html.H2([
            " This page is for the strategy called ' Triple RSI [ Relative Strength Index ] ' : "
        ]),
    dbc.Row([
        dbc.Col([
            html.H6(["Collection"]),
            dcc.Dropdown(
                    options=[i for i in col],
                    value=['AUROR'],
                    multi=False,
                    id="drop_collection",
                    style={'width': '200px', 'min-width': '150px'},),
        ], style={'align':'center'}),
        dbc.Col([
            html.H6(["Short Term RSI"], style={'left-margin':'10px'}),
            dcc.Slider(min=0,
                       max=7,
                       step=1,
                       marks={i: str(i) for i in range(0, 8)},
                       value=1,
                       id='short',
                       included=False,
                       )
        ], style={'padding': '10px', 'align': 'center'}),
        dbc.Col([
            html.H6(["Mid-Term RSI "], style={'left-margin':'10px'}),
            dcc.Slider(min=8,
                       max=14,
                       step=1,
                       marks={i: str(i) for i in range(8, 15)},
                       value=9,
                       id='mid',
                       included=False,
                       )
        ], style={'padding': '10px', 'align': 'center'}),
        dbc.Col([
            html.H6(["Long Term RSI "], style={'left-margin':'10px'}),
            dcc.Slider(min=15,
                       max=21,
                       step=1,
                       marks={i: str(i) for i in range(15, 22)},
                       value=15,
                       id='long',
                       included=False,
                       )
        ], style={'padding': '10px', 'align': 'center'}),
        dbc.Col([
            dbc.Button("Apply", id='apply', color="dark", outline=True, style={'weight': '70px', 'height':'45px'}),
            dbc.Button("Clear", id='clear', color="dark", outline=True, style={'weight': '70px', 'height':'45px'})
        ], className="d-grid gap-2 d-md-flex justify-content-md-end")
    ], style={'padding': '10px'}),
    dbc.Row([

    ]),
    dbc.Row([

    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='graph'),
            dbc.Tabs([
                dbc.Tab(dbc.Table(id='trsi_data_table'), label="Trades Simulation"),
                dbc.Tab(children=[
                    html.H5("The outcome of this strategy would be : "),
                    dbc.Row(html.Div(id='trsi_output_number')),
                    html.H5("The number of transactions would be : "),
                    dbc.Row(html.Div(id='trsi_trades'))
                ], label='Outcome', style={'padding': '20px'}),
            ]),
        ])
    ])
])
#
@callback(
    [Output(component_id='graph', component_property='figure', allow_duplicate=True),
     Output(component_id='trsi_data_table', component_property='children', allow_duplicate=True),
     Output(component_id='trsi_output_number', component_property='children', allow_duplicate=True),
     Output(component_id='trsi_trades', component_property='children', allow_duplicate=True)],
    Input(component_id='drop_collection', component_property='value'),
    Input(component_id="short", component_property='value'),
    Input(component_id="mid", component_property='value'),
    Input(component_id="long", component_property='value'),
    Input(component_id="apply", component_property='n_clicks'),
    prevent_initial_call=True
)

def update_graph(collection_value, shortv, midv, longv, n_clicks):
    # triggered_id = ctx.triggered_id
    if n_clicks is None:
        raise PreventUpdate
    else:
        rsi = TripleRSI()
        triple_rsi, trades, profit = rsi.triple_rsi(collection=collection_value, days=1, slow=longv, mid=midv, fast=shortv, timeframe=24)
        fig = plot_the_strategy(triple_rsi)
        df_tr = pandas.DataFrame(trades)
        df_table = dbc.Table.from_dataframe(df_tr, striped=True, bordered=True, hover=True)
        # print("------", type(df_tr), len(df_tr),'------')
        # pprint(df_tr)
        # print("FFFRGRG", len(trades))
    return fig, df_table, profit, len(trades)
