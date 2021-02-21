import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("TkAgg")
sg.theme('DarkAmber')

window = None
figure_canvas_agg = None


def delete_fig_canvas():
    global figure_canvas_agg
    figure_canvas_agg.get_tk_widget().forget()
    plt.close('all')


def draw_plots(ts, scaled_ts, paa_ts, tf):
    fig, axs = plt.subplots(3, figsize=(7, 6), dpi=100)
    fig.subplots_adjust(top=0.99, bottom=0.08, left=0.09, right=0.98, hspace=0.35)
    axs[0].plot(ts, label='Original time series')
    axs[0].legend(loc='best')
    axs[0].set_ylabel('value')
    axs[1].plot(scaled_ts, label='Scaled time series')
    axs[1].plot(paa_ts, label='PAA')
    axs[1].legend(loc='best')
    axs[1].set_xlabel('t')
    axs[1].set_ylabel('value')
    axs[2].bar(tf[:, 0], tf[:, 1])
    axs[2].xaxis.set_major_locator(MaxNLocator(integer=True))
    axs[2].yaxis.set_major_locator(MaxNLocator(integer=True))
    axs[2].set_xlabel('SAX symbol')
    axs[2].set_ylabel('frequency')

    global figure_canvas_agg
    figure_canvas_agg = FigureCanvasTkAgg(fig, window['canvas'].TKCanvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)


def init_layout(ts, scaled_ts, paa_ts, tf):
    line_plot_column = [
        [sg.Canvas(key='canvas')]
    ]
    input_column = [
        [sg.Text('Number of PAA segments')],
        [sg.Input(key='n_paa_segments')],
        [sg.Text('Number of SAX symbols')],
        [sg.Input(key='n_sax_symbols')],
        [sg.Text('Time series seed')],
        [sg.Input(key='ts_seed')],
        [sg.Button('Update'), sg.Button('Close')]
    ]
    layout = [
        [
            sg.Column(line_plot_column),
            sg.VSeperator(),
            sg.Column(input_column)
        ]
    ]
    global window
    window = sg.Window('SAX-App', layout, finalize=True)
    draw_plots(ts, scaled_ts, paa_ts, tf)


def reset_and_draw_plots(ts, scaled_ts, paa_ts, tf):
    delete_fig_canvas()
    draw_plots(
        ts,
        scaled_ts,
        paa_ts,
        tf
    )


