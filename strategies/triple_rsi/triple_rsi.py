from pprint import pprint
from strategies.triple_rsi.signals import Signals
from strategies.triple_rsi.plotter import plot_the_strategy
from time import time
from strategies.triple_rsi.backtesting import Backtesting
from repository.transactions_stats_repo import TransactionsStatsRepository
from local_data.data_readers import Readers
from plotly.offline import plot


class TripleRSI(object):

    imp = TransactionsStatsRepository()
    sig = Signals()
    back = Backtesting()
    rd = Readers()

    def data_preparation(self, collection, days, timeframe, local_data=True):
        triple_rsi = []
        if not local_data:
            trading_data, listing_data = self.imp.class_launcher(collection, days *1440)

            i = 0
            while i < len(listing_data) and i < len(trading_data):
                triple_rsi.append({"date": listing_data[i]["date"],
                                   "listed_elements": listing_data[i]["ls_count"],
                                   "transaction_count": trading_data[i]["tr_count"],
                                   "floor_price": listing_data[i]["ls_min_price"],
                                   "minimum_trading_price": trading_data[i]["tr_min_price"],
                                   "maximum_trading_price": trading_data[i]["tr_max_price"],
                                    "average_trading_price": trading_data[i]["tr_avg_price"]})
            i = i + 1
        else :
            triple_rsi = self.rd.local_data_readers(collection, timeframe)
        # pprint(triple_rsi)
        return triple_rsi

    def triple_rsi(self, collection, days, slow, fast, mid, timeframe,local_data=True):
        start = time()
        triple_rsi = self.data_preparation(collection, days, timeframe, local_data)
        self.sig.gain_loss_calcul(triple_rsi)
        self.sig.true_relative_strength(triple_rsi, mid, 'mid_rsi')
        self.sig.true_relative_strength(triple_rsi, fast, 'fast_rsi')
        self.sig.true_relative_strength(triple_rsi, slow, 'slow_rsi')
        triple_rsi = self.sig.buy_signal(triple_rsi[slow:])
        triple_rsi = self.sig.sell_signal(triple_rsi[slow:])
        # pprint(triple_rsi)
        fig = plot_the_strategy(triple_rsi)
        # plot(fig)
        trades, profit = self.back.trades(triple_rsi)
        # pprint(trades)
        # for i in triple_rsi:
        #     print(i['slow_rsi'],'**',i['mid_rsi'],'**',i['fast_rsi'],'**')
        # plot_the_strategy(triple_rsi)
        print("----------------------------------------------------------------------------------------")
        print("trades made in this period is : ", len(trades))
        print("The profitabilty of this strategy : ", profit)

        #------------------------------------------------
        end = time()
        ex = end - start
        print("----------------------------------------------------------------------------------------")
        print("the execution time is : ", round(ex, 3), " sec")
        return triple_rsi, trades, profit


# rsi = TripleRSI()
# col = rsi.triple_rsi('DGOD, 0.25, 21, 7, 14, 24, local_data=True')