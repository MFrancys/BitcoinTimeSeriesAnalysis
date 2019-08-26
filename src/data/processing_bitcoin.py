import os
import pandas as pd
import numpy as np

def get_data_bitcoin(file):
    ###Get data Bitcoin in minutes

    df_bitcoin= pd.read_csv(os.path.join(file))
    df_bitcoin["Timestamp"] = pd.to_datetime(df_bitcoin["Timestamp"], unit="s")
    df_bitcoin = df_bitcoin.set_index("Timestamp").dropna()
    df_bitcoin = df_bitcoin.resample("1T").last()

    return df_bitcoin

def resample_bitcoin_hour(df_bitcoin, ohlc_dict):
    #Resample data bitcoin in minute by hour

    data_bitcoin_resample = df_bitcoin.resample(rule="1H", how=ohlc_dict)
    INIT_DATE_ANALYSIS = "2019-01-01 00:00:00"
    data_bitcoin_resample = data_bitcoin_resample.loc[INIT_DATE_ANALYSIS:, :]

    data_bitcoin_resample = data_bitcoin_resample.reset_index()
    data_bitcoin_resample = data_bitcoin_resample.assign(
        date=data_bitcoin_resample["Timestamp"].dt.date,
        dayofweek=data_bitcoin_resample["Timestamp"].dt.dayofweek,
        month=data_bitcoin_resample["Timestamp"].dt.month,
        week=data_bitcoin_resample["Timestamp"].dt.week,
        hour=data_bitcoin_resample["Timestamp"].dt.hour
    )
    return data_bitcoin_resample

def main(file_coinbase, file_bitstamp, TARGET, INIT_DATE_ANALYSIS, LAST_DATE_UPDATE):
    ohlc_dict = {
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume_(Currency)": "sum"
    }

    ###Get data Bitcoin in minutes
    data_coinbase = get_data_bitcoin(file_coinbase)
    data_bitstamp = get_data_bitcoin(file_bitstamp)

    ###Replace nans in data_bitstamp with data_coinbase values
    data_bitcoin = data_bitstamp.combine_first(data_coinbase).loc["2016-01-01 00:00:00":]

    #Resample data bitcoin in minute by hour
    data_bitcoin_resample = resample_bitcoin_hour(data_bitcoin, ohlc_dict)
    data_bitcoin_resample.to_csv(os.path.join(ROOT_PATH, f"data\\ts_bitcoin_{INIT_DATE_ANALYSIS}_{LAST_DATE_UPDATE}.csv"))

    print("Data Shape: {}".format(data_bitcoin_resample.shape[0]))
    print("Number of null: {}".format(data_bitcoin_resample[data_bitcoin_resample["Open"].isnull()].shape[0]))
    print(data_bitcoin_resample[data_bitcoin_resample["Open"].isnull()])
    print(data_bitcoin_resample.head(15))

if __name__ == "__main__":
    ROOT_PATH = os.path.dirname(os.path.dirname(os.getcwd()))
    TARGET = "Close"

    ###Get data Bitcoin in minutes
    file_coinbase = os.path.join(ROOT_PATH, "data\\coinbase_2014_12_01_to_2019_01_09.csv")
    file_bitstamp = os.path.join(ROOT_PATH, "data\\bitstamp_2012_01_01_to_2019_03_13.csv")

    ###Select the data to analysis
    INIT_DATE_ANALYSIS = "2019-01-01"
    LAST_DATE_UPDATE = "2019-03-13"

    main(file_coinbase, file_bitstamp, TARGET, INIT_DATE_ANALYSIS, LAST_DATE_UPDATE)
