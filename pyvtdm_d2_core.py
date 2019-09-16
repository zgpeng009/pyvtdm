# coding: utf-8

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUiType
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

Ui_pyvtdm = loadUiType('pyvtdm_d2.ui')[0]
from cae_model.bdf_model import FEM


class DIALOG2(QDialog, Ui_pyvtdm):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinMaxButtonsHint)

        # aaa = eval("self.%s" % 'tableWidget')
        fem = FEM()
        self.model = fem.model

        label_list = ['模型名称', '单元编号', '单元属性编号', '节点编号', '节点编号', '节点编号', '节点编号']
        self.tableWidget.setRowCount(15)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(label_list)
        for j in range(15):
            names_list = ['QUAD4']
            element = self.model.elements[j + 15]
            names_list.append(element.eid)
            names_list.append(element.pid)
            names_list.extend(element.nodes)
            for i, item in enumerate(names_list):
                _item = QTableWidgetItem(str(item))
                _item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(j, i, _item)

        label_list = ['模型名称', '单元编号', '单元属性编号', '节点编号', '节点编号', '节点编号', '节点编号']
        self.tableWidget_2.setRowCount(15)
        self.tableWidget_2.setColumnCount(7)
        self.tableWidget_2.setHorizontalHeaderLabels(label_list)
        for j in range(15):
            names_list = ['QUAD4']
            element = self.model.elements[j + 15]
            names_list.append(element.eid)
            names_list.append(element.pid)
            names_list.extend(element.nodes)
            for i, item in enumerate(names_list):
                _item = QTableWidgetItem(str(item))
                _item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_2.setItem(j, i, _item)

        label_list = ['模型名称', '单元编号', '单元属性编号', '节点编号', '节点编号', '节点编号', '节点编号']
        self.tableWidget_3.setRowCount(15)
        self.tableWidget_3.setColumnCount(7)
        self.tableWidget_3.setHorizontalHeaderLabels(label_list)
        for j in range(15):
            names_list = ['QUAD4']
            element = self.model.elements[j + 15]
            names_list.append(element.eid)
            names_list.append(element.pid)
            names_list.extend(element.nodes)
            for i, item in enumerate(names_list):
                _item = QTableWidgetItem(str(item))
                _item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_3.setItem(j, i, _item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = DIALOG2()
    dialog.show()
    sys.exit(app.exec())
