import pandas as pd
from plotly.offline import plot
import plotly.express as px

def plot_the_strategy(data, plotted=False):

    df = pd.DataFrame(data[1:len(data)])
    fig = px.line(data_frame=df, x='date', y=['average_trading_price', 'fast_rsi', 'slow_rsi', 'mid_rsi'], title='TRIPLE RSI')
    return fig