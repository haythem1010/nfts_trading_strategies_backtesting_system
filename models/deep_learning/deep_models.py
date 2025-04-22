from repository.transactions_stats_repo import TransactionsStatsRepository
from utils.helpers import calculate_expo_ma
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras
from time import time
import torch


class DeepLearning(object):
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
                         "average_listing_price": listing_data[i]["ls_avg_price"],
                         "average_listing_price_change": listing_data[i]["ls_avg_price"],
                         "average_trading_price_change": listing_data[i]["tr_avg_price"]})
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
        return torch.tensor(X), torch.tensor(y)

    def LSTM_model_fitting(self,data, X_train, X_test, y_train, y_test, seq_length):
        num_features = X_train.shape[2]  # Get the number of features from the input data

        model = keras.Sequential([
            keras.layers.LSTM(64, activation='relu', input_shape=(seq_length, num_features)),
            keras.layers.Dense(num_features)
        ])

        model.compile(optimizer='adam', loss='mse')
        model.fit(X_train, y_train, epochs=50, batch_size=32)

        # Evaluate the model on test data
        loss = model.evaluate(X_test, y_test)

        # Make predictions on new unseen data
        new_data = np.array([[...]])  # Your new unseen data with shape (seq_length, num_features)

        # Use the same scaler object used to scale the training data to transform the new data
        scaler = MinMaxScaler()
        X_train_scaled = scaler.fit_transform(X_train.reshape(-1, num_features))
        X_test_scaled = scaler.transform(X_test.reshape(-1, num_features))
        new_data_scaled = scaler.transform(new_data.reshape(-1, num_features))

        X_new, _ = self.create_sequences(new_data_scaled, seq_length)
        predictions = model.predict(X_new)

        # Inverse transform predictions to get original scale
        predictions = scaler.inverse_transform(predictions)
        return predictions

    #---------------------------------------------------------------------------------------------------------------

    def class_launcher(self, collection, window, local_data=False):

        """ data preparation : """

        data = self.data_preparation(collection, window)

        start = time()