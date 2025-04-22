from pprint import pprint

from importers.collections_importers import CollectionsByAPI
from utils.helpers import convert_timestamp_to_date, create_time_range

import time as t



class BacktestingVONE(object):
    col = CollectionsByAPI()


    @staticmethod
    def backtesting_v1():
        start_ex = t.time()
        list_of_names = CollectionsByAPI().check_stats(1440)
        example = list_of_names[1]
        print(example)
        data = CollectionsByAPI().get_transactions_stats_available(example, 1440)

        for x in data:
            x["date"] = convert_timestamp_to_date(x["date"], '%Y-%m-%d %H:%M:%S')

        start = data[1]["date"]
        end = data[len(data)-1]["date"]
        time_range = create_time_range(start, end, 1440)

        time_strings = [time.strftime('%Y-%m-%d') for time in time_range]

        end = t.time()
        execution = start_ex - end
        print("excecution time = ", execution)

        return list_of_names, time_strings

my_data = BacktestingVONE()
list_of_collections = my_data.backtesting_v1()