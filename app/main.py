from app import time_series_manager, view
import PySimpleGUI as sg
import sys


def run_gui():
    while True:
        event, values = view.window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            view.window.close()
            sys.exit()


if __name__ == '__main__':
    time_series_manager = time_series_manager.TimeSeriesManager(1, 200, 1, 10)
    time_series_manager.create_scaled_ts(0, 1)
    time_series_manager.create_paa_ts(10)
    time_series_manager.generate_sax_symbols(10)
    view.init_layout(time_series_manager.ts,
                     time_series_manager.scaled_ts,
                     time_series_manager.paa_ts,
                     time_series_manager.sax_symbols.ravel())
    run_gui()


