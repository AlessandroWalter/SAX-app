import asyncio
from app import time_series_manager, view
import PySimpleGUI as sg
import sys
import traceback


async def update_gui(values):
    keys_to_clear = ['n_paa_segments', 'n_sax_symbols', 'ts_seed']
    is_input_valid = False
    try:
        n_paa_segments = values['n_paa_segments']
        n_sax_symbols = values['n_sax_symbols']
        ts_seed = values['ts_seed']
        if ts_seed != '':
            ts_seed = int(ts_seed)
            is_input_valid = True
            time_series_manager.create_random_walk_ts(1, 200, 1, seed=ts_seed)
            time_series_manager.create_scaled_ts(0, 1)
        if n_paa_segments != '':
            n_paa_segments = int(n_paa_segments)
            is_input_valid = True
            if n_paa_segments >= 99:
                n_paa_segments = 99
            if n_paa_segments < 1:
                raise ValueError
            time_series_manager.set_n_paa_segments(n_paa_segments)

        if n_sax_symbols != '':
            n_sax_symbols = int(n_sax_symbols)
            is_input_valid = True
            if n_sax_symbols >= 99:
                n_sax_symbols = 99
            if n_sax_symbols < 1:
                raise ValueError
            time_series_manager.set_n_sax_symbols(n_sax_symbols)

        if is_input_valid:
            time_series_manager.create_paa_ts()
            time_series_manager.generate_sax_symbols()
            tf = time_series_manager.count_sax_symbols()
            view.reset_and_draw_plots(
                time_series_manager.random_walk_ts[0].ravel(),
                time_series_manager.scaled_ts[0].ravel(),
                time_series_manager.paa_ts[0].ravel(),
                tf
            )

    except ValueError as e:
        print(e)
        traceback.print_stack()

    for key in keys_to_clear:
        view.window[key]('')


def run_gui():
    while True:
        event, values = view.window.read()
        if event == sg.WIN_CLOSED or event == 'Close':
            view.window.close()
            sys.exit()
        if event == 'Update':
            asyncio.run(update_gui(values))


if __name__ == '__main__':
    time_series_manager = time_series_manager.TimeSeriesManager(9, 5)
    time_series_manager.create_random_walk_ts(1, 200, 1, 10)
    time_series_manager.create_scaled_ts(0, 1)
    time_series_manager.create_paa_ts()
    time_series_manager.generate_sax_symbols()
    tf = time_series_manager.count_sax_symbols()
    view.init_layout(time_series_manager.random_walk_ts[0].ravel(),
                     time_series_manager.scaled_ts[0].ravel(),
                     time_series_manager.paa_ts[0].ravel(),
                     tf)
    run_gui()


