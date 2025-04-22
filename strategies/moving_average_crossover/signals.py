from pprint import pprint


class Signals(object):
    @staticmethod
    def buy_signal(data):
        i = 1
        while i < len(data):
            if data[i]['slow_moving_average'] < data[i]['fast_moving_average'] and data[i-1]['slow_moving_average'] > data[i-1]['fast_moving_average']:
                data[i-1]['action'] = 'buy'
            else:
                data[i - 1]['action'] = '--'
            i += 1
        data[len(data)-1]['action'] = '--'

    @staticmethod
    def sell_signal(data):
        i = 1
        while i < len(data):
            if data[i]['slow_moving_average'] > data[i]['fast_moving_average'] and data[i - 1]['slow_moving_average'] < data[i - 1]['fast_moving_average']:
                data[i - 1]['action'] = 'sell'
            i += 1