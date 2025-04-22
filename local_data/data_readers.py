import json
from pprint import pprint


class Readers(object):
    @staticmethod
    def local_data_readers(collection, timeframe):
        path = f"C:/Users/hayth/Desktop/suipa/suipa-trading-backtester/local_data/{str(timeframe)}h_saving/{collection}"
        with open(path, "r") as json_file:
            data = json.load(json_file)
        print(collection)
        # pprint(data)
        print('----- DONE ----')
        return data

# read = Readers()
# read.local_data_readers('DGOD', 6)