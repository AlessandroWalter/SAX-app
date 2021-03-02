import sys
import traceback


class Controller:

    def __init__(self, time_manager, view):
        self.tm = time_manager
        self.view = view

    def on_close_pressed(self):
        self.view.get_window().close()
        sys.exit()

    def on_update_pressed(self, values):
        should_recreate_paa_ts = False
        should_recreate_n_sax_symbols = False
        try:
            n_paa_segments = values['n_paa_segments']
            n_sax_symbols = values['n_sax_symbols']
            ts_seed = values['ts_seed']
            if ts_seed != '':
                ts_seed = int(ts_seed)
                should_recreate_paa_ts = True
                should_recreate_n_sax_symbols = True
                self.tm.set_base_ts(self.tm.create_random_walk_ts(1, 200, 1, seed=ts_seed))
                self.tm.create_and_update_scaled_ts(0, 1, self.tm.get_base_ts())
            if n_paa_segments != '':
                n_paa_segments = int(n_paa_segments)
                should_recreate_paa_ts = True
                should_recreate_n_sax_symbols = True
                self.tm.set_n_paa_segments(n_paa_segments)
            if n_sax_symbols != '':
                n_sax_symbols = int(n_sax_symbols)
                should_recreate_n_sax_symbols = True
                self.tm.set_n_sax_symbols(n_sax_symbols)

            if should_recreate_paa_ts:
                self.tm.create_and_update_paa_ts(self.tm.get_n_paa_segments(), self.tm.get_scaled_ts())
            if should_recreate_n_sax_symbols:
                self.tm.generate_and_update_sax_symbols(self.tm.get_n_paa_segments(), self.tm.get_n_sax_symbols(),
                                                        self.tm.get_scaled_ts())
            if should_recreate_n_sax_symbols | should_recreate_paa_ts:
                self.tm.notify()

        except ValueError as e:
            print(e)
            traceback.print_stack()

    def start(self):
        self.tm.set_base_ts(self.tm.create_random_walk_ts(1, 200, 1, 10))
        self.tm.create_and_update_scaled_ts(0, 1, self.tm.get_base_ts())
        self.tm.create_and_update_paa_ts(self.tm.get_n_paa_segments(), self.tm.get_scaled_ts())
        self.tm.generate_and_update_sax_symbols(self.tm.get_n_paa_segments(), self.tm.get_n_sax_symbols(),
                                                self.tm.get_scaled_ts())

        self.view.set_simple_gui_theme('DarkAmber')
        self.view.set_matplotlib_backend('TkAgg')
        self.view.init_layout()

        self.tm.attach(self.view)
        self.tm.notify()
        self.view.run_gui(self)

