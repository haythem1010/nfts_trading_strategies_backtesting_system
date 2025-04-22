from repository.transactions_stats_repo import TransactionsStatsRepository
import json
from utils.helpers import calculate_expo_ma

class LocalData(object):
    tr = TransactionsStatsRepository()

    def data_preparation(self, collection, timeframe):
        trading_data, listing_data = self.tr.class_launcher(collection, timeframe*60)
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

    def data_writing(self, timeframe):
        collections = ["aidegens", "AUROR", "BSL", "BORYOKU", "BGB", "CWM", "CoC", "DAPE", "DEGG", "DFC", "FFF", "FRTS", "GGSG", "GENOPET",
                       "GD", "MIDH", "Nyan", "C3","okay_bears", "PRTL", "PRIM", "QT", "SSC", "SMB", "SAC", "taiyo_robotics", "OMNI", "TAT",
                       "DGOD", "C3L"]

        for i in collections:
            data = self.data_preparation(i, timeframe)
            with open(i, 'w') as json_file:
                json.dump(data, json_file)

    def class_launcher(self, timeframe):
        self.data_writing(timeframe)


save = LocalData()
save.class_launcher(12)