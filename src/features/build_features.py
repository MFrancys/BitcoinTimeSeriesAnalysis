### Import basic packages
import pandas as pd
import os
from datetime import datetime as dt
from datetime import timedelta

###Import package used to get features timeseries
#tsfresh is a python package. It automatically calculates a large number of time series characteristics, the so called features.
#Further the package contains methods to evaluate the explaining power and importance of such characteristics for regression or classification tasks.

from tsfresh.utilities.dataframe_functions import roll_time_series
from tsfresh import extract_features
from tsfresh.feature_extraction import MinimalFCParameters

from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

def get_resample_features(data, window, settings=MinimalFCParameters()):
    """ Make rolling in time series to extrated daily features

    Given that time series that is taken as input must be in hours, the
    number of windows to make the rolling and in this way get daily features

    Parameters
    ----------
    data : DataFrame
        The DataFrame contains events update by CI
    settings : Object
        A object that maps feature calculator names in tsfresh. There are
        two options: ComprehensiveFCParameters() or MinimalFCParameters()
    list_features: list
        A list that contains the relevant features to calculate in tsfresh
    time_resample:
        Unit of time in which the features are required

    Returns
    -------
    DataFrame
        DataFrame with daily features
    """

    data["id"] = 1
    df_roll_time = roll_time_series(
                                    data,
                                    column_id="id",
                                    column_sort='Timestamp',
                                    column_kind=None,
                                    rolling_direction=1,
#                                    max_timeshift=23,
                                    max_timeshift=window
                                    )

    X_features = extract_features(df_roll_time,
                                  column_id="id",
                                  column_sort='Timestamp',
                                  default_fc_parameters=settings,
  #                                n_jobs=4
                                 )
    #resample time series by day
    X_features.index = pd.to_datetime(X_features.index)
    return X_features

def get_features_lag(df, lag=1):
	"""Get the time series lag

	Parameters
	----------
	df : dataframe
		DataFrame with the time series to lag
	lag : int
		Number of times the series will lag behind

	Returns
	-------
		df_lag
			A DataFrame whit the lags of time series
	"""

	df_lag = df.shift(lag)
	df_lag.columns = ["{}_lag_{}".format(column, lag) for column in df_lag.columns]
	return df_lag

def extraction_features_ts(df, window, settings, TARGET, list_features):

	"""Feature extraction with tsfresh package

	Parameters
	----------
	df : dataframe
		DataFrame with the time series to extraction time
	window : int
		Number of windows to calculate features
	settings : str
	TARGET : str
	list_features : list

	Returns
	-------
		df_lag
			A DataFrame whit feature extraction
	"""

	df_features = df.filter(list_features)

	df_features = get_resample_features(df_features, window, settings). \
	  drop(columns=["{}__length".format(TARGET), "{}__sum_values".format(TARGET)])

	df = df.set_index("Timestamp")

	df_features = pd.concat([df_features, df[TARGET]], axis=1)

	###Get lag 1
	df_features_lag = pd.concat([get_features_lag(df_features, lag=1), df_features[TARGET]], axis=1).dropna()
	###Get lag 2
	df_features_lag = pd.concat([get_features_lag(df_features, lag=2), df_features_lag], axis=1).dropna()

	return df_features_lag
