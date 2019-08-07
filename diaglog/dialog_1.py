# coding: utf-8

import os

from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUiType

Ui_Dialog = loadUiType('diaglog/dialog_1_w.ui')[0]


class DLG(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
