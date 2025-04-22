from pprint import pprint
import dash
from dash import Dash, Input, Output, dcc, html, ctx
import plotly.express as px
import dash_bootstrap_components as dbc
from strategies.bollinger_band.signals import Backtesting
from strategies.bollinger_band.plotter import plot_the_strategy
from importers.collections_importers import CollectionsByAPI
from strategies.buy_the_floor.buy_the_floor import BuyTheFloor
from strategies.buy_the_floor.plotter import plot_data
from dashboard_prototype.navbar import create_navbar


col = CollectionsByAPI().get_available_collections(local_data=True)
graf = Backtesting()
btf_s = BuyTheFloor()

# app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.CERULEAN], suppress_callback_exceptions=True)

NAVBAR = create_navbar()
# To use Font Awesome Icons
FA621 = "https://use.fontawesome.com/releases/v6.2.1/css/all.css"
APP_TITLE = "NFTs trading strategies backtesting system"

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dbc.themes.LUX,  # Dash Themes CSS
        FA621,  # Font Awesome Icons CSS
    ],
    title=APP_TITLE,
    use_pages=True,  # New in Dash 2.7 - Allows us to register pages
)
definition = html.P("Trading strategies Backtesting is a critical component of a trader's toolkit. It involves evaluating the performance of a trading strategy using historical market data to assess itsviability and potential profitability. By simulating trades and applying the strategy's rules to past market conditions, traders can gain valuable insights into how the strategy would have performed in the past. Backtesting allows traders to analyze risk-reward ratios, win rates, drawdowns, and other performance metrics, enabling them to make informed decisions about deploying the strategy in live trading. It also helps traders refine and optimize their strategies, identifying strengths, weaknesses, and areas for improvement.")
simulation = html.P(" Trade simulation is a technique used in financial markets to model and evaluate the performance of trading strategies without risking real capital. It involves using historical market data and a set of trading rules to mimic the execution of trades over a specified time period.Adapting trade simulation to the NFT  realm involves customizing the simulation process to account for the unique characteristics and challenges of NFT trading by developing various trading strategies and then backtest them ")
strategies = html.P("Developing a successful NFT (Non-Fungible Token) trading strategy requires a combination of careful research, market analysis, and risk management. Start by understanding the NFT space, including the various blockchain platforms and the types of NFTs available. Identify trends, artists, or projects with strong communities and potential for future value appreciation. Diversify your portfolio to spread risk and avoid putting all your assets into a single NFT. Stay up-to-date with news and events in the NFT ecosystem, as this can influence market sentiment. Additionally, set clear entry and exit points, define your risk tolerance, and employ stop-loss orders to protect your investments. Continuously adapt and refine your strategy based on market conditions and your own experience, and remember that NFT trading can be highly speculative, so never invest more than you can afford to lose.")


documentation = html.Div([
    html.H2('NFTs Trading Strategies Backtesting System ', style={'textAlign': 'center', 'color': '#614A8A'}),
    html.Div(definition, style={}),
    html.H2(" Trades Simulation ", style={'textAlign': 'center', 'color': '#614A8A'}),
    html.Div(simulation, style={}),
    html.H2('How to develop a NFTs trading strategy ?', style={'textAlign': 'center', 'color': '#614A8A'}),
    html.Div(strategies, style={})

], style={'padding': '10px'})

app.layout = dcc.Loading(
    id='loading_page_content',
    children=[
        html.Div(
            [
                NAVBAR,
                dash.page_container,
                documentation

            ]
        )
    ],
    color='primary',  # <- Color of the loading spinner
    fullscreen=True  # <- Loading Spinner should take up full screen
)

server = app.server

if __name__ == '__main__':
    app.run_server(debug=False)