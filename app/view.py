from app.observer import Observer
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator
import matplotlib
import matplotlib.pyplot as plt


class View(Observer):

    def __init__(self):
        self._window = None
        self._figure_canvas_agg = None
        self._keys = None

    def get_figure_canvas_agg(self):
        return self._figure_canvas_agg

    def set_figure_canvas_agg(self, figure_canvas_agg):
        self._figure_canvas_agg = figure_canvas_agg

    def get_keys(self):
        return self._keys

    def set_keys(self, keys):
        self._keys = keys

    @staticmethod
    def set_simple_gui_theme(theme):
        sg.theme(theme)

    @staticmethod
    def set_matplotlib_backend(aggregate):
        matplotlib.use(aggregate)

    def set_window(self, window):
        self._window = window

    def get_window(self):
        return self._window

    def clear_input_texts(self, keys):
        for key in keys:
            self.get_window()[key]('')

    def draw_plots(self, ts, scaled_ts, paa_ts, tf):
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

        self.set_figure_canvas_agg(FigureCanvasTkAgg(fig, self.get_window()['canvas'].TKCanvas))
        self.get_figure_canvas_agg().draw()
        self.get_figure_canvas_agg().get_tk_widget().pack(side='top', fill='both', expand=1)

    def delete_fig_canvas(self):
        self._figure_canvas_agg.get_tk_widget().forget()
        plt.close('all')

    def init_layout(self):
        line_plot_column = [
            [sg.Canvas(key='canvas')]
        ]
        input_column = [
            [sg.Text('Number of PAA segments')],
            [sg.Input(key='n_paa_segments')],
            [sg.Text('Number of unique SAX symbols')],
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

        self.set_keys(['n_paa_segments', 'n_sax_symbols', 'ts_seed'])
        self.set_window(sg.Window('SAX-App', layout, finalize=True))

    def run_gui(self, controller):
        while True:
            event, values = self.get_window().read()
            if event == sg.WIN_CLOSED or event == 'Close':
                controller.on_close_pressed()
            if event == 'Update':
                controller.on_update_pressed(values)

    def update(self, tm):
        if self.get_figure_canvas_agg() is not None:
            self.delete_fig_canvas()
        self.draw_plots(
            tm.get_base_ts()[0].ravel(),
            tm.get_scaled_ts()[0].ravel(),
            tm.get_paa_ts()[0].ravel(),
            tm.count_sax_symbols()
        )
        self.clear_input_texts(self.get_keys())

