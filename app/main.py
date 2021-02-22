import asyncio
from app import view
from app.time_series_manager import TimeSeriesManager
import sys
import traceback


async def update_gui(values, tm):
    keys_to_clear = ['n_paa_segments', 'n_sax_symbols', 'ts_seed']
    is_input_valid = False
    try:
        n_paa_segments = values['n_paa_segments']
        n_sax_symbols = values['n_sax_symbols']
        ts_seed = values['ts_seed']
        if ts_seed != '':
            ts_seed = int(ts_seed)
            if ts_seed > 9999999:
                ts_seed = 999999
            is_input_valid = True
            tm.create_random_walk_ts(1, 200, 1, seed=ts_seed)
            tm.create_scaled_ts(0, 1)
        if n_paa_segments != '':
            n_paa_segments = int(n_paa_segments)
            is_input_valid = True
            if n_paa_segments >= 99:
                n_paa_segments = 99
            if n_paa_segments < 1:
                raise ValueError
            tm.set_n_paa_segments(n_paa_segments)

        if n_sax_symbols != '':
            n_sax_symbols = int(n_sax_symbols)
            is_input_valid = True
            if n_sax_symbols >= 99:
                n_sax_symbols = 99
            if n_sax_symbols < 1:
                raise ValueError
            tm.set_n_sax_symbols(n_sax_symbols)

        if is_input_valid:
            tm.create_paa_ts()
            tm.generate_sax_symbols()
            tf = tm.count_sax_symbols()
            view.reset_and_draw_plots(
                tm.random_walk_ts[0].ravel(),
                tm.scaled_ts[0].ravel(),
                tm.paa_ts[0].ravel(),
                tf
            )

    except ValueError as e:
        print(e)
        traceback.print_stack()

    for key in keys_to_clear:
        view.window[key]('')


def on_close_pressed(window):
    window.close()
    sys.exit()


def on_update_pressed(values, tm):
    asyncio.run(update_gui(values, tm))


if __name__ == '__main__':
    tm = TimeSeriesManager(9, 5)
    tm.create_random_walk_ts(1, 200, 1, 10)
    tm.create_scaled_ts(0, 1)
    tm.create_paa_ts()
    tm.generate_sax_symbols()
    tf = tm.count_sax_symbols()

    view.init_layout(tm.random_walk_ts[0].ravel(),
                     tm.scaled_ts[0].ravel(),
                     tm.paa_ts[0].ravel(),
                     tf)
    view.run_gui(tm)


