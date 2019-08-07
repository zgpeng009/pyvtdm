from pyNastran.bdf.bdf import (BDF, CQUAD4)
from pyNastran.gui.utils.vtk.vtk_utils import (numpy_to_vtk_points, numpy_to_vtk)

from six import iteritems
import vtk
import os


class FEM(object):
    def __init__(self):
        self.current_dir = os.getcwd()
        bdfName = os.path.join(self.current_dir, 'cae_model/aerofoil_product.bdf')
        self.model = BDF()
        self.model.read_bdf(bdfName)

    def create_grid(self):
        # result_array = vtk.vtkDataArray.CreateDataArray(vtk_typecode)
        # result_array.SetNumberOfTuples(shape[0])
        # result_array.SetVoidArray(z_flat, len(z_flat), 1)
        # *********points_array = numpy_to_vtk(num_array=nodes, deep=deep, array_type=vtk.VTK_FLOAT,)
        # points = vtk.vtkPoints()
        # nnodes = nodes.shape[0]
        # points.SetNumberOfPoints(nnodes)
        # points.SetData(result_array)
        out = self.model.get_displacement_index_xyz_cp_cd(
            fdtype='float32', idtype='int32', sort_ids=True)

        icd_transform, icp_transform, xyz_cp, nid_cp_cd = out
        cid = 0

        xyz_cid0 = self.model.transform_xyzcp_to_xyz_cid(
            xyz_cp, nid_cp_cd[:, 0], icp_transform, cid=cid,
            in_place=False)

        points = numpy_to_vtk_points(xyz_cid0)

        grid = vtk.vtkUnstructuredGrid()
        grid.SetPoints(points)

        for (eid, element) in sorted(iteritems(self.model.elements)):
            if isinstance(element, CQUAD4):
                node_ids = element.node_ids
                n1, n2, n3, n4 = [int(nid) - 1 for nid in node_ids]
                elem = vtk.vtkQuad()
                elem.GetPointIds().SetId(0, n1)
                elem.GetPointIds().SetId(1, n2)
                elem.GetPointIds().SetId(2, n3)
                elem.GetPointIds().SetId(3, n4)
                grid.InsertNextCell(elem.GetCellType(), elem.GetPointIds())

        return grid

    def display_model_1(self):
        grid = self.create_grid()
        # ********source******************************
        cone = vtk.vtkConeSource()
        cone.SetHeight(30.0)
        cone.SetRadius(1.0)
        cone.SetResolution(10)
        # *********************************************


        # ************render***************************
        render = vtk.vtkRenderer()
        win = vtk.vtkRenderWindow()
        win.AddRenderer(render)
        inter = vtk.vtkRenderWindowInteractor()
        inter.SetRenderWindow(win)
        win.Render()
        # *********************************************


        # *********mapper and actor***************************************
        coneMapper = vtk.vtkPolyDataMapper()
        coneMapper.SetInputConnection(cone.GetOutputPort())
        mapperData = vtk.vtkDataSetMapper()
        mapperData.SetInputData(grid)

        actor = vtk.vtkActor()
        actor.SetMapper(mapperData)
        render.AddActor(actor)
        # ****************************************************************


        inter.Initialize()
        inter.Start()


if __name__ == '__main__':
    display = FEM()
    display.display_model_1()
