from pprint import pprint
from plotly.offline import plot
import pandas
from importers.collections_importers import CollectionsByAPI
from strategies.buy_the_floor.risk_management_rules import RiskManagementRules
from strategies.buy_the_floor.backtesting import Backtesting
from strategies.buy_the_floor.plotter import plot_data
from time import time
from utils.helpers import calculate_sma
from local_data.data_readers import Readers

""" 
        This class in allocated for applying the strategy with the name buy the floor.
        The main idea of this strategy is purchasing the element with the least listing price
        and then sell it after a certain period of time in perspective of gaining popularity in 
        the future  . 

"""


class BuyTheFloor(object):
    rm = RiskManagementRules()
    rd = Readers()
    bck = Backtesting()

    def build_the_strategy(self, collection, timeframe,):

        # listing_data = self.col.get_listing_data_stats_available(collection, days*1440)
        # trading_data = self.col.trading_data_correction(collection, days, listing_data)
        buy_the_floor = self.rd.local_data_readers(collection, timeframe)

        # i = 0
        #
        # while i < len(listing_data) and i < len(trading_data):
        #     buy_the_floor.append({"date": listing_data[i]["date"],
        #                           "listed_elements": listing_data[i]["ls_count"],
        #                           "transaction_count": trading_data[i]["tr_count"],
        #                           "floor_price": listing_data[i]["ls_min_price"],
        #                           "minimum_trading_price": trading_data[i]["tr_min_price"],
        #                           "maximum_trading_price": trading_data[i]["tr_max_price"],
        #                           "average_trading_price": trading_data[i]["tr_avg_price"]})
        #     i = i + 1
        #
        # # pprint(buy_the_floor)

        return buy_the_floor

    def buy_sell(self, collection, timeframe, window, local_data=True):
        start = time()
        data = self.build_the_strategy(collection, timeframe)
        calculate_sma(data, 'average_trading_price', window,'moving_average')
        pprint(data)
        i = window
        while i < len(data):
            small_data = data[i - window: i]
            data[i]["action"] = self.rm.risk_management(small_data)
            i = i + 1

        # data[period]['action'] = 'buy'
        trades, trading_data = self.bck.only_one_position_allowed(data[window:])
        profit = self.bck.backtesting_profitability(trading_data)
        df_trading = pandas.DataFrame(trading_data)
        # pprint(trading_data)
        # pprint(trades)
        print(" Number of trades made within this period is : ", len(trades))
        print("The income of this collection = ", profit)
        # print(type(trading_data), "--", type(trades), "---", type(profit))
        fig = plot_data(df_trading)
        # plot(fig)

        end = time()
        exe = end - start
        print("-----------------------------------------------------------------------------------")
        print("execution time is : ", exe)
        return df_trading, trades, profit, fig


# btf = BuyTheFloor()
# ser = btf.buy_sell("DGOD", 24, 5)
# ser = btf.build_the_strategy("DGOD", 1)