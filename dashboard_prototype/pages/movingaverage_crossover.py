import pandas
from dash import html, register_page, callback
from dash import Input, Output, dcc, html, ctx, Dash, dash, callback_context
import dash_bootstrap_components as dbc
from importers.collections_importers import CollectionsByAPI
from strategies.moving_average_crossover.maco import MovingAverageCrossOver
from strategies.moving_average_crossover.plotter import plot_the_strategy
from dash.exceptions import PreventUpdate

col = CollectionsByAPI().get_available_collections(local_data=True)
cross = MovingAverageCrossOver()

register_page(
    __name__,
    name='Moving Average Crossover',
    top_nav=True,
    path='/movingaverage_crossover.py'
)

layout = html.Div([
    html.H2([
            " This page is for the strategy called Moving Average strategy : "
        ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H6(["Collection"]),
                dcc.Dropdown(
                    options=[i for i in col],
                    value=['AUROR'],
                    multi=False,
                    id="drop_collection",
                    style={'width': '200px', 'min-width': '150px'}),
            ], style={'justify': "center", 'align':"center"}),
        ], style={'align': 'center'}),
        dbc.Col([
            dbc.Row([
                html.H6(["Slow Moving Average"], style={'left-margin':'10px'}),
                dcc.Slider(min=0,
                            max=7,
                            step=1,
                            marks={i: str(i) for i in range(0, 8)},
                            value=7,
                            id='slow',
                            included=False,
                )]),
            dbc.Row([
                html.H6(["Fast Moving Average"], style={'left-margin':'10px'}),
                dcc.Slider(min=8,
                            max=15,
                            step=1,
                            marks={i: str(i) for i in range(8, 16)},
                            value=7,
                            id='fast',
                            included=False,
                       )]),
        ], style={'padding': '10px', 'align': 'center'}),
        dbc.Col([
            dbc.Button("Apply", id='apply', color="dark", outline=True, style={'weight': '70px', 'height':'45px'}),
            # dbc.Button("Clear", id='clear', color="dark", outline=True, style={'weight': '70px', 'height':'45px'})
        ], className="d-grid gap-2 d-md-flex justify-content-md-end")
    ], style={'padding': '10px'}),
    dbc.Row([

    ]),
    dbc.Row([

    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='graph'),
            dbc.Col([
                dbc.Tabs([
                    dbc.Tab(dbc.Table(id='maco_data_table'), label="Trades Simulation", style={'padding': '15px'}),
                    dbc.Tab(children=[
                        html.H5("The outcome of this strategy would be : "),
                        dbc.Row(html.Div(id='maco_output_number')),
                        html.H5("The number of transactions would be : "),
                        dbc.Row(html.Div(id='maco_trades'))
                    ], label='Outcome', style={'padding': '50px'}),
                ]),
            ])
        ])
    ])
])


@callback(
    [Output(component_id='graph', component_property='figure', allow_duplicate=True),
     Output(component_id='maco_data_table', component_property='children', allow_duplicate=True),
     Output(component_id='maco_output_number', component_property='children', allow_duplicate=True),
     Output(component_id='maco_trades', component_property='children', allow_duplicate=True)],
    Input(component_id='drop_collection', component_property='value'),
    Input(component_id="slow", component_property='value'),
    Input(component_id="fast", component_property='value'),
    Input(component_id="apply", component_property='n_clicks'),
    prevent_initial_call=True
)

def update_graph(collection_value, slow_value, fast_value, n_clicks):
    # triggered_id = ctx.triggered_id
    if n_clicks is None:
        raise PreventUpdate
    else:
        data, trades, profit = cross.build_the_strategy(collection_value, 1, slow_value, fast_value, 24)
        df_trades = pandas.DataFrame(trades)
        fig = plot_the_strategy(data)
        df_table = dbc.Table.from_dataframe(df_trades, striped=True, bordered=True, hover=True)
    return fig, df_table, profit, len(trades)