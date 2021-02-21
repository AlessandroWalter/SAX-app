# exec in terminal: python -m pytest tests

from app import time_series_manager
import numpy as np
import pytest

tm = time_series_manager.TimeSeriesManager(8, 3)
random_walk_seed = 12


def test_count_sax_symbols_counts_correctly():
    tm.create_random_walk_ts(1, 100, 1, random_walk_seed)
    tm.create_scaled_ts(0, 1)
    tm.set_n_paa_segments(1)
    tm.set_n_sax_symbols(1)
    tm.create_paa_ts()
    tm.generate_sax_symbols()
    counters = tm.count_sax_symbols()
    np.testing.assert_array_equal(counters[:, 1], np.array([1]))

    tm.set_n_paa_segments(2)
    tm.set_n_sax_symbols(2)
    tm.create_paa_ts()
    tm.generate_sax_symbols()
    counters = tm.count_sax_symbols()
    np.testing.assert_array_equal(counters[:, 1], np.array([1, 1]))


def test_create_random_walk_ts_has_correct_length():
    expected_df_length = 878
    tm.create_random_walk_ts(1, expected_df_length, 1, random_walk_seed)
    assert tm.random_walk_ts.size == expected_df_length


def test_create_random_walk_has_no_nan():
    tm.create_random_walk_ts(1, 100, 1, random_walk_seed)
    assert np.count_nonzero(np.isnan(tm.random_walk_ts)) == 0


def test_create_random_walk_ts_none():
    tm.random_walk_ts = None
    tm.create_random_walk_ts(1, 100, 1, random_walk_seed)
    assert tm.random_walk_ts is not None


def test_create_scaled_ts_has_close_to_0_mean():
    tolerance = 0.001
    tm.create_random_walk_ts(1, 250, 1, random_walk_seed)
    tm.create_scaled_ts(0, 1)
    scaled_mean = tm.scaled_ts.mean()
    if scaled_mean < 0:
        assert scaled_mean > -tolerance
    else:
        assert scaled_mean > tolerance


def test_create_paa_ts_not_none():
    tm.paa_ts = None
    tm.create_paa_ts()
    assert tm.paa_ts is not None


def test_init_throws_value_error():
    with pytest.raises(ValueError):
        time_series_manager.TimeSeriesManager(-1, 1)
    with pytest.raises(ValueError):
        time_series_manager.TimeSeriesManager(1, -1)
    with pytest.raises(ValueError):
        time_series_manager.TimeSeriesManager(-1, -1)


def test_set_n_paa_segments_value_error():
    with pytest.raises(ValueError):
        tm.set_n_paa_segments(-1)


def test_set_n_paa_segments_updates():
    tm.n_paa_segments = None
    tm.set_n_paa_segments(9)
    assert tm.n_paa_segments == 9


def test_set_n_sax_symbols_value_error():
    with pytest.raises(ValueError):
        tm.set_n_sax_symbols(-1)


def test_set_n_sax_symbols_updates():
    tm.n_paa_segments = None
    tm.set_n_sax_symbols(9)
    assert tm.n_sax_symbols == 9
