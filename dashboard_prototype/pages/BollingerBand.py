from pprint import pprint
import pandas
from dash import Input, Output, dcc, html, ctx, Dash, dash, callback_context
import dash_bootstrap_components as dbc
from dash import html, register_page , callback
from importers.collections_importers import CollectionsByAPI
col = CollectionsByAPI().get_available_collections(local_data=True)
from strategies.bollinger_band.signals import Backtesting
from strategies.bollinger_band.plotter import plot_the_strategy
from dash.exceptions import PreventUpdate

register_page(
    __name__,
    name='Bollinger Band',
    top_nav=True,
    path='/BollingerBand.py',
)



layout = html.Div([
    html.H2([
            " This page is for the strategy called Bollinger band strategy : "
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
            html.H6(["Moving Average"], style={'left-margin':'10px'}),
            dcc.Slider(min=0,
                       max=15,
                       step=1,
                       marks={i: str(i) for i in range(0, 16)},
                       value=7,
                       id='slider',
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
                dbc.Tab(dbc.Table(id='bb_data_table'), label="Trades Simulation"),
                dbc.Tab(children=[
                    html.H5("The outcome of this strategy would be : "),
                    dbc.Row(html.Div(id='bb_output_number')),
                    html.H5("The number of transactions would be : "),
                    dbc.Row(html.Div(id='bb_trades'))
                ], label='Outcome', style={'padding': '50px'}),
            ]),
        ])
    ])
])

@callback(
    [Output(component_id='graph', component_property='figure', allow_duplicate=True),
     Output(component_id='bb_data_table', component_property='children', allow_duplicate=True),
     Output(component_id='bb_output_number', component_property='children', allow_duplicate=True),
     Output(component_id='bb_trades', component_property='children', allow_duplicate=True)],
    Input(component_id='drop_collection', component_property='value'),
    Input(component_id="slider", component_property='value'),
    Input(component_id="apply", component_property='n_clicks'),
    prevent_initial_call=True
)

def update_graph(collection_value, window_value, n_clicks):
    # triggered_id = ctx.triggered_id
    if n_clicks is None:
        raise PreventUpdate
    else:
        bck = Backtesting()
        trades, data, outcome = bck.backtest_bollinger_band(collection_value, window_value, 24)
        fig = plot_the_strategy(data)
        df_tr = pandas.DataFrame(trades)
        df_table = dbc.Table.from_dataframe(df_tr, striped=True, bordered=True, hover=True)
    return fig, df_table, outcome, len(trades)


