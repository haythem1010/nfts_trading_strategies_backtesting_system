from pprint import pprint

import dash
from dash import Input, Output, dcc, html, ctx, State
import plotly.express as px
import dash_bootstrap_components as dbc
from strategies.bollinger_band.signals import Backtesting
from strategies.bollinger_band.plotter import plot_the_strategy
from importers.collections_importers import CollectionsByAPI
from strategies.buy_the_floor.buy_the_floor import BuyTheFloor
from strategies.buy_the_floor.plotter import plot_data

col = CollectionsByAPI().get_available_collections()
graf = Backtesting()
btf_s = BuyTheFloor()

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = dash.Dash(__name__, prevent_initial_callbacks=True, external_stylesheets=[dbc.themes.BOOTSTRAP,dbc_css],suppress_callback_exceptions=True)

buttons = dbc.ButtonGroup(
        children=[
        dbc.Button("Bollinger Band Strategy", id="btn-bb", color="light", outline=False, className="btn_1",style={'align': 'center', 'color': '#181812','font-size':'10', 'weight':'70px', 'height':'35px'}),
        dbc.Button("Buy the floor Strategy", id="btn-btf", color="light", outline=False, className="btn_1",style={'align': 'center', 'color': '#181812','font-size':'16',  'weight':'70px', 'height':'35px'}),
        dbc.Button("Strategy 3 ", id="btn-area", color="light", outline=False, className="btn_1", style={'align': 'center', 'color': '#181812','font-size':'16'}),
    ],
    className="d-grid gap-2",
)
date_filter = html.Nav(
    children=[
    dbc.Button("7d", id="d7_filter", color='light', outline=True, className="btn_filters", style={'color': '#7F1B93', 'text-align': 'center','border-radius': '50%','font-size':'10px', 'weight':'25px', 'height':'25px'}),
    dbc.Button("1M", id="M1_filter", color='light', outline=True, className="btn_filters", style={'color': '#7F1B93', 'text-align': 'center','border-radius': '50%','font-size':'10px', 'weight':'25px', 'height':'25px'}),
    dbc.Button("3M", id="M3_filter", color='light', outline=True, className="btn_filters", style={'color': '#7F1B93', 'text-align': 'center','border-radius': '50%','font-size':'10px', 'weight':'25px', 'height':'25px'}),
    dbc.Button("6M", id="M6_filter", color='light', outline=True, className="btn_filters", style={'color': '#7F1B93', 'text-align': 'center','border-radius': '50%','font-size':'10px', 'weight':'25px', 'height':'25px'}),
    dbc.Button("ALL", id="ALL_filter", color='light', outline=True, className="btn_filters", style={'color': '#7F1B93', 'text-align': 'center','border-radius': '50%','font-size':'10px', 'weight':'25px', 'height':'25px'}),
    ],
    className="filters-by-time"
)

collection_filter = dcc.RadioItems(
    options=[i for i in col],
    value='DGOD',
    inline=False,
    id='radio_collection',
    style={'text-align': 'left', 'font-size':'14px','color': '#7F1B93'}

)

slider = dcc.Slider(
    id='slider_windows',
    min=3,
    max=21,
    step=1,
    marks={i : str(i) for i in range(3, 22, 3)},
)

tabs = dcc.Tabs(id='tabs',value='tab1',children=[
    buttons
]
)

app.layout = dbc.Container(
    [
        html.H1("NFTs Trading Strategies", style={'align': 'center', 'color': '#FFFFFF'}),
        html.Hr(),
        dbc.Row([
            dbc.Col([collection_filter], width=2),
            dbc.Col([
                dbc.Row([date_filter]),
                dbc.Row([dcc.Graph(id="custom", config={'displayModeBar': False})]),
            ], md=8),
            dbc.Col([
                dbc.Row([html.Label('Indicators', style={'color':'#FFFFFF'})]),
                dbc.Row(html.Hr()),
                dbc.Row([buttons]),
            ]),
        ], align='center'),
        dbc.Row([slider])
    ], style={'background-color': '#0F035D', 'width': '2240px', 'height': '920px'}
)


# @app.callback(
#     Output('custom', component_property='figure'),
#     Input('btn-bb', component_property='n_clicks'),
#     Input('btn-btf', component_property='n_clicks'),
#     Input('radio_collection', component_property='value')
# )
#
# def get_period_of_data():
#     clicked_button = ctx.triggered_id if ctx.triggered_id else "ALL_filer"
#     if clicked_button == 'd7_filter':
#         return 7
#     elif clicked_button == 'M1_filter':
#         return 30
#     elif clicked_button == 'M3_filter':
#         return 90
#     elif clicked_button == 'M6_filter':
#         return 120
#     else:
#         return 0


@app.callback(
    Output('custom', 'figure'),
    Input('btn-btf', 'n_clicks'),
    Input('btn-bb', 'n_clicks'),
    Input('radio_collection', 'value'),
    prevent_initial_call=True
)
def update_figure(btn_btf, btn_bb, radio_collection_v):
    ctx = dash.callback_context

    if not ctx.triggered:
        button_id = None
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'btn-btf' and btn_btf is not None:
        trading_data, trades = btf_s.buy_sell(collection=radio_collection_v, period=1, days=5)
        pprint(trading_data)
        fig = plot_data(trading_data, plotted=True)
    elif button_id == 'btn-bb' and btn_bb is not None:
        trades, data = graf.backtest_bollinger_band(collection=radio_collection_v, period=1, window=7)
        fig = plot_the_strategy(data, plotted=True)
    else:
        fig = {}

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)