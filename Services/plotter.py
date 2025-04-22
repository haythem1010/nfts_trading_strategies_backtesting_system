import plotly.graph_objects as go
from plotly.offline import plot
import plotly.express as px

def plot_data(data, plotted=False):
    date = []
    average_price = []
    floor = []
    mini = []
    decision = []
    for i in data:
        date.append(i['date'])
        average_price.append(i["average_trading_price"])
        floor.append(i['floor_price'])
        mini.append(i["minimum_trading_price"])
        # pprint(i["decision"])
        # decision.append(i["decision"])

    # fig = go.Figure()

    trace1 = go.Scatter(x=date, y=average_price, mode='lines', name='Average Trading Price')
    trace2 = go.Scatter(x=date, y=floor, mode='lines', name='Floor Price')
    trace3 = go.Scatter(x=date, y=mini, mode='lines', name='Minimum Trading Price')
    fig = px.line(data=[trace3,trace1,trace2])
    # fig.update_layout(title='Multiple Line Chart', xaxis_title='Time')
    fig.update_layout(title="Average Trading Price", xaxis_title='Time') # hovertemplate='Value Y: %{y}<br>Value Z: %{customdata[0]}', customdata=[decision])
    if plotted:
        plot(fig)
    return






















# data = BacktestingVONE()
# list_of_names, time_strings, tr, sol = data.backtesting_v1()
# print(len(time_strings))
#
# fig_1, ax = plt.subplots()
# ax.bar(time_strings, tr, width=0.5)
#
# ax.set_xticks(time_strings)
# ax.set_xticklabels(time_strings, rotation=90)
#
# ax.set_xlabel('Date')
# ax.set_ylabel('Trading Volume')
# ax.set_title('Daily Trading Volume')
#
# # Show plot
# plt.show()

