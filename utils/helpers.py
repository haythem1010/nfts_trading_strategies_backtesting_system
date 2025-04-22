from datetime import datetime, timedelta
from pprint import pprint

import numpy as np
from requests import get
import pandas as pd
import plotly.express as px
from plotly.offline import plot
import json
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from prettytable import PrettyTable

#------------------------------------------------------------------------------------------------------

def splitting_dataframe_to_train(df, index_is_time=True, shuffle=False):
    if not index_is_time:
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'date', '0': 'floor_price'}, inplace=True)
        df = df.drop('date', axis=1)


    if shuffle:
        df = df.sample(frac=1, random_state=42)

    split_index = int(0.8*len(df))
    train_data = df.iloc[:split_index]  # Take the first 80% of rows as training data
    test_data = df.iloc[split_index:]   # The rest of the data is for testing the model

    return train_data, test_data

#------------------------------------------------------------------------------------------------------

def load_data_from_json(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
    return data

#------------------------------------------------------------------------------------------------------

def plot_data(data, plotted=False):
    df = pd.DataFrame(data)
    fig = px.line(data_frame=df, x='date', y=['floor_price','average_trading_price'], title='Double Bottoms')
    plot(fig)
    return fig

#------------------------------------------------------------------------------------------------------

def delete_duplicates(list):
    my_set = set()
    list_no_dp = [i for i in list if not(i in my_set or my_set.add(i))]
    return list_no_dp
#------------------------------------------------------------------------------------------------------

def convert_timestamp_to_date(time, output_format='%Y-%m-%d %H:%M:%S'):
    time = time // 1000
    dt = datetime.fromtimestamp(time)
    return dt.strftime(output_format)
#------------------------------------------------------------------------------------------------------

def create_time_range(start_date, end_date, delay):
    time_range = []
    start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S').date()
    while start_date <= end_date:
        time_range.append(start_date)
        start_date = start_date + timedelta(minutes=delay)

    return time_range
#------------------------------------------------------------------------------------------------------

def percent_change(old, new):
    """
    :param old: the value that occurs before in time
    :param new: the current value
    :return: the percentage of change between two values taken as parameter
    """
    percent = ((new - old) / abs(old)) * 100
    return percent
#------------------------------------------------------------------------------------------------------

# def find_different_element(lst):
#
#     for i in range(1, len(lst)):
#         if lst[i] != lst[0]:
#             return lst[i]
#     return lst[0]
#------------------------------------------------------------------------------------------------------

def find_different_element(lst):

    for i in range(1, len(lst)):
        if lst[i] != lst[0]:
            return lst[i]
    return lst[0]

#------------------------------------------------------------------------------------------------------
def calculate_sma(data, key, window, new_mesure):
    """
    :param data: data source
    :param key: the key used to calculate simple moving average
    :param window: period used to calculate the moving average
    :return: list of reals calculated starting from the day number "window" to the last day available
    """
    tr_avg_price = [d[key] for d in data]
    for i in range(window, len(tr_avg_price)):
        sma = sum(tr_avg_price[i-window:i]) / window
        data[i][new_mesure] = sma
    return 0

#------------------------------------------------------------------------------------------------------
def calculate_expo_ma(data, key, window, smoothing, new_mesure):
    """
    :param data:data source
    :param key: the key used to calculate simple moving average
    :param window: period used to calculate the moving average
    :param smoothing: factor determines the weight given to the most recent price data in the EMA calculation.
    :return:
    """

    smoothing_factor = smoothing / (window+1)
    average_price = [d[key] for d in data]
    for i in range(len(average_price)):
        if i == 0:
            data[i][new_mesure] = average_price[i]
        else:
            ema = average_price[i] * smoothing_factor + data[i-1][new_mesure] * (1-smoothing_factor)
            data[i][new_mesure] = ema
    return 0

#------------------------------------------------------------------------------------------------------

def sql_to_dict(sql_data, labels, type=1):
    """
    :param sql_data:
    :param labels:
    :param type: type 2 : [{'a': a, 'b':a}, ....], type 1 : {'a': [...], 'b':[...]}
    :return:
    """
    if type == 2:
        list_of_dict = []
        for s in sql_data:
            assert len(s) == len(labels)
            dicti = {}
            for el, l in zip(s, labels):
                dicti[l] = el
            list_of_dict.append(dicti)
    else:
        list_of_dict = {}
        for l in labels:
            list_of_dict[l] = []
        for s in sql_data:
            assert len(s) == len(labels)
            for el, l in zip(s, labels):
                list_of_dict[l].append(el)
    return list_of_dict

#------------------------------------------------------------------------------------------------------

def get_ip_address():
    # hostname = socket.gethostname()
    # print(hostname)
    # ip_address = socket.gethostbyname(hostname)
    ip_address = get('https://api.ipify.org').content.decode('utf8')
    return ip_address

#------------------------------------------------------------------------------------------------------

def reversed_differencing_dataframe_edition(df):
    df_reverse = df[::-1]
    df_reverse['sum_column'] = df_reverse['column_name'].rolling(window=2).sum()
    df_sum = df_reverse[::-1]
    return df_sum

#------------------------------------------------------------------------------------------------------------

def models_evaluation(actual_values, predicted_values):
    score_mae = mean_absolute_error(actual_values, predicted_values)
    score_r2 = r2_score(actual_values, predicted_values)
    score_rmse = np.sqrt(mean_squared_error(actual_values, predicted_values))

    x = PrettyTable()

    x.field_names = ["MAE", "R-squared", "RMSE"]

    x.add_row([score_mae, score_r2, score_rmse])

    print(x)
    return 0