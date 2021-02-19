import numpy as np
import pandas as pd


def create_utc_time_series(start, end, freq):
    date_index = pd.date_range(start, end, tz='UTC', freq=freq)
    random_time_series = pd.DataFrame(date_index, columns=['date'])
    random_time_series['value'] = np.random.randn(len(date_index))
    return random_time_series


def do_simple_eda(time_series):
    print(f'Crated time series of length {len(time_series.index)}')
    print(f'\nTime series head:\n{time_series.head(5)}')
    print(
        f'\nMin value: {time_series["value"].min()}\
        Max value {time_series["value"].max()}'
    )
    print(
        f'\nMean: {time_series["value"].mean()}\
        Median: {time_series["value"].median()}'
    )
    print(
        f'\n1th quantile: {time_series["value"].quantile(0.01)}\
        25th quantile: {time_series["value"].quantile(0.025)}\
        \n75th quantile: {time_series["value"].quantile(0.75)}\
        99th quantile: {time_series["value"].quantile(0.99)}'
    )
    #TODO add interquartile range for outlier detection


def get_min_val():
    pass
    #return time_series["value"].min()





