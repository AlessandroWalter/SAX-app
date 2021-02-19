from app import time_series_creator, view
import PySimpleGUI as sg
import sys


def welcome_me(name):
    return f'Hi, {name}'


def start_gui():
    while True:
        event, values = view.window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            view.window.close()
            sys.exit()


if __name__ == '__main__':
    time_series = time_series_creator.create_utc_time_series('1/1/2020', '1/1/2021', 'H')
    time_series_creator.do_simple_eda(time_series)
    start_gui()


