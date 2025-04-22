from pprint import pprint
from utils.helpers import calculate_expo_ma


class Signals(object):

    @staticmethod
    def gain_loss_calcul(data):
        data[0]['loss'] = 0
        data[0]['gain'] = 0
        for i in range(1, len(data)):
            change = data[i]['average_trading_price'] - data[i-1]['average_trading_price']
            if change > 0:
                data[i]['gain'] = change
                data[i]['loss'] = 0
            elif change < 0:
                data[i]['loss'] = abs(change)
                data[i]['gain'] = 0
            else:
                data[i]['loss'] = 0
                data[i]['gain'] = 0


    @staticmethod
    def true_relative_strength(data, window, mesure):
        calculate_expo_ma(data, 'gain', window, 2, 'average_gain')
        calculate_expo_ma(data, 'loss', window, 2, 'average_loss')

        for i in range(window, len(data)):
            # j = i - window
            # sum_gain = 0
            # sum_loss = 0
            # while j <= i:
            #     sum_gain = sum_gain + data[j]['gain']
            #     sum_loss = sum_loss + data[j]['loss']
            #     j = j+1
            # average_gain = sum_gain / window
            # average_loss = sum_loss / window
            # data[i]['average_gain'] = average_gain
            # data[i]['average_loss'] = average_loss
            data[i][mesure] = 100 - (100/(1+(data[i]['average_gain']/data[i]['average_loss'])))


    @staticmethod
    def buy_signal(data):
        i = 1
        while i < len(data):
            if data[i-1]['fast_rsi'] > data[i-1]['mid_rsi'] and data[i]['fast_rsi'] < data[i]['mid_rsi'] \
                    and data[i-1]['mid_rsi'] > data[i-1]['slow_rsi'] and data[i]['mid_rsi'] < data[i]['slow_rsi']:
                data[i]['action'] = 'buy'
            else:
                data[i]['action'] = '--'
            i = i+1
        data[len(data) - 1]['action'] = '--'
        return data

    @staticmethod
    def sell_signal(data):
        i = 1
        while i < len(data):
            if data[i - 1]['fast_rsi'] < data[i - 1]['mid_rsi'] and data[i]['fast_rsi'] > data[i]['mid_rsi'] \
                    and data[i-1]['slow_rsi'] > data[i-1]['mid_rsi'] and data[i]['slow_rsi'] < data[i]['mid_rsi']:
                data[i]['action'] = 'sell'
            i = i+1
        return data