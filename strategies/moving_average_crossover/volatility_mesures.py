from pprint import pprint
from plotly.offline import plot
import plotly.express as px
import pandas as pd
import numpy as pp


class Volatility(object):

    @staticmethod
    def standardize_values(data, key):
        list_by_key = [i[key] for i in data]
        standardized_values = []
        maxi = max(list_by_key)
        mini = min(list_by_key)
        for i in list_by_key:
            standardized = (i-mini) / (maxi-mini)
            standardized_values.append(standardized)
        return standardized_values


    def true_range_calculation(self, data):
        i = 1
        standardized_maxi = self.standardize_values(data, 'maximum_trading_price')
        standardized_mini = self.standardize_values(data, 'minimum_trading_price')
        standardized_average = self.standardize_values(data, 'average_trading_price')

        while i < len(data):
            maxi = standardized_maxi[i]
            mini = standardized_mini[i]
            c = standardized_average[i-1]
            data[i]['true_range'] = max(maxi-mini, abs(maxi-c), abs(mini-c))
            r = max(maxi, mini, c)
            data[i]['true_range_r'] = data[i]['true_range'] / r
            i = i+1
        data[0]['true_range'] = 0
        # pprint
        return standardized_maxi



    def average_true_range_calculation(self, data, window):
        standardized_maxi = self.true_range_calculation(data)
        new_data = data[window:]

        for i in range(window, len(data)):
            j = i - window+1
            aux = 0
            while j <= i:
                aux = aux + data[j]['true_range']
                j = j+1
            new_data[i-window]['ATR'] = aux

        for i in range(len(new_data)):
            new_data[i]['ATR'] = new_data[i]['ATR']/window

        df = pd.DataFrame(new_data)
        fig = px.line(data_frame=df, x='date', y='ATR', title='ATR')
        plot(fig)

        return new_data, standardized_maxi

