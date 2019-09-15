# coding: utf-8

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUiType
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

Ui_pyvtdm = loadUiType('pyvtdm_d1.ui')[0]


class DIALOG1(QDialog, Ui_pyvtdm):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinMaxButtonsHint)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = DIALOG1()
    dialog.show()
    sys.exit(app.exec())
