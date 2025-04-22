from dash import html, register_page, callback, dcc, Input, Output, State
import dash_bootstrap_components as dbc

register_page(
    __name__,
    name='Pattern Detection',
    top_nav=True,
    path='/PatternDetection.py'
)

radio_style = {}



layout = html.Div([
    html.H3([
            " Pattern Recognition "], style={'textAlign': 'center', 'margin-top': '20px'}),
    dbc.Row([
        dbc.Col([
            dcc.RadioItems([
                {"label": html.Div(['Trend Reversal'], style={'color': 'Black', 'font-size': '14px', 'font-weight': 'bold'}), "value": "Double_Top", "disabled": True},
                {"label": html.Div(['Double Top'], style={'color': 'Red', 'font-size': '12px'}), "value": "Double_Top", },
                {"label": html.Div(['Double Bottom'], style={'color': 'Green', 'font-size': '12px'}), "value": "Double_Bottom"},
                {"label": html.Div(['Head and Shoulders'], style={'color': 'Red', 'font-size': '12px'}), "value": "Head_and_Shoulders"},
                {"label": html.Div(['Inverse Head and Shoulders'], style={'color': 'Green', 'font-size': '12px'}), "value": "Reversal_Head_and_Shoulders"},
                {"label": html.Div(['Falling Wedge'], style={'color': 'Green', 'font-size': '12px'}), "value": "Falling_Wedges"},
                {"label": html.Div(['Rising Wedge'], style={'color': 'Red', 'font-size': '12px'}), "value": "Rising_Wedge"},
                {"label": html.Div(['Trend Continuation'], style={'color': 'Black', 'font-size': '14px','font-weight': 'bold'}), "value": "Triangle", "disabled": True},
                {"label": html.Div(['Symmetrical Triangle'], style={'color': 'Blue', 'font-size': '12px'}), "value": "Symmetrical_Triangle"},
                {"label": html.Div(['Ascending Triangle'], style={'color': 'Blue', 'font-size': '12px'}), "value": "Ascending_Triangle"},
                {"label": html.Div(['Descending Triangle'], style={'color': 'Blue', 'font-size': '12px'}), "value": "Descending_Triangle"},
                {"label": html.Div(['Pennant'], style={'color': 'Blue', 'font-size': '12px'}), "value": "Pennant"},
                {"label": html.Div(['Flag'], style={'color': 'Blue', 'font-size': '12px'}), "value": "Flag"},
            ], labelStyle={"display": "flex", "align-items": "center"}, style={'margin-top': '10px'})
        ], width=2, style={'height': '500px', 'border': '1px solid black'}),
        dbc.Col([
            dcc.Graph(id='pattern')
        ], width=10)
    ], style={'margin-top': '15px', 'margin-left': '15px'}),

])
