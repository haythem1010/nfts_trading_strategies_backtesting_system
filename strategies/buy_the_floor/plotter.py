from pprint import pprint

import pandas as pd
import plotly.express as px




def plot_data(data, plotted=False):
    fig = px.line(data_frame=data, x='date', y=['floor_price', 'moving_average','average_trading_price'], title='Buy The Floor')
    # plot(fig)
    return fig