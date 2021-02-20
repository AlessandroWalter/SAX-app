# exec in terminal: python -m pytest tests

from app import time_series_manager
import numpy as np

tm = time_series_manager.TimeSeriesManager(1, 100, 1)


def test_create_random_walk_ts_has_correct_length():
    expected_df_length = 878
    tm.create_random_walk_ts(1, expected_df_length, 1)
    assert tm.ts.size == expected_df_length


def test_create_random_walk_has_no_nan():
    tm.create_random_walk_ts(1, 100, 1)
    assert np.count_nonzero(np.isnan(tm.ts)) == 0




