from app.controller import Controller
from app.time_series_manager import TimeSeriesManager
from app.view import View


if __name__ == '__main__':
    tm = TimeSeriesManager(25, 5)
    view = View()
    controller = Controller(tm, view)
    controller.start()


