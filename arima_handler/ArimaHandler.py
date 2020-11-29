import itertools
import math
import warnings

import pandas as pd

from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima_model import ARIMA, ARIMAResults


class ArimaHandler(object):

    def __init__(self):
        pass


    @staticmethod
    def biased_rounding(avg_value):
        """Round floats using biased rounding instead of 3.x bankers rounding.

        :param avg_value: float output from averaging
        :return: a rounded int
        """
        if float(avg_value) % 1 >= 0.5:
            return math.ceil(avg_value)
        else:
            return math.floor(avg_value)


    def is_stationary(self, series, window=5, cutoff=0.01):
        """Determine likelihood of series stationarity (required for ARIMA).

        :param series: series to test for stationarity
        :param window: integer value representing size of rolling mean/std window
        :param cutoff: float value indicating significance threshold for p-value
        :return: boolean indicating stationarity
        """
        rolling_mean = series.rolling(window).mean()
        rolling_std = series.rolling(window).std()

        df_test = adfuller(series, autolag='AIC', maxlag=20)
        p_value = df_test[1]

        return p_value < cutoff


    def optimize_params(self, series, n):
        """Find optimal ARIMA parameters (p, d, q) via grid search.

        :param segment: pandas.Series object
        :param n: integer representing upper bound of grid search range
        :return: optimal values for p, d, q such that AIC is minimized
        """
        p = d = q = range(0, n)
        pdq = list(itertools.product(p, d, q))
        aic = {}

        for param in pdq:
            try:
                model = ARIMA(series, order=param)
                model_fit = model.fit()
                aic[model_fit.aic] = param
            except Exception:
                continue

        sorted_aic = sorted(aic)
        return aic, sorted_aic


    def forecast(self, actual, params):
        """ARIMA modeling to fit and forecast data.

        :param actual: training data the model will use to make predictions
        :param params: ARIMA model parameters (tuple)
        :return: rounded single prediction for next value in series
        """
        model = ARIMA(actual, order=params)
        model_fit = model.fit()
        single_prediction = model_fit.forecast()[0][0]

        return biased_rounding(single_prediction)
