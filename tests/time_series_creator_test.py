from app import main, time_series_creator

created_time_series = time_series_creator.create_utc_time_series('1/1/2020', '1/1/2021', 'H')


def test_welcome_me():
    name = 'test'
    assert main.welcome_me(name) == f'Hi, {name}'


def test_create_utc_time_series_has_correct_length():
    expected_df_length = 8785
    assert len(created_time_series.index) == expected_df_length


def test_create_utc_time_series_has_no_nulls():
    assert created_time_series.isnull().to_numpy().sum() == 0


