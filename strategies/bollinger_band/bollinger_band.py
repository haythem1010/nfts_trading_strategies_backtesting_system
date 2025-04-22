from pprint import pprint
import numpy as np
from importers.collections_importers import CollectionsByAPI
from local_data.data_readers import Readers



class BollingerBand(object):
    col = CollectionsByAPI()
    rd = Readers()

    @staticmethod
    def calculate_sma(data, key, window):
        """

        :param key: key of the specific numeric data t ocalculate
        :param data: trading data and listing data combined in one list of dictionaries
        :param window: window that used to calculate the moving average price
        :return: appending a new (key : moving average,value: moving average) in the entry data
        """
        mvg_avrg = []
        tr_avg_price = [d[key] for d in data]
        for i in range(window, len(tr_avg_price)):
            sma = sum(tr_avg_price[i-window:i]) / window
            mvg_avrg.append({"date": data[i]['date'], "trading_price": data[i]['average_trading_price'], "mvg_average": sma})

        return mvg_avrg

    @staticmethod
    def standard_deviation(data, key):
        """
        :param data: trading data and listing data combined in one list of dictionaries
        :param key: key of the specific numeric data to calculate
        :return: standard deviation
        """

        values = [d[key] for d in data]
        stddev = np.std(values)
        return stddev



    def lower_upper_band(self, collection, window, timeframe):
        """

        :param timeframe:
        :param collection:
        :param window:
        :return:
        """
        #------------------------ data initialization
        # days = 1
        # collection = "DGOD"
        # window = 7
        #-------------------------

        # listing = self.col.get_listing_data_stats_available(collection, days*1440)
        # data = self.col.trading_data_correction(collection, days, listing)
        data = self.rd.local_data_readers(collection, timeframe)
        # pprint(data)
        mvg_average_trading_data = self.calculate_sma(data, 'average_trading_price', window)

        for i in range(window, len(mvg_average_trading_data)):
            data = mvg_average_trading_data[i-window:i]
            stddev = self.standard_deviation(data, 'mvg_average')
            mvg_average_trading_data[i]["lower_band"] = mvg_average_trading_data[i]["mvg_average"] - 2 * stddev
            mvg_average_trading_data[i]["upper_band"] = mvg_average_trading_data[i]["mvg_average"] + 2 * stddev

        mvg_average_trading_data = mvg_average_trading_data[window:]
        return mvg_average_trading_data




