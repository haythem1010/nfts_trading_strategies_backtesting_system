import json
from pprint import pprint
from time import time
from models.times_series.data_processing import PatternRecognition
import pandas as pd
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import plotly.graph_objs as go
import plotly.express as px
import sklearn.gaussian_process as gp
import matplotlib.pyplot as plt
import pmdarima as pm
from statsmodels.tsa.statespace.varmax import VARMAX
from prophet import Prophet
from sklearn.gaussian_process.kernels import RBF, Matern, RationalQuadratic, ExpSineSquared
from prettytable import PrettyTable
from plotly.offline import plot
from utils.helpers import models_evaluation
from local_data.data_readers import Readers
import pickle


"""'    'average_listing_price',
        'average_trading_price',
        'date',
        'floor_price',
        'listed_elements',
        'maximum_listing_price',
        'maximum_trading_price',
        'minimum_listing_price',
        'minimum_trading_price',
        'trading_price_moving_average',
        'transaction_count'
        ['average_trading_price','floor_price']"""

class Mymodel(object):
    tr = PatternRecognition()
    rd = Readers()

    @staticmethod
    def make_serie_stationnary(series):
        series_diff = series.diff().dropna()
        return series_diff

    @staticmethod
    def read_local_data(collection):
        path_to_file = f"C:/Users/hayth/Desktop/-/Stages/suipa-NFTs-trading-strategies_backtesting/local_data/{collection}.json"
        with open(path_to_file, 'r') as file:
            data = json.load(file)
        return data

    @staticmethod
    def endo_exo_variables(data, value):
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        # df.set_index('date', inplace=True)
        if value == 'floor_price':
            df_exo = df[['minimum_trading_price', 'average_listing_price', 'average_trading_price']]
        else:
            df_exo = df[['minimum_trading_price', 'maximum_listing_price', 'minimum_listing_price', 'floor_price']]

        df_endo = df[value]
        # df_endo = df['average_trading_price']

        return df_exo, df_endo

    @staticmethod
    def augmented_Dickey_Fuller(series, window, visualization=False):

        print(series.describe())

        if visualization:
            # Visualize the time series
            plt.plot(series)
            plt.title('Time Series Data')
            plt.show()

        # Calculate summary statistics
        mean = series.mean()
        variance = series.var()
        print('Mean:', mean)
        print('Variance:', variance)

        # Calculate rolling statistics
        rolling_mean = series.rolling(window=window).mean()
        rolling_variance = series.rolling(window=window).var()
        # pprint(rolling_variance)
        # pprint(rolling_mean)

        if visualization:
            # Plot rolling statistics
            plt.plot(series, label='Original')
            plt.plot(rolling_mean, label='Rolling Mean')
            plt.plot(rolling_variance, label='Rolling Variance')
            plt.title('Rolling Statistics')
            plt.legend()
            plt.show()

        # Perform the ADF test
        result = adfuller(series)

        # Extract the test statistics and p-value
        test_statistic = result[0]
        p_value = result[1]

        print("-----------------------------------------")
        print('test_statistic = ', test_statistic)
        print('p-value = ', p_value)

        stationary = True
        # Compare the p-value to the significance level (e.g., 0.05)
        if p_value < 0.05:
            print("The time series is likely stationary.")
        else:
            print("The time series is likely non-stationary.")
            stationary = False

        return series, stationary

    @staticmethod
    def autocorrelation_analysis(series, visualization=True, plot=True):
        # Convert Series to numpy array
        data = series.values
        if plot:
            # Calculate ACF and PACF
            acf_values = acf(data, nlags=30)
            pacf_values = pacf(data, nlags=30)

            # Print ACF values
            print("ACF:")
            for lag, acf_val in enumerate(acf_values[:25]):
                print(f"Lag {lag + 1}: {acf_val}")

            # Print PACF values
            print("PACF:")
            for lag, pacf_val in enumerate(pacf_values[:25]):
                print(f"Lag {lag + 1}: {pacf_val}")

        if visualization:
            # Plot Autocorrelation Function (ACF)
            fig, ax = plt.subplots(figsize=(10, 6))
            plot_acf(series, ax=ax, lags=30)  # Adjust the number of lags as needed
            plt.xlabel('Lag')
            plt.ylabel('Autocorrelation')
            plt.title('Autocorrelation Plot (ACF)')
            plt.show()

            # Plot Partial Autocorrelation Function (PACF)
            fig, ax = plt.subplots(figsize=(10, 6))
            plot_pacf(series, ax=ax, lags=30)  # Adjust the number of lags as needed
            plt.xlabel('Lag')
            plt.ylabel('Partial Autocorrelation')
            plt.title('Partial Autocorrelation Plot (PACF)')
            plt.show()

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

    # ------------------------------------------------------------------------------------------------------------------

    """ ---- fit the models ---- """

    @staticmethod
    def fit_the_ARIMA_model(data, exo_train, exo_test, endo_train, endo_test, p, d, q, to_predicit, residuals_plot=True,visualisation=False):
        model = ARIMA(endo_train, exog=exo_train, order=(p, d, q))
        model_fit = model.fit()
        print(model_fit.summary())

        residuals = model_fit.resid[1:]
        if residuals_plot:
            fig, ax = plt.subplots(1, 2)
            residuals.plot(title='Residuals', ax=ax[0])
            residuals.plot(title='Density', kind='kde', ax=ax[1])
            plot_acf(residuals)
            plot_pacf(residuals)

        forecast_test = model_fit.forecast(len(endo_test), exog=exo_test)
        predicted_values = pd.Series([None] * len(endo_train) + list(forecast_test), index=range(len(data)))

        print("ARIMAX Model Interpretation : ")
        models_evaluation(endo_test, forecast_test)

        data = pd.DataFrame(data)
        data['predicted_value'] = predicted_values
        fig = px.line(data, x='date', y=[to_predicit, 'predicted_value'], title='ARIMAX Model Interpretation')


        with open('arimax_model.pkl', 'wb') as f:
            pickle.dump(model_fit, f)
        return  fig





    #----------------------------------------------------------------------------------------------------

    def class_launcher(self, collection, window, timeframe, local_data=False, to_predict='average_trading_price'):

        """ data preparation : """
        if not local_data:
            data = self.tr.data_preparation(collection, window)
        else:
            data = self.rd.local_data_readers(collection, timeframe)

        start = time()
        # pprint(data)
        exogenous, endogenous = self.endo_exo_variables(data, to_predict)

        """ stationarity tests : """
        series, stationary = self.augmented_Dickey_Fuller(endogenous, 14, visualization=False)
        # self.kpss_analysis(data, 'trading_price_moving_average')

        """ Splitting the data : """
        endo_train, endo_test = self.splitting_dataframe_to_train(endogenous, index_is_time=True, shuffle=False)
        exo_train, exo_test = self.splitting_dataframe_to_train(exogenous, index_is_time=True, shuffle=False)

        """ Auto Fitting the model """
        # self.auto_fitting_arima_model(endo_train)

        """ Make the serie stationnary by integrating """
        endogenous_copy = endogenous.copy()
        d = 0
        while not stationary:
            d = d + 1
            endogenous_copy = self.make_serie_stationnary(endogenous_copy)
            endogenous_copy, stationary = self.augmented_Dickey_Fuller(endogenous_copy, 14, visualization=False)

        print(" *-*-*-*-* d = ", d)


        """ decomposition of the time series : """
        # trend, season, residuals = self.decompose_series(endogenous, visualization=False)

        """ AUTOCORRELATION : """
        # self.autocorrelation_analysis(endogenous, visualization=True, plot=False)


        """ Fitting the ARIMAX model : """
        fig = self.fit_the_ARIMA_model(data, exo_train=exo_train, exo_test=exo_test, endo_train=endo_train, endo_test=endo_test, p=5, d=d, q=2,to_predicit=to_predict, residuals_plot=False, visualisation=False)
        plot(fig)

        end = time()
        ex = end - start
        print("------------------------------------------------------------------------------------")
        print(" Execution Time is : ", ex, "seconds")
        return fig
    # ----------------------------------------------------------------------------------------------------
    def predict_the_future_with_loaded_model(self,collection, timeframe, local_data=True, to_predict='floor_price'):
        data = []
        with open('arimax_model.pkl', 'rb') as f:
            loaded_model_fit = pickle.load(f)

        if local_data:
            data = self.rd.local_data_readers(collection, timeframe)

        exogenous, endogenous = self.endo_exo_variables(data, to_predict)
        endo_train, endo_test = self.splitting_dataframe_to_train(endogenous, index_is_time=True, shuffle=False)
        exo_train, exo_test = self.splitting_dataframe_to_train(exogenous, index_is_time=True, shuffle=False)

        new_df = pd.DataFrame(data)
        pred = loaded_model_fit.forecast(steps=len(exo_test), exog=exo_test)

        pprint(new_df['floor_price'][304:311])
        pprint(pred)

        data['predicted_value'] = pred
        fig = px.line(new_df, x='date', y=['floor_price', 'predicted_value'], title='ARIMAX Model Interpretation')
        fig.show()

        # ----------------------------------------------------------------------------------------------------
#
# analysis = Mymodel()
# analysis.class_launcher('DGOD', 60 * 12, 24, local_data=True, to_predict='average_trading_price')
# analysis.predict_the_future_with_loaded_model('AUROR', 24, local_data=True)