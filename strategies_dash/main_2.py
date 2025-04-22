# from pprint import pprint
#
# import dash
# from dash import Input, Output, dcc, html, ctx
# import plotly.express as px
# import dash_bootstrap_components as dbc
# from strategies.bollinger_band.signals import Backtesting
# from strategies.bollinger_band.plotter import plot_the_strategy
# from importers.collections_importers import CollectionsByAPI
# from strategies.buy_the_floor.buy_the_floor import BuyTheFloor
# from strategies.buy_the_floor.plotter import plot_data
#
# col = CollectionsByAPI().get_available_collections()
# graf = Backtesting()
# btf_s = BuyTheFloor()
#
# dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
# app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP,dbc_css])
#
# app.layout = html.Div([
#     dbc.Row([
#         html.Span("0F035D", style={'align': 'center', 'color': '#0F035D'}),
#         html.Hr(style={'height': '10px', 'color': '0F035D'})
#     ]),
#
#     dbc.Row([
#         dbc.Col([
#             html.Span([
#                 html.I(className='fa-solid fa-plane-departure'),
#                 html.I(className='fa-solid fa-plane-departure'),
#                 " NFTs Trading Strategies ",
#                 html.I(className="fa-solid fa-plane-departure")], className='h1')
#             ], width={"size": 6, "offset": 3})
#         ], justify='center', className='my-2'),
#
#     dbc.Row([
#         html.Div([
#                 dbc.Button(
#                     dcc.Link(
#                         f"{page['name']} ", href=page["relative_path"],
#                     ), outline='True', color='info', style={'align': 'center', 'color': '#181812', 'font-size':'10', 'weight':'70px', 'height':'35px'}
#                 ) for page in dash.page_registry.values()
#             ]), dash.page_container ,
# ])],style={'background-color': '#0F035D','width': '100%', 'height': '100%'})
#
#
#
#
# if __name__ == '__main__':
#     app.run_server(debug=True)