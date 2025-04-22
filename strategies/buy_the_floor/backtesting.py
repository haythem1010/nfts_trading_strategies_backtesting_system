from pprint import pprint


class Backtesting(object):

    @staticmethod
    def trades_dates(data):

        """
        :param data:
        :return:
        """
        # pprint(data)
        trades = []
        for i in data:
            if i['action'] != '--':
                trades.append({'date': i['date'], 'action': i['action'], 'price': i['average_trading_price']})

        return trades

    def only_one_position_allowed(self, data):
        """
        :param data:
        :return:
        """

        trades = self.trades_dates(data)
        i = 1
        while i < len(trades):
            if trades[i]['action'] == trades[i - 1]['action']:
                del trades[i]
                i = i-1
            i = i+1

        j = 0
        k = 0
        while j < len(data) and k < len(trades):
            if trades[k]['date'] == data[j]['date']:
                data[j]['action'] = trades[k]['action']
                k = k+1
                j = j+1
            else:
                data[j]['action'] = '--'
                j = j+1


        # print("-----------------------------------------------------------------------------------")
        return trades, data


    @staticmethod
    def backtesting_profitability(data):
        profit = 0
        for i in data:
            if i['action'] == 'buy':
                profit = profit - i['floor_price']
            elif i['action'] == 'sell':
                profit = profit + i['average_trading_price']

        return profit