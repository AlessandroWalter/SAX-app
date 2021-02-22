import numpy as np
from tslearn.generators import random_walks
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
from tslearn.piecewise import PiecewiseAggregateApproximation
from tslearn.piecewise import SymbolicAggregateApproximation


class TimeSeriesManager:

    def __init__(self, n_paa_segments: int, n_sax_symbols: int):
        self.n_paa_segments = None
        self.n_sax_symbols = None
        self.set_n_paa_segments(n_paa_segments)
        self.set_n_sax_symbols(n_sax_symbols)
        self.random_walk_ts = None
        self.scaled_ts = None
        self.paa_ts = None
        self.sax_symbols = None

    def create_paa_ts(self):
        paa = PiecewiseAggregateApproximation(n_segments=self.n_paa_segments)
        self.paa_ts = paa.inverse_transform(paa.fit_transform(self.scaled_ts))

    def create_random_walk_ts(self, n_ts, sz, d, seed):
        max_ts_seed = 9999999
        if seed > max_ts_seed:
            seed = max_ts_seed
        np.random.seed(seed)
        self.random_walk_ts = random_walks(n_ts=n_ts, sz=sz, d=d)

    def create_scaled_ts(self, mu, std):
        scaler = TimeSeriesScalerMeanVariance(mu=mu, std=std)
        self.scaled_ts = scaler.fit_transform(self.random_walk_ts)

    def count_sax_symbols(self):
        sax_symbol_keys = np.arange(0, self.n_sax_symbols)
        counters = np.array([[key, np.sum(self.sax_symbols == key)] for key in sax_symbol_keys])
        return counters

    def generate_sax_symbols(self):
        sax = SymbolicAggregateApproximation(n_segments=self.n_paa_segments,
                                             alphabet_size_avg=self.n_sax_symbols,
                                             scale=True)
        self.sax_symbols = sax.fit_transform(self.scaled_ts)

    def set_n_sax_symbols(self, n_sax_symbols: int):
        if n_sax_symbols < 1:
            raise ValueError('Ints for n_sax_symbols smaller than 1 forbidden')

        max_n_sax_symbols = 99
        if n_sax_symbols > max_n_sax_symbols:
            n_sax_symbols = max_n_sax_symbols
        self.n_sax_symbols = n_sax_symbols

    def set_n_paa_segments(self, n_paa_segments: int):
        if n_paa_segments < 1:
            raise ValueError('Ints for n_paa_segments smaller than 1 forbidden')

        max_n_paa_segments = 99
        if n_paa_segments > max_n_paa_segments:
            n_paa_segments = max_n_paa_segments
        self.n_paa_segments = n_paa_segments




