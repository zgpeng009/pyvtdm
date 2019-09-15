from __future__ import print_function

import os

# print(os.environ['path'])
# os.environ['path'] += r';E:\work\pyvtdm\oce-0.18.3\Win64\bin'
# os.environ['path'] += ';C:\\Python36'

import sys

# sys.path.append(r'E:\work\pyvtdm\venv\Lib\site-packages\OCC\Core')

from OCC.Display.backend import load_pyqt5
from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox

# check for pyqt5
if not load_pyqt5():
    print("pyqt5 required to run this test")
    sys.exit()

print('pyqt5 test')
pyqt5_display, start_display, add_menu, add_function_to_menu = init_display('qt-pyqt5')
my_box_1 = BRepPrimAPI_MakeBox(10., 20., 30.).Shape()
pyqt5_display.DisplayShape(my_box_1, update=True)
pass
