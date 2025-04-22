import pandas as pd
import plotly.express as px
from plotly.offline import plot

def plot_the_strategy(data, plotted=False):

    df = pd.DataFrame(data[1:len(data)])
    fig = px.line(data_frame=df, x='date', y=['average_trading_price', 'fast_moving_average', 'slow_moving_average'], title='Moving Average Crossover')
    # plot(fig)
    return fig