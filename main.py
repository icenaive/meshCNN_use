import vtk
import torch
from models.networks import MeshEncoderDecoder, init_weights
from models.layers.mesh import Mesh

# Renderer
renderer = vtk.vtkRenderer()

# Render window
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)
renWin.SetSize(1000, 1000)

# Render window interactor
iren = vtk.vtkRenderWindowInteractor()

interactorStyle = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(interactorStyle)
iren.SetRenderWindow(renWin)



def make_actor(polydata):
    
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)
    # mapper.SetScalarRange([0.0, 15.0])

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)


    return actor



if __name__ == "__main__":



    #Get Torch Network
    # ncf = [64, 128, 256]
    # ninput_edges 2280

    down_convs = [5, 64, 128, 256]
    up_convs = [256, 128, 64, 8]
    pool_res = [2250, 1350, 600]
    resblocks =  3


    net = MeshEncoderDecoder(pool_res, down_convs, up_convs, resblocks)
    init_weights(net, 'normal', 0.02)

    #Import sample mesh
    mesh = Mesh('./data/test.obj')
    mesh_feature = mesh.extract_features()
    

    sample_input = torch.tensor(mesh_feature).unsqueeze(0).float()
    print(sample_input.size())
    
    y = net.forward(sample_input, [mesh])

    print(y.size())
    
    
    
    
    exit() 
    reader = vtk.vtkOBJReader()
    reader.SetFileName('./data/test.obj')
    reader.Update()

    polydata = reader.GetOutput()
    ############################################
    
    points = polydata.GetPoints()
    vs = []

    for i in range(points.GetNumberOfPoints()):
        vs.append(polydata.GetPoint(i))

    print(len(vs), vs[0])

    polys = polydata.GetPolys()
    faces = []
    for i in range(polys.GetNumberOfCells()):
        ids = []
        pointids = polydata.GetCell(i).GetPointIds()
        
        faces.append(pointids)

    print(len(faces), faces[0])
    
    
    #######################################################
    actor = make_actor(polydata)


    renderer.AddActor(actor)
    renWin.Render()
    iren.Start()