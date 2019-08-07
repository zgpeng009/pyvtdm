from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

print('Using PyQT5')


class QVTKWidget(QVTKRenderWindowInteractor):
    def __init__(self, parent=None):
        QVTKRenderWindowInteractor.__init__(self, parent)
