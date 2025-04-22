from dash import html, register_page, callback
import dash_bootstrap_components as dbc
register_page(
    __name__,
    name='Predictions',
    top_nav=True,
    path='/Predictions.py'
)


def layout():
    layout = html.Div([
        html.H1(
            [
                " This page is for time series predicitions : "
            ]
        ),
        html.H1([
            " This page is for trading strategies : "
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Button("Floor Price", id='apply', color="dark", outline=True, href='/floor_price.py',
                           style={'weight': '200px', 'height': '45px'})
            ]),
            dbc.Col([
                dbc.Button("Average Trading Price", id='apply', color="dark", outline=True, href='/average_trading_price.py',
                           style={'weight': '200px', 'height': '45px'})
            ])
        ], style={'padding': '10px'})
    ])
    return layout