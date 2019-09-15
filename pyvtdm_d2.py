# coding: utf-8

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUiType
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

Ui_pyvtdm = loadUiType('pyvtdm_d2.ui')[0]


class DIALOG2(QDialog, Ui_pyvtdm):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinMaxButtonsHint)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = DIALOG2()
    dialog.show()
    sys.exit(app.exec())
