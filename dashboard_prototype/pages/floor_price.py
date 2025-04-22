from dash import html, register_page, callback, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from importers.collections_importers import CollectionsByAPI
from dash.exceptions import PreventUpdate
from models.times_series.arimax_model import Mymodel


mdl = Mymodel()
col = CollectionsByAPI().get_available_collections(local_data=True)

register_page(
    __name__,
    name='Floor Price Predictions',
    top_nav=True,
    path='/floor_price.py'
)



layout = html.Div([
    html.H3(
            " Forcasting reliable values to gain insights  ",  style={'textAlign': 'center'}
        ),
    dbc.Row([
         dbc.Button('Floor Price', outline=True, color='secondary', href='/floor_price.py', style={'textAlign': 'center', 'color': '#614A8A', 'font-size': '12px', 'font-weight': 'bold', 'width': '250px','height': '50px','border-radius': '10%','margin-left': '5px'}),
         dbc.Button("Average Trading Price", outline=True, color='secondary', href='/average_trading_price.py', style={'textAlign': 'center', 'color': '#614A8A', 'font-size': '12px', 'font-weight': 'bold', 'width': '250px','height': '50px','border-radius': '10%','margin-left': '5px'}),
     ], justify='center', style={'padding': '20px'}),
    dbc.Row([
        dbc.Col([
            html.H6(["Collection"]),
            dcc.Dropdown(
                options=[i for i in col],
                value=['AUROR'],
                multi=False,
                id="drop_collection_tr_avg_price",
                style={'width': '200px', 'min-width': '150px'}, ),
        ], style={'align': 'center','display': 'flex', 'justify-content': 'flex-end'}),
        dbc.Col([
            dbc.Button("Apply", id='apply_tr_avg_price', color="dark", outline=True, style={'weight': '70px', 'height': '45px'}),
        ])
    ], style={'padding': '10 px'}),
    dbc.Row([
        dcc.Graph(id='floor_price_pred')
    ])
    ], style={'padding': '20px'})

@callback(
    Output(component_id='floor_price_pred', component_property='figure', allow_duplicate=True),
    Input(component_id='drop_collection_tr_avg_price', component_property='value'),
    Input(component_id="apply_tr_avg_price", component_property='n_clicks'),
    prevent_initial_call=True,
)

def update_graph(collection_value, n_clicks):
    # triggered_id = ctx.triggered_id
    if n_clicks is None:
        raise PreventUpdate
    else:
        fig = mdl.class_launcher(collection_value,1, 24, True, 'floor_price')
    return fig