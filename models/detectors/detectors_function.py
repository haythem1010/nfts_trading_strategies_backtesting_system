from repository.transactions_stats_repo import TransactionsStatsRepository
from time import time
from utils.helpers import percent_change, calculate_expo_ma
from pprint import pprint
from models.detectors.plotter import plotter
from local_data.data_readers import Readers


class PatternRecognition(object):
    col = TransactionsStatsRepository()
    local = Readers()

    def data_preparation(self, collection, timeframe, local_data = True):
        data = []
        if not local_data:
            trading_data, listing_data = self.col.class_launcher(collection, timeframe)

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
        else:
            data = self.local.local_data_readers(collection, 12)
        calculate_expo_ma(data, 'average_trading_price', 7, 2, 'moving_average')
        return data

    @staticmethod
    def lows_detector(data):

        lows_indices = []
        i = 1
        while i < len(data)-1:
            if (data[i]['average_trading_price'] < data[i - 1]['average_trading_price']) \
                    and data[i]['average_trading_price'] < data[i + 1]['average_trading_price']:
                lows_indices.append(i)
            i = i + 1
        # print(" ***** Lows")
        # print(lows_indices)
        return lows_indices

    @staticmethod
    def highs_detector(data):
        highs_indices = []
        i = 1
        while i < len(data)-1:
            if (data[i]['average_trading_price'] > data[i - 1]['average_trading_price'])\
                    and data[i]['average_trading_price'] > data[i + 1]['average_trading_price']:
                highs_indices.append(i)
            i = i + 1
        # print(" ***** Highs")
        # print(highs_indices)
        return highs_indices

    def double_tops_detector(self, data):

        lows_indices = self.lows_detector(data)
        highs_indices = self.highs_detector(data)
        i = 2 # for highs
        j = 2 # for lows
        double_tops = []

        while i < len(highs_indices) and j < len(lows_indices):
            if (highs_indices[i] < lows_indices[j] < highs_indices[i+1]) \
                    and (data[highs_indices[i]]['average_trading_price']/data[highs_indices[i-1]]['average_trading_price'] > 1) \
                    and (1.5 > data[highs_indices[i]]['average_trading_price']/data[highs_indices[i+1]]['average_trading_price'] > 1) \
                    and (data[highs_indices[i - 1]]['average_trading_price'] / data[highs_indices[i - 2]]['average_trading_price'] > 1) \
                    and (data[highs_indices[i]]['average_trading_price']/data[lows_indices[j]]['average_trading_price'] > 1.5)\
                    and (1.2 > data[lows_indices[j]]['average_trading_price']/data[lows_indices[j-1]]['average_trading_price'] > 0.9)\
                    and (data[highs_indices[i]]['average_trading_price'] / data[lows_indices[j+1]]['average_trading_price'] > 1.5):

                list_aux = data[lows_indices[i-1]:lows_indices[j+1]]
                double_tops.append(list_aux)

            i = i+1
            j = j+1
        print(len(double_tops))
        # pprint(double_tops)
        return double_tops

    def double_bottoms_detector(self, data):

        lows_indices = self.lows_detector(data)
        highs_indices = self.highs_detector(data)
        i = 0 # for highs
        j = 0 # for lows

        double_bottoms = []

        while i < len(highs_indices) and j < len(lows_indices):
            if (highs_indices[i] < lows_indices[j] < highs_indices[i+1])\
                    and (data[highs_indices[i]]['average_trading_price']/data[lows_indices[j]]['average_trading_price'] > 1.5)\
                    and (data[highs_indices[i+1]]['average_trading_price']/data[lows_indices[j]]['average_trading_price'] > 1.5) \
                    and data[lows_indices[j]]['average_trading_price'] < data[lows_indices[j+1]]['average_trading_price']\
                    and (highs_indices[i]-highs_indices[i-1] < 4) \
                    and (lows_indices[j]-lows_indices[j-1] < 4):

                list_aux = data[highs_indices[i]:highs_indices[j+2]]
                double_bottoms.append(list_aux)

            i = i+1
            j = j+1

        # pprint(double_bottoms)
        return double_bottoms

    def head_shoulder_detector(self, data):
        lows_indices = self.lows_detector(data)
        highs_indices = self.highs_detector(data)

        # counter
        i = 3  # for highs
        j = 3  # for lows
        head_and_shoulder = []

        while i < len(highs_indices)-1 and j < len(lows_indices)-1:
            if (data[highs_indices[i]]['average_trading_price'] > data[highs_indices[i + 1]]['average_trading_price']) \
                    and (data[highs_indices[i]]['average_trading_price'] > data[highs_indices[i - 1]]['average_trading_price'])\
                    and (highs_indices[i]-highs_indices[i-1] < 4) \
                    and (highs_indices[i-1] - lows_indices[i-1] < 4) \
                    and (0.85 < data[highs_indices[i+1]]['average_trading_price'] / data[highs_indices[i - 1]]['average_trading_price'] < 1.15):

                list_aux = data[lows_indices[j - 2]+1:lows_indices[j+2]-1]
                head_and_shoulder.append(list_aux)
            i = i + 1
            j = j + 1

        return head_and_shoulder


    def rising_wedge_detector(self, data, n):
        lows_indices = self.lows_detector(data)
        highs_indices = self.highs_detector(data)

        for i in range(2, n):
            if data[i]['average_trading_price'] < data[i - 1]['average_trading_price'] < data[i - 2]['average_trading_price']:
                if data[i]['average_trading_price'] < data[i]['average_trading_price'] < data[i - 1]['average_trading_price']:
                    return True
            return False




    def class_launcher(self, collection, window, timeframe):
        #data preparation
        data = self.data_preparation(collection, window)

        #---------------------------------------------------------------------------------
        #calculation
        start = time()
        # double_bottoms = self.double_bottoms_detector(data)
        double_tops = self.double_tops_detector(data)
        # head_and_shoulder = self.head_shoulder_detector(data)
        plotter(data, double_tops)

        #---------------------------------------------------------------------------------
        #code performance
        end = time()
        ex = end - start
        print("------------------------- pattern detection took : ", round(ex, 3), " seconds -------------")
        return 0


dbl_btm = PatternRecognition()
c = dbl_btm.class_launcher('AUROR', 60*12, 24)
