from app.subject import Subject
import numpy as np
from tslearn.generators import random_walks
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
from tslearn.piecewise import PiecewiseAggregateApproximation
from tslearn.piecewise import SymbolicAggregateApproximation


class TimeSeriesManager(Subject):

    def __init__(self, _n_paa_segments, _n_sax_symbols):
        self._n_paa_segments = None
        self._n_sax_symbols = None
        self.set_n_paa_segments(_n_paa_segments)
        self.set_n_sax_symbols(_n_sax_symbols)
        self._base_ts = None
        self._scaled_ts = None
        self._paa_ts = None
        self._sax_symbols = None
        self._observers = []

    def get_n_paa_segments(self):
        return self._n_paa_segments

    def set_n_paa_segments(self, n_paa_segments):
        min_n_paa_segments, max_n_paa_segments = 1, 99
        if (n_paa_segments < min_n_paa_segments) | (n_paa_segments > max_n_paa_segments):
            error_msg = (f'Ints for n_paa_segments smaller than {min_n_paa_segments} or greater than '
                         f' {max_n_paa_segments} forbidden')
            raise ValueError(error_msg)
        self._n_paa_segments = n_paa_segments

    def get_n_sax_symbols(self):
        return self._n_sax_symbols

    def set_n_sax_symbols(self, n_sax_symbols):
        min_n_sax_symbols, max_n_sax_symbols = 1, 99
        if (n_sax_symbols < min_n_sax_symbols) | (n_sax_symbols > max_n_sax_symbols):
            error_msg = (f'Ints for n_sax_symbols smaller than {min_n_sax_symbols} or greater than {max_n_sax_symbols}'
                         f' forbidden')
            raise ValueError(error_msg)
        self._n_sax_symbols = n_sax_symbols

    def set_paa_ts(self, paa_ts):
        self._paa_ts = paa_ts

    def get_paa_ts(self):
        return self._paa_ts

    def get_base_ts(self):
        return self._base_ts

    def set_base_ts(self, ts):
        self._base_ts = ts

    def get_scaled_ts(self):
        return self._scaled_ts

    def set_scaled_ts(self, scaled_ts):
        self._scaled_ts = scaled_ts

    def get_sax_symbols(self):
        return self._sax_symbols

    def attach(self, observer):
        self._observers.append(observer)

    def create_and_update_paa_ts(self, n_paa_segments, scaled_ts):
        paa = PiecewiseAggregateApproximation(n_segments=n_paa_segments)
        self._paa_ts = paa.inverse_transform(paa.fit_transform(scaled_ts))

    @staticmethod
    def create_random_walk_ts(n_ts, size, n_dimensions, seed):
        max_seed = 9999999
        if seed > max_seed:
            raise ValueError(f'Seeds greater than {max_seed} forbidden')
        np.random.seed(seed)
        return random_walks(n_ts=n_ts, sz=size, d=n_dimensions)

    def create_and_update_scaled_ts(self, mu, std, ts):
        scaler = TimeSeriesScalerMeanVariance(mu=mu, std=std)
        self._scaled_ts = scaler.fit_transform(ts)

    def count_sax_symbols(self):
        sax_symbol_keys = np.arange(0, self.get_n_sax_symbols())
        counters = np.array([[key, np.sum(self.get_sax_symbols() == key)] for key in sax_symbol_keys])
        return counters

    def detach(self, observer):
        self._observers.remove(observer)

    def generate_and_update_sax_symbols(self, n_paa_segments, n_sax_symbols, ts):
        sax = SymbolicAggregateApproximation(n_segments=n_paa_segments,
                                             alphabet_size_avg=n_sax_symbols,
                                             scale=True)
        self._sax_symbols = sax.fit_transform(ts)

    def notify(self):
        for observer in self._observers:
            observer.update(self)
