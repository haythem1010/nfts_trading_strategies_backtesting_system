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
from utils.helpers import models_evaluation
from local_data.data_readers import Readers
import pickle
import plotly.graph_objs as go
import plotly.offline as pyo

#-----------------------------------------------------------------------------------------------------------

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

class Analysis(object):
    tr = PatternRecognition()
    rd = Readers()

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
        df_exo = df[['minimum_trading_price', 'maximum_listing_price', 'minimum_listing_price', 'average_trading_price']]
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
    def kpss_analysis(series, value='floor_price'):

        plt.plot(series)
        result = kpss(series)

        # Extract the test statistic and p-value
        test_statistic = result[0]
        p_value = result[1]

        print("-----------------------------------------")
        print('test_statistic = ', test_statistic)
        print('p-value = ', p_value)

        # Compare the p-value to the significance level (e.g., 0.05)
        stationary = False
        if p_value < 0.05:
            print("The time series is likely non-stationary.")

        else:
            print("The time series is likely stationary.")
            stationary = True

        return stationary

    @staticmethod
    def make_serie_stationnary(series):
        series_diff = series.diff().dropna()
        return series_diff

    @staticmethod
    def decompose_series(series, visualization=True):
        # Perform seasonal decomposition
        decomposition = seasonal_decompose(series, model='additive', period=14)

        # Access the decomposed components
        trend = decomposition.trend
        seasonal = decomposition.seasonal
        residuals = decomposition.resid

        if visualization:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(trend, label='Trend')
            ax.plot(seasonal, label='Seasonality')
            ax.plot(residuals, label='Residuals')
            ax.set_xlabel('Time')
            ax.set_ylabel('Component Value')
            ax.set_title('Decomposed Time Series')
            ax.legend()

            # Show the plot
            plt.show()

        return trend, seasonal, residuals

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

#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------

    """ ---- fit the models ---- """
    @staticmethod
    def fit_the_ARIMA_model(data, exo_train, exo_test, endo_train, endo_test, p, d, q, value, residuals_plot=True, visualisation=False):
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
        fig = px.line(data, x='date', y=[value, 'predicted_value'], title='ARIMAX Model Interpretation')
        fig.show()

        # with open('arima_model.pkl', 'wb') as f:
        #     pickle.dump(model_fit, f)
        return 0

    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def fit_the_VARMAX_model(data, exo_train, exo_test, endo_train, endo_test, p, q, value, residuals_plot=True):
        model = VARMAX(endo_train, exog=exo_train, order=(p, q))
        model_fit = model.fit()
        print(model_fit.summary())

        residuals = model_fit.resid[1:]
        if residuals_plot:
            fig, ax = plt.subplots(1, 2)
            residuals.plot(title='Residuals', ax=ax[0])
            residuals.plot(title='Density', kind='kde', ax=ax[1])
            plot_acf(residuals)
            plot_pacf(residuals)

        forecast_test = model_fit.forecast(steps=len(endo_test), exog=exo_test)
        # Create a new DataFrame with the forecasted values
        predicted_values = pd.DataFrame(forecast_test, columns=endo_test.columns, index=endo_test.index)

        # Concatenate the original data and the predicted values DataFrame
        predicted_data = pd.concat([endo_train, predicted_values], axis=0)

        data = pd.DataFrame(data)
        data['predicted_floor_price'] = predicted_data['floor_price']
        data['predicted_average_trading_price'] = predicted_data['average_trading_price']
        data_to_plot = data['predicted_floor_price'].tail(len(endo_test))
        print(type(predicted_data))
        # data.plot(x='date', y=[value[0], data_to_plot])
        plt.plot(data['date'], data[value[1]], label=value[1])
        plt.plot(data_to_plot, label='predicted_floor_price')
        plt.legend()
        plt.show()
        return 0


    @staticmethod
    def auto_fitting_arima_model(train_set):
        auto_arima = pm.auto_arima(train_set, stepwise=False, seasonal=False)
        print(auto_arima)
        print(auto_arima.summary())


    def fit_PROPHET_model(self, data, to_predict='average_trading_price', visualization=False):
        df = pd.DataFrame(data)
        df.rename(columns={'date': 'ds', to_predict: 'y'}, inplace=True)
        df['ds'] = pd.to_datetime(df['ds'])
        df1, stationarity = self.augmented_Dickey_Fuller(df['y'], window=7, visualization=False)
        df1_copy = df1.to_frame(name='y')

        print("*****************  How many times we performed differencing ! ************** ")
        d = 0
        while not stationarity:
            d = d+1
            df1_copy['y'] = df1_copy['y'].diff().dropna()
            df1_copy['y'].fillna(0, inplace=True)
            df1_copy, stationarity = self.augmented_Dickey_Fuller(df1_copy['y'], window=7, visualization=False)

        print("------------- d = ", d, "-------------")

        df.rename(columns={'y': 'diff'}, inplace=True)
        df = df.drop('diff', axis=1)
        concatenated = pd.concat([df, df1_copy], axis=1)

        train, test = self.splitting_dataframe_to_train(concatenated, index_is_time=True, shuffle=False)
        model = Prophet()
        model.fit(train)
        forcast = model.predict(test)

        i = 1
        if d != 0:
            while i <= d:
                train['diff'] = df1
                test['diff'] = df1
                # forcast['yhat'] = forcast['yhat'].rolling(window=2).sum()
                i = i+1
        print("ARIMAX Model Interpretation : ")
        models_evaluation(test, forcast)
        if visualization:
            if d == 0:
                #Plot training data
                plt.plot(train['ds'], train['y'], label='Training Data')
                plt.plot(test['ds'], test['y'], label='Actual Data')
            else:
                plt.plot(test['ds'], test['diff'], label='Actual Data')
                plt.plot(train['ds'], train['diff'], label='Training Data')

            # Plot predicted values
            plt.plot(forcast['ds'], forcast['yhat'], label='Predicted Values')

            # Customize the plot
            plt.xlabel('Time')
            plt.ylabel(to_predict)
            plt.title('Actual vs. Predicted Values')
            plt.legend()

            # Show the plot
            plt.show()


        return 0


    def fit_the_GPR_model(self, data, visualization=False, to_predict='floor_price'):
        df = pd.DataFrame(data)
        train, test = self.splitting_dataframe_to_train(df, index_is_time=True, shuffle=False)
        # feature_cols = ['average_listing_price','average_trading_price', 'minimum_trading_price',
        #                   'listed_elements','maximum_listing_price','maximum_trading_price',
        #                   'minimum_listing_price', 'trading_price_moving_average',
        #                   'transaction_count']

        # feature_cols = ['minimum_trading_price', 'floor_price', 'maximum_listing_price', 'maximum_trading_price', 'minimum_listing_price']
        feature_cols = ['minimum_trading_price', 'maximum_listing_price', 'average_trading_price']

        exo_train = train[feature_cols].values.reshape(-1, len(feature_cols))
        endo_train = train[to_predict].values.reshape(-1, 1)


        exo_test = test[feature_cols].values.reshape(-1, len(feature_cols))
        endo_test = test[to_predict].values.reshape(-1, 1)

        #Kernels determinations :
        kernels = [
            RBF(length_scale=0.1),
            Matern(length_scale=0.1, nu=1.5),
            RationalQuadratic(length_scale=2.0, alpha=0.0)
        ]

        # Create and fit the Gaussian Process Regression model
        gpr = gp.GaussianProcessRegressor(kernel=RBF(length_scale=10), alpha=1, normalize_y=True)
        # gpr = gp.GaussianProcessRegressor(normalize_y=False)
        gpr.fit(exo_train, endo_train)

        # Make predictions
        endo_prediction = gpr.predict(exo_test)

        print("GPR model interpretation : ")
        models_evaluation(endo_test, endo_prediction)

        if visualization:
            # Plot actual and predicted floor prices
            # plt.plot(train['date'], endo_test, label='Historical Data')
            plt.plot(test['date'], endo_test, label='Actual Data')
            plt.plot(test['date'], endo_prediction, label='Predicted Values')
            plt.xlabel('Date')
            plt.ylabel(to_predict)
            plt.title('Actual vs. Predicted ')
            plt.legend()
            plt.show()

        return 0
    #----------------------------------------------------------------------------------------------------

    def class_launcher(self, collection, window, timeframe, to_predict, local_data=False):

        """ data preparation : """
        if not local_data:
            data = self.tr.data_preparation(collection, window)
        else:
            data = self.rd.local_data_readers(collection, timeframe)

        start = time()
        # pprint(type(data[0]['date']))
        """ endogenous data + exogenous data  """
        exogenous, endogenous = self.endo_exo_variables(data, to_predict)

        """ stationarity tests : """
        series, stationary = self.augmented_Dickey_Fuller(endogenous, 14, visualization=False)
        # self.kpss_analysis(data, to_predict)

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
        self.fit_the_ARIMA_model(data, exo_train=exo_train, exo_test=exo_test, endo_train=endo_train, endo_test=endo_test, p=5, d=d, q=14, value=to_predict, residuals_plot=False, visualisation=False)

        """ Fitting the VARMAX model : """
        # self.fit_the_VARMAX_model(data, exo_train=exo_train, exo_test=exo_test, endo_train=endo_train, endo_test=endo_test, p=4, q=1, value=['average_trading_price', 'floor_price'], residuals_plot=False)

        """ Fitting the Prophet Model"""
        # self.fit_PROPHET_model(data, 'floor_price', visualization=True)

        """  Fitting the GPR model : """
        self.fit_the_GPR_model(data, visualization=True, to_predict=to_predict)

        """ Perform grid search on the models : """
        """ Define the models to include in the grid search : """
        # models = ["ARIMA", "SARIMA", "GPR", "Prophet", "VARMAX"]
        # best_models, best_params = self.gridsearch_time_series_models(endo_train=endo_train, exo_train=exo_train, models=models)


        end = time()
        ex = end - start
        print("******                  **********               **********            *********")
        print(" Execution Time is : ", ex, "seconds")
#----------------------------------------------------------------------------------------------------

analysis = Analysis()
analysis.class_launcher('DGOD', 60 * 12, 24, local_data=True, to_predict='average_trading_price')