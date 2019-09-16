# coding: utf-8

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUiType
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

Ui_pyvtdm = loadUiType('pyvtdm_login.ui')[0]


class WIDGET(QWidget, Ui_pyvtdm):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowCloseButtonHint)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = WIDGET()
    dialog.show()
    sys.exit(app.exec())
