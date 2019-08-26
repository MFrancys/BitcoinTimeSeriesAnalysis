import pandas as pd
import numpy as np
from scipy.stats import iqr # Compute the interquartile range of the data along the specified axis

###Import package used to get features timeseries
from statsmodels.tsa.stattools import adfuller, kpss

###Identify days with outliers
def get_outlier(x, lower_bound, upper_bound):
    if x < lower_bound or x > upper_bound:
        return int(1)
    else:
        return np.nan

def identify_outliers(df, TARGET, threshold_outlier=1.5):
    q1, q3= np.percentile(df[TARGET], [25, 75])
    IQR = iqr(df[TARGET])
    lower_bound = q1 - (threshold_outlier * IQR)
    upper_bound = q3 + (threshold_outlier * IQR)
    serie_outlier = df[TARGET].apply(lambda x: get_outlier(x, lower_bound, upper_bound))
    return serie_outlier

def test_stationary(df, TARGET):
  # ADF Test
  result = adfuller(df[TARGET], autolag='AIC')
  print("Test stationary")
  print(f'ADF Statistic: {result[0]}')
  print(f'p-value: {result[1]}')
  for key, value in result[4].items():
      print('Critial Values:')
      print(f'   {key}, {value}')
  if result[1] > 0.01:
    return df[TARGET].diff(), result[1]
  else:
    return df[TARGET], result[1]
