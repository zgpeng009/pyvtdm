# coding: utf-8

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUiType
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui

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
                if j % 2 == 0:
                    _item.setBackground(QtGui.QColor(170, 170, 255))
                self.tableWidget.setRowHeight(j, 5)
                self.tableWidget.setItem(j, i, _item)

        label_list = ['工况名称', '载荷数量', '最大载荷', '最小载荷']
        self.tableWidget_2.setRowCount(15)
        self.tableWidget_2.setColumnCount(5)
        self.tableWidget_2.setHorizontalHeaderLabels(label_list)
        names_list = [['loadcase_01', '3', '10000N', '5000N'],
                      ['loadcase_03', '3', '10000N', '5000N'],
                      ['loadcase_04', '3', '10000N', '5000N'],
                      ['loadcase_07', '6', '30000N', '10000N'],
                      ['loadcase_08', '6', '30000N', '10000N'],
                      ['loadcase_09', '6', '30000N', '10000N'],
                      ['loadcase_11', '12', '60000N', '10000N'],
                      ['loadcase_12', '12', '60000N', '10000N'], ]
        for j, items in enumerate(names_list):
            for i, item in enumerate(items):
                _item = QTableWidgetItem(str(item))
                _item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_2.setRowHeight(j, 5)
                self.tableWidget_2.setItem(j, i, _item)

        label_list = ['载荷类型', '载荷ID', '载荷方向', '载荷大小', '载荷位置']
        self.tableWidget_3.setRowCount(15)
        self.tableWidget_3.setColumnCount(5)
        self.tableWidget_3.setHorizontalHeaderLabels(label_list)
        names_list = [['单点力', '1', 'X', '5000N', 'node 105'],
                      ['单点力', '2', 'Y', '5000N', 'node 105'],
                      ['单点力', '3', 'Z', '10000N', 'node 105'], ]
        for j, items in enumerate(names_list):
            for i, item in enumerate(items):
                _item = QTableWidgetItem(str(item))
                _item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_3.setRowHeight(j, 5)
                self.tableWidget_3.setItem(j, i, _item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = DIALOG2()
    dialog.show()
    sys.exit(app.exec())
