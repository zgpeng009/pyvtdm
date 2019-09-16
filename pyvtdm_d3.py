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

        names = [u'静力试验', u'加载级', u'位移']
        data1 = [1, 2, 3]
        data2 = [2, 4, 6]
        self.axes = self.widget.fig.add_subplot(111)
        self.axes.grid(True)
        self.axes.set_title(names[0], fontproperties=myfont, fontsize=15)
        self.axes.set_xlabel(names[1], fontproperties=myfont, fontsize=12)
        self.axes.set_ylabel(names[2], fontproperties=myfont, fontsize=12)
        self.axes.plot(data1, data1, 'k--', linewidth=0.7)
        self.axes.scatter(data1, data2, s=40, c='', marker='o', edgecolor='c')
        self.axes.legend(loc='upper left')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = DIALOG2()
    dialog.show()
    sys.exit(app.exec())
