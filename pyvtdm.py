# coding: utf-8

import sys
import vtk
import os
import shutil
import shelve

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUiType

Ui_pyvtdm = loadUiType('pyvtdm_w.ui')[0]

from diaglog.dialog_1 import DLG
from interactor.interactor_style import MyInteractorStyle


class MainWnd(QMainWindow, Ui_pyvtdm):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.control_flag = 0
        self.mouse_motion_flag = 0

        self.setupUi(self)
        # self.show_maximized()

        self.cwd = os.getcwd()  # 获取当前程序文件位置

        self.grid = None
        self.color = vtk.vtkNamedColors()
        self.actor = vtk.vtkActor()

        self.is_edges_black = True
        prop = self.actor.GetProperty()
        prop.EdgeVisibilityOn()

        self.render = vtk.vtkRenderer()
        self.render.GetActiveCamera().ParallelProjectionOn()
        self.render.SetBackground(self.color.GetColor3d("SteelBlue"))  # SlateGray Peacock
        self.render.ResetCamera()

        self.axes = vtk.vtkAxesActor()
        self.axes.SetTotalLength(500.0, 500.0, 500.0)
        self.render.AddActor(self.axes)

        self.window = self.vtk_context.GetRenderWindow()
        self.window.AddRenderer(self.render)
        self.iren = self.window.GetInteractor()

        MyInteractorStyle(self)
        self.iren.SetInteractorStyle(None)
        self.iren.Initialize()
        self.iren.Start()

        # self.style.SetDefaultRenderer(self.render)
        # self.style = vtk.vtkInteractorStyleRubberBandPick()
        # vtk.vtkCommand() # 查看vtk事件

    def SetViewXY(self):
        camera = self.render.GetActiveCamera()
        camera.SetPosition(1.0, 0.0, 0.0)
        camera.SetFocalPoint(0.0, 0.0, 0.0)
        camera.SetViewUp(0.0, 0.0, 1.0)
        self.render.ResetCamera()
        self.iren.Render()

    def SetViewXZ(self):
        camera = self.render.GetActiveCamera()
        camera.SetPosition(0.0, 1.0, 0.0)
        camera.SetFocalPoint(0.0, 0.0, 0.0)
        camera.SetViewUp(0.0, 0.0, 1.0)
        self.render.ResetCamera()
        self.iren.Render()

    def SetViewYZ(self):
        camera = self.render.GetActiveCamera()
        camera.SetPosition(0.0, 0.0, 1.0)
        camera.SetFocalPoint(0.0, 0.0, 0.0)
        camera.SetViewUp(0.0, 1.0, 0.0)
        self.render.ResetCamera()
        self.iren.Render()

    def FitView(self):
        self.render.ResetCamera()
        self.iren.Render()

    def MeshEdge(self):
        self.is_edges_black = not self.is_edges_black
        if self.is_edges_black:
            prop = self.actor.GetProperty()
            prop.EdgeVisibilityOn()
        else:
            prop = self.actor.GetProperty()
            prop.EdgeVisibilityOff()
        self.actor.Modified()
        prop.Modified()
        self.iren.Render()

    def pick(self):
        aaa = self.iren.GetEventPosition()
        print(aaa)

    def my_diag(self):
        # QMessageBox.information(self, 'aaa', 'aaa')
        # print('aaa')
        self.dlg = DLG()
        self.dlg.show()
        # dlg.exec()

    def show_current(self):
        if self.grid:
            mapper = vtk.vtkDataSetMapper()
            mapper.SetInputData(self.grid)

            prop = self.actor.GetProperty()
            prop.SetPointSize(500)

            self.actor.SetMapper(mapper)
            self.render.AddActor(self.actor)
            # win = vtk.vtkRenderWindow()
            # win.AddRenderer(render)
            # interact = vtk.vtkRenderWindowInteractor()
            # interact..SetRenderWindow(win)

            self.render.ResetCamera()
            self.iren.Render()

            # self.iren.AddObserver('LeftButtonPressEvent', SinglePick(self.render, self.grid))
            # self.textBrowser.append(self.comboBox.currentText())

    def show_maximized(self):
        desktop = QApplication.desktop()
        rect = desktop.availableGeometry()
        self.setGeometry(rect)

    def path_copy_remove_rename(self, file):
        file_dat = file + '.dat'
        # file_dir = file + '.dir'
        # file_bak = file + '.bak'
        # if os.path.exists(file_dir):
        #     os.remove(file_dir)
        # if os.path.exists(file_bak):
        #     os.remove(file_bak)
        # if os.path.exists(file_dat):
        #     os.rename(file_dat, file)
        shutil.copy(file_dat, file)

    def open_db(self):
        files, filetype = QFileDialog.getOpenFileNames(self, "打开文件", self.cwd, "DataBase (*.db);;All Files (*)")

        # 读取数据
        if files:
            pass

    def open_bdf(self):
        files, filetype = QFileDialog.getOpenFileNames(self, "打开文件", self.cwd, "DataBase (*.bdf);;All Files (*)")

        # 读取数据
        if files:
            from cae_model.bdf_model import FEM
            fem = FEM()
            self.grid = fem.create_grid()
            self.show_current()

    def save_db(self):
        file, filetype = QFileDialog.getSaveFileName(self, "保存文件", self.cwd, "DataBase (*.db);;All Files (*)")

        # 保存数据
        if file:
            with shelve.open(file, 'n') as db:
                db['Tom'] = 'tom'
                db['Jerry'] = 'jerry'
            shutil.copy(file + '.dat', file)


def main():
    app = QApplication(sys.argv)
    mainwnd = MainWnd()
    mainwnd.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
