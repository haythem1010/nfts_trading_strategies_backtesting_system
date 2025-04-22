from repository.transactions_stats_repo import TransactionsStatsRepository
from utils.helpers import  calculate_expo_ma
import numpy as np


class PatternRecognition(object):
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
    def splitting_dataframe_to_train(df, index_is_time=True, shuffle=False):
        if not index_is_time:
            df.reset_index(inplace=True)
            df.rename(columns={'index': 'date', '0': 'floor_price'}, inplace=True)
            df = df.drop('date', axis=1)

        if shuffle:
            df = df.sample(frac=1, random_state=42)

        split_index = int(0.8 * len(df))
        train_data = df.iloc[:split_index]  # Take the first 80% of rows as training data
        test_data = df.iloc[split_index:]  # The rest of the data is for testing the model

        return train_data, test_data

    @staticmethod
    def create_sequences(data, seq_length):
        X, y = [], []
        for i in range(len(data) - seq_length):
            X.append(data[i:i + seq_length])
            y.append(data[i + seq_length])
        return np.array(X), np.array(y)

