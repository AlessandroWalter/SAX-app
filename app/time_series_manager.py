import numpy as np
import pandas as pd
from tslearn.generators import random_walks
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
from tslearn.piecewise import PiecewiseAggregateApproximation
from tslearn.piecewise import SymbolicAggregateApproximation


class TimeSeriesManager:

    def __init__(self, n_ts, size, n_dimensions, n_paa_segments):
        self.n_paa_segments = n_paa_segments
        self.ts = None
        self.scaled_ts = None
        self.paa_ts = None
        self.sax_symbols = None
        self.create_random_walk_ts(n_ts, size, n_dimensions)

    def create_paa_ts(self, n_paa_segments):
        paa = PiecewiseAggregateApproximation(n_segments=n_paa_segments)
        self.paa_ts = paa.inverse_transform(paa.fit_transform(self.scaled_ts))

    def create_random_walk_ts(self, n_ts, sz, d):
        np.random.seed(11)
        self.ts = random_walks(n_ts=n_ts, sz=sz, d=d)

    def create_scaled_ts(self, mu, std):
        scaler = TimeSeriesScalerMeanVariance(mu=mu, std=std)
        self.scaled_ts= scaler.fit_transform(self.ts)

    def create_utc_ts(self, start, end, freq):
        date_index = pd.date_range(start, end, tz='UTC', freq=freq)
        self.ts = pd.DataFrame(date_index, columns=['date'])
        self.ts['value'] = np.random.randn(len(date_index))

    def do_simple_eda(self):
        print(f'Crated time series of length {len(self.ts.index)}')
        print(f'\nTime series head:\n{self.ts.head(5)}')
        print(
            f'\nMin value: {self.ts["value"].min()}\
            Max value {self.ts["value"].max()}'
        )
        print(
            f'\nMean: {self.ts["value"].mean()}\
            Median: {self.ts["value"].median()}'
        )
        print(
            f'\n1th quantile: {self.ts["value"].quantile(0.01)}\
            25th quantile: {self.ts["value"].quantile(0.025)}\
            \n75th quantile: {self.ts["value"].quantile(0.75)}\
            99th quantile: {self.ts["value"].quantile(0.99)}'
        )

    def generate_sax_symbols(self, n_sax_symbols):
        sax = SymbolicAggregateApproximation(n_segments=self.n_paa_segments,
                                             alphabet_size_avg=n_sax_symbols,
                                             scale=True)
        # self.sax_ts = sax.inverse_transform(sax.fit_transform(self.ts))
        self.sax_symbols = sax.fit_transform(self.ts)

    def get_min_val(self):
        return self.ts["value"].min()

    def get_max_val(self):
        return self.ts["value"].max()

    def set_n_paa_segments(self, n_paa_segments):
        self.n_paa_segments = n_paa_segments





