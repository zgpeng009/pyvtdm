# coding: utf-8

import sys
import os
import numpy as np
import matplotlib

from PyQt5.uic import loadUiType
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

Ui_pyvtdm = loadUiType('pyvtdm_d3.ui')[0]
myfont = matplotlib.font_manager.FontProperties(fname='simhei.ttf')


class DIALOG2(QDialog, Ui_pyvtdm):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinMaxButtonsHint)

        names = [u'静力试验', u'加载级(0-1)', u'位移(mm)']
        data1 = np.array([i / 10.0 for i in range(1, 11)])

        data2 = np.array([i / 100.0 for i in range(1, 11)])
        data_random = np.random.randint(10, size=10) / 1000
        data2 += data_random

        data3 = np.array([i / 70.0 for i in range(1, 11)])
        data_random = np.random.randint(10, size=10) / 1000
        data3 += data_random

        data4 = np.array([i / 50.0 for i in range(1, 11)])
        data_random = np.random.randint(10, size=10) / 1000
        data4 += data_random

        self.axes = self.widget.fig.add_subplot(111)
        self.axes.grid(True)
        self.axes.set_title(names[0], fontproperties=myfont, fontsize=15)
        self.axes.set_xlabel(names[1], fontproperties=myfont, fontsize=12)
        self.axes.set_ylabel(names[2], fontproperties=myfont, fontsize=12)
        self.axes.plot(data1, data2, c='r', marker='o', label='node 1')
        self.axes.plot(data1, data3, c='b', marker='*', label='node 2')
        self.axes.plot(data1, data4, c='g', marker='+', label='node 3')
        # self.axes.scatter(data1, data2, s=40, c='r', marker='o', edgecolor='c')
        self.axes.legend(loc='upper left')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = DIALOG2()
    dialog.show()
    sys.exit(app.exec())
