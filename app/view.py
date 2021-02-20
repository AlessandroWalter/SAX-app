import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


window = None

matplotlib.use("TkAgg")
sg.theme('DarkAmber')


def draw_plots(ts, scaled_ts, paa_ts, sax_symbols):
    fig, axs = plt.subplots(3, figsize=(7, 5), dpi=100)
    fig.subplots_adjust(bottom=0.1, left=0.1)
    axs[0].plot(ts[0].ravel())
    axs[0].set_ylabel('value')
    axs[1].plot(scaled_ts[0].ravel())
    axs[1].plot(paa_ts[0].ravel())
    axs[1].set_xlabel('t')
    axs[1].set_ylabel('value')
    unique, counts = np.unique(sax_symbols, return_counts=True)
    axs[2].bar(unique, counts)
    axs[2].set_xlabel('symbol')
    axs[2].set_ylabel('frequency')

    figure_canvas_agg = FigureCanvasTkAgg(fig, window['line-canvas'].TKCanvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)


def init_layout(ts, scaled_ts, paa_ts, sax_symbols):
    line_plot_column = [
        [sg.Canvas(key='line-canvas'), sg.Text('Frequencies')]
    ]
    input_column = [
        [sg.Text('Number of segments')],
        [sg.Text('Number of SAX-classes')]
    ]
    layout = [
        [sg.VSeperator()],
        [sg.Column(line_plot_column)]
    ]
    global window
    window = sg.Window('SAX-App', layout, finalize=True)
    draw_plots(ts, scaled_ts, paa_ts, sax_symbols)


def set_min_val(new_min_val):
    global window
    window['min_val'].update(new_min_val)


def set_max_val(new_max_val):
    global window
    window['max_val'].update(new_max_val)

