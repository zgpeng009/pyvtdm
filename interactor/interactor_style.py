import sys
import vtk
import numpy as np
from vtk.util.numpy_support import (
    create_vtk_array, get_numpy_array_type,
    get_vtk_array_type, numpy_to_vtk, vtk_to_numpy,
)


class MyInteractorStyle(object):
    def __init__(self, main_wnd):
        # self.AddObserver('LeftButtonPressEvent', self.left_button_press_event)
        # self.AddObserver('MouseMoveEvent', self.mouse_move_event)
        # self.mouse_motion_flag = 0
        # self.ren = self.iren.FindPokedRenderer(0, 0)
        self.ren = main_wnd.render
        self.renWin = self.ren.GetRenderWindow()
        self.iren = self.renWin.GetInteractor()
        self.grid = main_wnd.grid

        self.actors = []
        self.node_ids = []

        self.picker = vtk.vtkPointPicker()

        self.picker_points = []
        # self.area_picker = vtk.vtkAreaPicker()
        self.area_picker = vtk.vtkRenderedAreaPicker()
        self.area_picker.SetRenderer(self.ren)

        self.Rotating = 0
        self.Panning = 0
        self.Zooming = 0
        self.SinglePick = 0
        self.BoxPick = 0
        self.SinglePickRelease = 0
        self.BoxPickRelease = 0

        self.iren.AddObserver('LeftButtonPressEvent', self.PickEvent)
        self.iren.AddObserver('LeftButtonReleaseEvent', self.PickEvent)
        self.iren.AddObserver("MiddleButtonPressEvent", self.MoveEvent)
        self.iren.AddObserver("MiddleButtonReleaseEvent", self.MoveEvent)
        self.iren.AddObserver("MouseMoveEvent", self.MouseMove)
        self.iren.AddObserver("KeyPressEvent", self.Keypress)

    def PickEvent(self, obj, event):
        if event == "LeftButtonPressEvent":
            if obj.GetControlKey():
                self.box_pick_left_button_down_event(self.iren)
                self.BoxPick = 1
            else:
                self.single_pick(self.iren)
                self.SinglePick = 1
        elif event == 'LeftButtonReleaseEvent':
            if self.BoxPickRelease:
                self.box_pick_left_button_release_event(self.iren)
                self.BoxPickRelease = 0
                self.BoxPick = 0
            else:
                self.SinglePick = 0
                self.SinglePickRelease = 0

    # Handle the mouse button events.
    def MoveEvent(self, obj, event):
        if event == "MiddleButtonPressEvent":
            if obj.GetControlKey():
                self.Zooming = 1
            elif obj.GetShiftKey():
                self.Panning = 1
            else:
                self.Rotating = 1
        elif event == "MiddleButtonReleaseEvent":
            self.Rotating = 0
            self.Panning = 0
            self.Zooming = 0

            # elif event == "RightButtonPressEvent":
            #     self.Zooming = 1
            # elif event == "RightButtonReleaseEvent":
            #     self.Zooming = 0

    # General high-level logic
    def MouseMove(self, obj, event):
        lastXYpos = self.iren.GetLastEventPosition()
        lastX = lastXYpos[0]
        lastY = lastXYpos[1]

        xypos = self.iren.GetEventPosition()
        x = xypos[0]
        y = xypos[1]

        center = self.renWin.GetSize()
        centerX = center[0] / 2.0
        centerY = center[1] / 2.0

        if self.Rotating:
            self.Rotate(self.ren, self.ren.GetActiveCamera(), x, y, lastX, lastY, centerX, centerY)
        elif self.Panning:
            self.Pan(self.ren, self.ren.GetActiveCamera(), x, y, lastX, lastY, centerX, centerY)
        elif self.Zooming:
            self.Dolly(self.ren, self.ren.GetActiveCamera(), x, y, lastX, lastY, centerX, centerY)
        elif self.BoxPick:
            self.box_pick_mouse_move_event(self.iren)

    def Keypress(self, obj, event):
        key = obj.GetKeySym()
        if key == "e":
            obj.InvokeEvent("DeleteAllObjects")
            sys.exit()
        elif key == "w":
            self.Wireframe()
        elif key == "s":
            self.Surface()

    # Routines that translate the events into camera motions.
    # This one is associated with the left mouse button. It translates x
    # and y relative motions into camera azimuth and elevation commands.
    def Rotate(self, renderer, camera, x, y, lastX, lastY, centerX, centerY):
        camera.Azimuth(lastX - x)
        camera.Elevation(lastY - y)
        camera.OrthogonalizeViewUp()
        self.renWin.Render()

    # Pan translates x-y motion into translation of the focal point and
    # position.
    def Pan(self, renderer, camera, x, y, lastX, lastY, centerX, centerY):
        FPoint = camera.GetFocalPoint()
        FPoint0 = FPoint[0]
        FPoint1 = FPoint[1]
        FPoint2 = FPoint[2]

        PPoint = camera.GetPosition()
        PPoint0 = PPoint[0]
        PPoint1 = PPoint[1]
        PPoint2 = PPoint[2]

        renderer.SetWorldPoint(FPoint0, FPoint1, FPoint2, 1.0)
        renderer.WorldToDisplay()
        DPoint = renderer.GetDisplayPoint()
        focalDepth = DPoint[2]

        APoint0 = centerX + (x - lastX)
        APoint1 = centerY + (y - lastY)

        renderer.SetDisplayPoint(APoint0, APoint1, focalDepth)
        renderer.DisplayToWorld()
        RPoint = renderer.GetWorldPoint()
        RPoint0 = RPoint[0]
        RPoint1 = RPoint[1]
        RPoint2 = RPoint[2]
        RPoint3 = RPoint[3]

        if RPoint3 != 0.0:
            RPoint0 = RPoint0 / RPoint3
            RPoint1 = RPoint1 / RPoint3
            RPoint2 = RPoint2 / RPoint3

        factor = 1.0
        camera.SetFocalPoint((FPoint0 - RPoint0) / factor + FPoint0,
                             (FPoint1 - RPoint1) / factor + FPoint1,
                             (FPoint2 - RPoint2) / factor + FPoint2)
        camera.SetPosition((FPoint0 - RPoint0) / factor + PPoint0,
                           (FPoint1 - RPoint1) / factor + PPoint1,
                           (FPoint2 - RPoint2) / factor + PPoint2)
        self.renWin.Render()

    # Dolly converts y-motion into a camera dolly commands.
    def Dolly(self, renderer, camera, x, y, lastX, lastY, centerX, centerY):
        # dollyFactor = pow(1.02, (0.5 * (y - lastY)))
        dollyFactor = pow(1.02, (0.5 * (lastY - y)))
        if camera.GetParallelProjection():
            parallelScale = camera.GetParallelScale() * dollyFactor
            camera.SetParallelScale(parallelScale)
        else:
            camera.Dolly(dollyFactor)
            renderer.ResetCameraClippingRange()

        self.renWin.Render()

    # Wireframe sets the representation of all actors to wireframe.
    def Wireframe(self):
        actors = self.ren.GetActors()
        actors.InitTraversal()
        actor = actors.GetNextItem()
        while actor:
            actor.GetProperty().SetRepresentationToWireframe()
            actor = actors.GetNextItem()

        self.renWin.Render()

    # Surface sets the representation of all actors to surface.
    def Surface(self):
        actors = self.ren.GetActors()
        actors.InitTraversal()
        actor = actors.GetNextItem()
        while actor:
            actor.GetProperty().SetRepresentationToSurface()
            actor = actors.GetNextItem()
        self.renWin.Render()

    def box_pick_left_button_down_event(self, obj):
        self.StartPosition = obj.GetEventPosition()
        self.picker_points.append(self.StartPosition)
        self.pixel_array = vtk.vtkUnsignedCharArray()
        self.pixel_array.Initialize()
        self.pixel_array.SetNumberOfComponents(4)
        size = self.renWin.GetSize()
        self.pixel_array.SetNumberOfTuples(size[0] * size[1])
        self.renWin.GetRGBACharPixelData(0, 0, size[0] - 1, size[1] - 1, 1, self.pixel_array)

    def box_pick_mouse_move_event(self, obj):
        self.EndPosition = obj.GetEventPosition()
        EndPosition = list(self.EndPosition)
        size = self.renWin.GetSize()

        if self.EndPosition[0] > (size[0] - 1):
            EndPosition[0] = size[0] - 1
        if self.EndPosition[0] < 0:
            EndPosition[0] = 0
        if self.EndPosition[1] > (size[1] - 1):
            EndPosition[1] = size[1] - 1
        if self.EndPosition[1] < 0:
            EndPosition[1] = 0

        tmp_pixel_array = vtk.vtkUnsignedCharArray()
        tmp_pixel_array.DeepCopy(self.pixel_array)
        # tmp_pixel_array = pixel_array
        pixel_numpy = vtk_to_numpy(tmp_pixel_array)
        # print(pixel_numpy)

        _min = [0, 0]
        _max = [0, 0]

        if self.StartPosition[0] <= EndPosition[0]:
            _min[0] = self.StartPosition[0]
        else:
            _min[0] = EndPosition[0]
        if _min[0] < 0:
            _min[0] = 0
        if _min[0] >= size[0]:
            _min[0] = size[0] - 1

        if self.StartPosition[1] <= EndPosition[1]:
            _min[1] = self.StartPosition[1]
        else:
            _min[1] = EndPosition[1]
        if _min[1] < 0:
            _min[1] = 0
        if _min[1] >= size[1]:
            _min[1] = size[1] - 1

        if EndPosition[0] > self.StartPosition[0]:
            _max[0] = EndPosition[0]
        else:
            _max[0] = self.StartPosition[0]
        if _max[0] < 0:
            _max[0] = 0
        if _max[0] >= size[0]:
            _max[0] = size[0] - 1

        if EndPosition[1] > self.StartPosition[1]:
            _max[1] = EndPosition[1]
        else:
            _max[1] = self.StartPosition[1]
        if _max[1] < 0:
            _max[1] = 0
        if _max[1] >= size[1]:
            _max[1] = size[1] - 1

        for i in range(_min[0], _max[0]):
            pixel_numpy[_min[1] * size[0] + i] = [0, 0, 0, 0]
            pixel_numpy[_max[1] * size[0] + i] = [0, 0, 0, 0]
            # pixel_numpy[_min[1] * size[0] + i] = [255 ^ pixel_numpy[_min[1] * size[0] + i][j] for j in range(4)]
            # pixel_numpy[_max[1] * size[0] + i] = [255 ^ pixel_numpy[_max[1] * size[0] + i][j] for j in range(4)]

        for i in range(_min[1], _max[1]):
            pixel_numpy[i * size[0] + _min[0]] = [0, 0, 0, 0]
            pixel_numpy[i * size[0] + _max[0]] = [0, 0, 0, 0]
            # pixel_numpy[i * size[0] + _min[0]] = [255 ^ pixel_numpy[i * size[0] + _min[0]][j] for j in range(4)]
            # pixel_numpy[i * size[0] + _max[0]] = [255 ^ pixel_numpy[i * size[0] + _max[0]][j] for j in range(4)]

        pixel_vtk = numpy_to_vtk(pixel_numpy)
        self.renWin.SetRGBACharPixelData(0, 0, size[0] - 1, size[1] - 1, pixel_vtk, 0)
        self.renWin.Frame()
        self.BoxPickRelease = 1

    def box_pick_left_button_release_event(self, obj):
        """
        gets the second point and calls _pick_depth_ids
        """
        pixel_x, pixel_y = obj.GetEventPosition()
        self.picker_points.append((pixel_x, pixel_y))
        # self.mouse_polygon.OnLeftButtonUp()

        if len(self.picker_points) == 2:
            p1x, p1y = self.picker_points[0]
            p2x, p2y = self.picker_points[1]
            # self.picker_points = []
            xmin = min(p1x, p2x)
            ymin = min(p1y, p2y)
            xmax = max(p1x, p2x)
            ymax = max(p1y, p2y)

            dx = abs(p1x - p2x)
            dy = abs(p1y - p2y)
            # self.picker_points = []
            if dx > 0 and dy > 0:
                self.pick_depth_ids(xmin, ymin, xmax, ymax)
        # print(self.picker_points)
        self.picker_points = []

    def pick_depth_ids(self, xmin, ymin, xmax, ymax):
        """
        Does an area pick of all the ids inside the box, even the ones
        behind the front elements
        """
        retval = self.area_picker.AreaPick(xmin, ymin, xmax, ymax, self.ren)
        # self.area_picker.Pick()
        frustum = self.area_picker.GetFrustum()  # vtkPlanes

        ids = vtk.vtkIdFilter()
        ids.SetInputData(self.grid)
        # ids.CellIdsOn()
        ids.PointIdsOn()
        ids.SetIdsArrayName("Ids")

        # get the cells/points inside the frustum
        selected_frustum = vtk.vtkExtractSelectedFrustum()
        selected_frustum.SetFieldType(True)
        selected_frustum.SetFrustum(frustum)
        selected_frustum.SetInputConnection(ids.GetOutputPort())
        selected_frustum.Update()
        picked_grid = selected_frustum.GetOutput()
        if picked_grid:
            point_ids = None
            points = picked_grid.GetPointData()
            if points is not None:
                ids = points.GetArray('Ids')
                if ids is not None:
                    point_ids = vtk_to_numpy(ids)
                    if len(point_ids) != 0:
                        self.node_ids.extend(point_ids)
                        points = self.grid.GetPoints()
                        _grid = vtk.vtkUnstructuredGrid()
                        _grid.SetPoints(points)
                        for node_id in point_ids:
                            vertex = vtk.vtkVertex()
                            vertex.GetPointIds().SetId(0, node_id)
                            _grid.InsertNextCell(vertex.GetCellType(), vertex.GetPointIds())
                        mapper = vtk.vtkDataSetMapper()
                        mapper.SetInputData(_grid)
                        colors = vtk.vtkNamedColors()
                        actor = vtk.vtkActor()
                        actor.SetMapper(mapper)
                        actor.GetProperty().SetColor(colors.GetColor3d("Tomato"))
                        # actor.GetProperty().SetOpacity(.5)
                        actor.GetProperty().SetPointSize(10)
                        self.actors.append(actor)
                        self.ren.AddActor(actor)
        self.iren.Render()

    def single_pick(self, caller):
        # caller.RemoveObservers('RotateEvent')
        clickcoords = caller.GetEventPosition()
        retval = self.picker.Pick(clickcoords[0], clickcoords[1], 0, self.ren)

        if 0:
            node_id = self.picker.GetPointId()
            points = self.grid.GetPoints()
            vertices = vtk.vtkCellArray()
            vertices.InsertNextCell(1, node_id)

            point = vtk.vtkPolyData()
            point.SetPoints(points)
            point.SetVerts(vertices)

            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputData(point)

            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetPointSize(6)

            self.actors.append(actor)
            self.ren.AddActor(actor)
            self.iren.Render()

        if retval:
            node_id = self.picker.GetPointId()
            self.node_ids.append(node_id)

            points = self.grid.GetPoints()
            vertex = vtk.vtkVertex()
            vertex.GetPointIds().SetId(0, node_id)

            grid = vtk.vtkUnstructuredGrid()
            grid.SetPoints(points)
            grid.InsertNextCell(vertex.GetCellType(), vertex.GetPointIds())

            mapper = vtk.vtkDataSetMapper()
            mapper.SetInputData(grid)

            colors = vtk.vtkNamedColors()
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetColor(colors.GetColor3d("Tomato"))
            # actor.GetProperty().SetOpacity(.5)
            actor.GetProperty().SetPointSize(10)

            self.actors.append(actor)
            self.ren.AddActor(actor)
        else:
            self.clear_actors()

        caller.Render()
        # self.style.OnLeftButtonUp()
        # self.style.OnLeftButtonDown()
        # self.iren.RemoveObservers('LeftButtonReleaseEvent')

    def clear_actors(self):
        self.node_ids = list(set(self.node_ids))
        for actor in self.actors:
            self.ren.RemoveActor(actor)
            del actor
        self.node_ids = []
        self.iren.Render()
