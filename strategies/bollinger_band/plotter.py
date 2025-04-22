import plotly.express as px
import plotly.offline as plt
import pandas as pd

def plot_the_strategy(data, plotted=False):

    df = pd.DataFrame(data[1:len(data)])
    fig = px.line(data_frame=df, x='date', y=['lower_band','upper_band','mvg_average','trading_price'], title='Bollinger Band')
    # plt.plot(fig)
    return fig


# date = [data[e]['date'] for e in len(data)]
    # lower_band = [data[e]['lower_band'] for e in len(data)]
    # upper_band = [data[e]['upper_band'] for e in len(data)]
    # average = [data[e]['mvg_average'] for e in len(data)]
    # tr_price = [data[e]['trading_price'] for e in len(data)]

    # trace1 = go.Scatter(x=date, y=lower_band, mode='lines', name='Lower band', fillcolor='blue')
    # trace2 = go.Scatter(x=date, y=upper_band, mode='lines', name='Upper Band', fillcolor='blue')
    # trace3 = go.Scatter(x=date, y=average, mode='lines', name='Moving Average Price')
    # trace4 = go.Scatter(x=date, y=tr_price, mode='lines', name='Average Trading Price')
    # fig = go.Figure(data=[trace3, trace1, trace2, trace4])
    # fig.update_layout(title='Multiple Line Chart', xaxis_title='Time')

    # def data_preparation(data):
    #     # date = []
    #     # lower_band = []
    #     # upper_band = []
    #     # average = []
    #     # tr_price = []
    #     # for i in data:
    #     #     date.append(data[i]['date'])
    #     #     lower_band.append(data[i]['lower_band'])
    #     #     upper_band.append(data[i]['upper_band'])
    #     #     average.append(data[i]['mvg_average'])
    #     #     tr_price.append(data[i]['trading_price'])
    #     # data.pop(0)
    #     df = pd.DataFrame(data[1:len(data)])
    #     print(len(data))
    #     # print(df)