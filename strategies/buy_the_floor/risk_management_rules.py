from pprint import pprint
from utils.helpers import percent_change, find_different_element

# data :
#               {'average_trading_price': 433.6975,
#               'date': '2022-12-25 01:00:00',
#               'floor_price': 455,
#               'listed_elements': 419,
#               'maximum_trading_price': 666,
#               'minimum_trading_price': 419,
#               'transaction_count': 238}

class RiskManagementRules(object):
    @staticmethod

    def take_profit_sell(data):
        """
        :param data:
        :return:
        """
        i = 1
        buy_sell = []
        while i < len(data):
            if percent_change(data[i - 1]['transaction_count'], data[i]['transaction_count']) > 10 \
                    and percent_change(data[i - 1]['average_trading_price'], data[i]['average_trading_price']) > 10:

                buy_sell.append('sell')
            else:
                buy_sell.append('--')

            i = i+1
        for j in buy_sell:
            if j != '--':
                decision = j
            else:
                decision = "--"
        return decision

    @staticmethod
    def stop_loss_sell(data):
        i = 1
        buy_sell = []
        while i < len(data):
            if percent_change(data[i - 1]['transaction_count'], data[i]['transaction_count']) < -10 \
                    and percent_change(data[i - 1]['average_trading_price'], data[i]['average_trading_price']) < -10:

                buy_sell.append('sell')
            else:
                buy_sell.append('--')
            i = i+1
        for j in buy_sell:
            if j != '--':
                decision = j
            else:
                decision = "--"
        return decision

    @staticmethod
    def buy_at_floor_signal(data):
        i = 1
        buy = []
        while i < len(data):
            if 10 > percent_change(data[i-1]['average_trading_price'], data[i]['average_trading_price']) > 1 \
                    and percent_change(data[i-1]['floor_price'], data[i]['floor_price']) > 1:
                    # and percent_change(data[i-1]['listed_elements'], data[i]['listed_elements']) > 1:
                buy.append("buy")
            else:
                buy.append("--")
            i = i+1
        for j in buy:
            if j != '--':
                decision = j
            else:
                decision = "--"
        return decision

    def risk_management(self, data):
        decisions = []
        deci1 = self.buy_at_floor_signal(data)
        decisions.append(deci1)
        deci2 = self.stop_loss_sell(data)
        decisions.append(deci2)
        deci3 = self.take_profit_sell(data)
        decisions.append(deci3)
        deci = "--"
        # print(decisions)
        for i in decisions:
            if i != '--':
                deci = i
        return deci