from pprint import pprint

from strategies.bollinger_band.bollinger_band import BollingerBand
from strategies.bollinger_band.risk_mngmnt import BolingerBandRiskMngmnt
from repository.transactions_stats_repo import TransactionsStatsRepository
from utils.helpers import calculate_expo_ma
from time import time
from strategies.bollinger_band.plotter import plot_the_strategy

class Backtesting(object):
    bb = BollingerBand()
    rsk = BolingerBandRiskMngmnt
    col = TransactionsStatsRepository()

    def data_preparation(self, collection, timeframe):
        trading_data, listing_data = self.col.class_launcher(collection, timeframe)
        data = []

        i = 0

        while i < len(listing_data) and i < len(trading_data) and trading_data[i]['date'] == listing_data[i]['date']:
            data.append({"date": listing_data[i]["date"],
                         "listed_elements": listing_data[i]["ls_count"],
                         "transaction_count": trading_data[i]["tr_count"],
                         "floor_price": listing_data[i]["ls_min_price"],
                         "minimum_trading_price": trading_data[i]["tr_min_price"],
                         "maximum_trading_price": trading_data[i]["tr_max_price"],
                         "average_trading_price": trading_data[i]["tr_avg_price"],
                         "minimum_listing_price": listing_data[i]["ls_min_price"],
                         "maximum_listing_price": listing_data[i]["ls_min_price"],
                         "average_listing_price": listing_data[i]["ls_avg_price"]})
            i = i + 1
            calculate_expo_ma(data, 'average_trading_price', 7, 2, 'trading_price_moving_average')
        return data

    @staticmethod
    def only_one_position_allowed(data):
        i = 1
        while i < len(data):
            if data[i]["action"] == data[i-1]["action"] and data[i-1]["action"] == 'sell':
                data[i-1]['action'] = 'hold'
            elif data[i]["action"] == data[i - 1]["action"] and data[i - 1]["action"] == 'buy':
                data[i - 1]['action'] = '--'
            i = i+1
        trades = []
        for i in data:
            if i['action'] == 'buy' or i['action'] == 'sell':
                trades.append({'date': i['date'], 'price': i['price'], 'action': i['action']})
        return trades

    def backtest_bollinger_band(self, collection, window, timeframe):
        st = time()
        data = self.bb.lower_upper_band(collection, window, timeframe)
        trades = []
        for i in range(len(data)):
            if data[i]['trading_price'] <= data[i]['lower_band']:
                # Buy signal
                trades.append({'date': data[i]['date'], 'price': data[i]['trading_price'], 'action': 'buy'})
            elif data[i]['trading_price'] >= data[i]['upper_band']:
                # Sell signal
                trades.append({'date': data[i]['date'], 'price': data[i]['trading_price'], 'action': 'sell'})

        trades = self.only_one_position_allowed(trades)
        # self.rsk.take_profit_rule(trades, 5)
        # self.rsk.stop_loss_rule(trades, 5)

        number_of_trades = 0
        pnl = 0

        for i in trades:
            if i["action"] == 'buy':
                #purchasing assets
                pnl = pnl - i['price']
                number_of_trades = number_of_trades + 1
            elif i["action"] == 'sell':
                #selling assets
                pnl = pnl + i['price']
                number_of_trades = number_of_trades + 1

        print("-----------------------------------------------------")
        # pprint(trades)
        # pprint(data)
        print("The number of trades made : ", number_of_trades)
        print("The return from this strategy would be : ", pnl, "  SOLANA")
        # plot_the_strategy(data, plotted=True)

        fin = time()
        ex = fin - st
        print("-----------------------------------------------------")
        print("execution time is : ", round(ex, 3), " sec")

        return trades, data, pnl

#
# backtest = Backtesting()
# bb = backtest.backtest_bollinger_band("DGOD", 7, 24)