from pprint import pprint
from repository.transactions_stats_repo import TransactionsStatsRepository
from utils.helpers import calculate_expo_ma, calculate_sma
from strategies.moving_average_crossover.plotter import plot_the_strategy
from time import time
from strategies.moving_average_crossover.backtesting import Backtesting
from strategies.moving_average_crossover.signals import Signals
from strategies.moving_average_crossover.volatility_mesures import Volatility
from strategies.moving_average_crossover.risk_management import RiskManagement
from local_data.data_readers import Readers



class MovingAverageCrossOver(object):

    imp = TransactionsStatsRepository()
    signals = Signals()
    back = Backtesting()
    vol = Volatility()
    rm = RiskManagement()
    rd = Readers()

    def data_preparation(self, collection, days, timeframe, local_data=False, ):
        ma_crossover = []
        if not local_data:
            trading_data, listing_data = self.imp.class_launcher(collection, days*1440)
            i = 0
            while i < len(listing_data) and i < len(trading_data):
                ma_crossover.append({"date": listing_data[i]["date"],
                                    "listed_elements": listing_data[i]["ls_count"],
                                    "transaction_count": trading_data[i]["tr_count"],
                                    "floor_price": listing_data[i]["ls_min_price"],
                                    "minimum_trading_price": trading_data[i]["tr_min_price"],
                                    "maximum_trading_price": trading_data[i]["tr_max_price"],
                                    "average_trading_price": trading_data[i]["tr_avg_price"]})
            i = i + 1
        else:
            ma_crossover = self.rd.local_data_readers(collection, timeframe)

        # pprint(buy_the_floor)

        return ma_crossover

    def build_the_strategy(self, collection,days, fast, slow, timeframe):
        start = time()
        ma_crossover = self.data_preparation(collection, days, timeframe, local_data=True)
        for i in ma_crossover:
            i['action'] = '--'
        calculate_expo_ma(ma_crossover, 'average_trading_price', fast, 2, 'fast_moving_average')
        calculate_expo_ma(ma_crossover, 'average_trading_price', slow, 2, 'slow_moving_average')
        # calculate_sma(ma_crossover, 'average_trading_price', window=fast, new_mesure='fast_moving_average')
        # calculate_sma(ma_crossover, 'average_trading_price', window=slow, new_mesure='slow_moving_average')
        # pprint(ma_crossover)
        fig = plot_the_strategy(ma_crossover)
        print("------------------------------------------------------------------------")

        self.signals.buy_signal(ma_crossover)
        self.signals.sell_signal(ma_crossover)
        # pprint(ma_crossover)
        trades, profit = self.back.trades(ma_crossover)
        # pprint(trades)
        print("------------------------------------------------------------------------")

        # new_data, standardized_maxi = self.vol.average_true_range_calculation(ma_crossover[slow:], slow)
        # self.rm.verif(new_data, standardized_maxi)
        print("------------------------------------------------------------------------")

        print('The number of trades made is : ', len(trades))
        print('the profit from this strategy is : ', profit, 'SOL')
        print('------------------------------------------------------------------------')

        end = time()
        ex = end - start
        print("MACO execution time is : ", round(ex, 3), "sec")
        return ma_crossover, trades, profit

# maco = MovingAverageCrossOver()
# maco1 = maco.build_the_strategy('DGOD', 1, 3, 10, 24)