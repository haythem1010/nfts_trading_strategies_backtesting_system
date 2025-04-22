from sklearn.gaussian_process import GaussianProcessRegressor
from prophet import Prophet
from copy import deepcopy
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from sklearn.metrics import mean_squared_error
import json
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.statespace.varmax import VARMAX


class GridSearch(object):
    # Perform grid search on the models
    @staticmethod
    def get_model_instance(endo_train, model_name):
        # Return the model instance based on the model name
        if model_name == "ARIMA":
            return ARIMA(endog=endo_train)
        elif model_name == "SARIMA":
            return SARIMAX(endog=endo_train)
        elif model_name == "GPR":
            return GaussianProcessRegressor(endo_train)
        elif model_name == "Prophet":
            return Prophet(endo_train)
        elif model_name == "VARMAX":
            return VARMAX(endog=endo_train)
        else:
            raise ValueError(f"Unknown model name: {model_name}")

    @staticmethod
    def models_definition(exog_data):

        # Define the parameter grid for each model
        param_grid = [
            {
                'order': [(1, 0, 1)],
                'seasonal_order': [(0, 0, 0, 0)],
                'exog': [None, exog_data],
                'trend': [None, 'c', 't', 'ct']
            },
            {
                'order': [(1, 0, 1)],
                'seasonal_order': [(0, 0, 0, 0)],
                'exog': [None, exog_data],
                'trend': [None, 'c', 't', 'ct']
            },
            {
                'kernel': ['RBF', 'Matern'],
                'alpha': [1e-5, 1e-3, 1e-1]
            },
            {
                'changepoint_prior_scale': [0.01, 0.1, 1.0],
                'seasonality_prior_scale': [0.01, 0.1, 1.0]
            },
            {
                'order': [(1, 1)],
                'trend': ['c', 'ct'],
                'exog': [None, exog_data]
            }
        ]

        return param_grid


    def gridsearch_time_series_models(self, exo_train, endo_train, models, scoring_metric='neg_mean_squared_error', cv_splits=3):
        """
        Perform grid search on multiple time series models.

        Parameters:
        - exo_train: Exogenous variables training data
        - endo_train: Endogenous variable training data
        - models: List of model names or instances
        - param_grid: List of dictionaries specifying the parameter grid for each model
        - scoring_metric: Scoring metric for grid search (default: 'neg_mean_squared_error')
        - cv_splits: Number of cross-validation splits (default: 3)

        Returns:
        - best_models: Dictionary containing the best models for each model name
        - best_params: Dictionary containing the best parameters for each model name
        """
        param_grid = self.models_definition(endo_train)
        tscv = TimeSeriesSplit(n_splits=cv_splits)
        best_models = {}
        best_params = {}

        for model_name, params in zip(models, param_grid):
            estimator = self.get_model_instance(endo_train, model_name)  # Get the model instance based on the model name
            grid_search = GridSearchCV(estimator=estimator, param_grid=params, scoring=scoring_metric, cv=tscv)
            grid_search.fit(exo_train, endo_train)

            best_models[model_name] = grid_search.best_estimator_
            best_params[model_name] = grid_search.best_params_

            print(f"Best parameters for {model_name}: {grid_search.best_params_}")
            print(f"Best score for {model_name}: {-grid_search.best_score_}\n")

        return best_models, best_params