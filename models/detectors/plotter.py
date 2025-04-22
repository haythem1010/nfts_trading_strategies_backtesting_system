import pandas as pd
from plotly.offline import plot
import plotly.express as px
import plotly.graph_objects as go



def plotter(data, double_bottoms):
    df = pd.DataFrame(data)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y=df['average_trading_price'], mode='lines', name='Price'))
    for double_bottom in double_bottoms:
        db_df = pd.DataFrame(double_bottom)
        mask = df['date'].isin(db_df['date'])
        fig.add_trace(go.Scatter(x=db_df['date'], y=db_df['average_trading_price'], mode='markers', name='Double Bottom', marker=dict(color='black', size=8)))
        fig.add_trace(go.Scatter(x=df[mask]['date'], y=df[mask]['average_trading_price'], mode='lines',line=dict(color='green'), name='Double Bottom Region'))
        fig.update_layout(title='Double Bottom Detector')

        plot(fig)
        return fig