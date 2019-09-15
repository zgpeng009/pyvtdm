import sys
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

print('Using PyQT5')


class QVTKWidget(QVTKRenderWindowInteractor):
    def __init__(self, parent=None):
        QVTKRenderWindowInteractor.__init__(self, parent)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    qvtk = QVTKWidget()
    qvtk.show()
    sys.exit(app.exec_())
