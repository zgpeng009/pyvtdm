# coding: utf-8

import sys

import matplotlib

matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt5.QtWidgets import *


class FGWidget(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure()
        FigureCanvas.__init__(self, self.fig)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    figure = FGWidget()
    axes = figure.fig.add_subplot(111)
    figure.show()
    sys.exit(app.exec())
