from dash import Input, Output, dcc, html, ctx, Dash, dash
import plotly.express as px
import dash_bootstrap_components as dbc
from importers.collections_importers import CollectionsByAPI
from dash import html, register_page , callback

col = CollectionsByAPI().get_available_collections(local_data=True)

buttons = dbc.ButtonGroup(
        children=[
        dbc.Button("Bollinger Band Strategy", id="btn-bb", color="light", outline=False, className="btn_1",style={'align': 'center', 'color': '#181812','font-size':'10', 'weight':'70px', 'height':'35px'}),
        dbc.Button("Buy the floor Strategy", id="btn-btf", color="light", outline=False, className="btn_1",style={'align': 'center', 'color': '#181812','font-size':'16',  'weight':'70px', 'height':'35px'}),
        dbc.Button("Strategy 3 ", id="btn-area", color="light", outline=False, className="btn_1", style={'align': 'center', 'color': '#181812','font-size':'16'}),
    ],
    className="d-grid gap-2",
)


slider = dcc.Slider(
    id='slider_windows',
    min=3,
    max=21,
    step=1,
    marks={i : str(i) for i in range(3, 22, 3)},
)

tabs = dcc.Tabs(id='tabs', value='tab1', children=[
    buttons
]
)


register_page(
    __name__,
    name='Strategies',
    top_nav=True,
    path='/Strategies.py'
)


layout = html.Div([
     html.H3([
             " Pattern Recognition "], style={'textAlign': 'center', 'margin-top': '20px'}),
     dbc.Row([
         dbc.Button("Bollinger Band ", href='/BollingerBand.py', outline=True, color='secondary',  style={'textAlign': 'center', 'color': '#614A8A', 'font-size': '12px', 'font-weight': 'bold', 'width': '300px','height': '50px','border-radius': '10%','margin-left': '5px'}),
         dbc.Button("Triple RSI", href='/triple_rsi.py', outline=True, color='secondary', style={'textAlign': 'center', 'color': '#614A8A', 'font-size': '12px', 'font-weight': 'bold', 'width': '300px','height': '50px','border-radius': '10%','margin-left': '5px'}),
         dbc.Button("Buy the Floor", href='/Buythefloor.py', outline=True, color='secondary', style={'textAlign': 'center', 'color': '#614A8A', 'font-size': '12px', 'font-weight': 'bold', 'width': '300px','height': '50px','border-radius': '10%','margin-left': '5px'}),
         dbc.Button("Moving Average Crossover", href='/movingaverage_crossover.py', outline=True, color='secondary', style={'textAlign': 'center', 'color': '#614A8A', 'font-size': '12px', 'font-weight': 'bold', 'width': '300px','height': '50px','border-radius': '10%','margin-left': '5px'}),
     ], justify='center', style={'padding': '10px'}),

 ])



#
# app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.CERULEAN], suppress_callback_exceptions=True)
# app.layout = dbc.Container(
#     [
#         html.H1("NFTs Trading Strategies Backtesting System", style={'align': 'center', 'color': '#614A8A'}),
#         html.Hr(),
#         dbc.Row([
#             dbc.Col([], md=8),
#             dbc.Col([
#                 dbc.Row([html.Label('Indicators', style={'color': '#614A8A'})]),
#                 dbc.Row(html.Hr()),
#             ]),
#         ], align='center'),
#         dbc.Row([
#             dbc.Col([
#                 dbc.Button(
#                     dcc.Link(
#                         f"{page['name']} ", href=page["relative_path"],
#                     ), outline=True, color='info'
#                 )
#                 for page in dash.page_registry.values()
#             ])
#         ]),
#         dash.page_container
#     ], style={'background-color': '#FFFFFF', 'width': '2240px', 'height': '920px'}
# )