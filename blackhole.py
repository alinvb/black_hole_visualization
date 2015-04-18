# black_hole_visualization
Creating the visualization of the black hole merger from the simulation data
import math
import argparse
from paraview.simple import *
from numpy import *
from lookuptable import lookuptable1, lookuptable2, lookuptable3, lookuptable4
from AhA import *
# sets the values for the resolution and the number of frames 
parser = argparse.ArgumentParser( description = "resolution, frames")
parser.add_argument('resx',help = "Determines the x value and should be an integer", action = 'store', nargs ='?', default = 1280, type = int)
parser.add_argument('resy',help = "Determines the y value and should be an integer", action = 'store', nargs = '?', default = 720, type = int)
parser.add_argument('Nframes',help = " Determines the number of frames in the movie", action= 'store', nargs = '?', default =100, type = int)
parser.add_argument('output',help = "Determines the output directory where the images are stored", action = 'store', nargs = '?', default = '/cita/home/anbabul/CITA299/moviefinal', type = str())
args = parser.parse_args()
resx = args.resx
resy = args.resy
Nframes = args.Nframes
output = args.output

# the camera position and angle during the inspiral 
InspiralCamPos = array([ -16.51, 27.129, 22.889 ]) 
InspiralAngleOfView = math.radians(40.)

# the camera position and angle during the merger 
MergerCamPos = array([ -7.51, 18.129, 13.889 ]) 
MergerAngleOfView = math.radians(40.)



AhA = '/mnt/raid-project/nr/pfeiffer/CombineSamurai2/submovie0/Lev3/ApparentLev3_1_30/Data3.pvd'#Spinning Blackhole data location

AhB = '/mnt/raid-project/nr/pfeiffer/CombineSamurai2/submovie0/Lev3/ApparentLev3_2_30/Data3.pvd'#Non-Spinning Blackhole data location

AhC = '/mnt/raid-project/nr/pfeiffer/CombineSamurai2/submovie0/Lev3/ApparentLev3_3_30/Data3.pvd' #Combined Blackhole data location

plane = '/mnt/raid-project/nr/pfraser/CombineSamurai2/root_Lev3/Data_Inner_15/Combine3.pvd'# Angular Momentum Plane data location

Trajectory_AhA = '/mnt/raid-project/nr/pfraser/CombineSamurai2/submovie0/Lev3/ApparentLev3_2_30/Traj.pvd'# Trajectory of Spinning Blackhole data location

Trajectory_AhB = '/mnt/raid-project/nr/pfraser/CombineSamurai2/submovie0/Lev3/ApparentLev3_1_30/Traj.pvd'# Trajectory of Non-spinning Blackhole data location


# sets the initial scene
RenderView = GetRenderView()

RenderView.CenterAxesVisibility = 0
RenderView.OrientationAxesVisibility = 0
RenderView.CenterOfRotation = [0, 0, -1*(10**(-20))]
RenderView.CameraViewAngle = InspiralAngleOfView
RenderView.MaintainLuminance = 1


RenderView.ViewSize = [resx, resy]
RenderView.CameraFocalPoint = [0, 0, 0 ]
RenderView.CameraViewUp = [0.561747910539, -0.311326750420212, 0.766495231216645]
RenderView.Background2 = [0.0, 0.0, 0.16470588235294117]
RenderView.Background = [0.10196078431372549, 0.10980392156862745, 0.1411764705882353]
RenderView.LightSwitch = 1


# reads in AhA data 
AhAread = OpenDataFile(AhA)
# applies the filters to AhA 
AhAExtractSurface = ExtractSurface()
AhAGenerateSurfaceNormals = GenerateSurfaceNormals()
AhATemporalInter = TemporalInterpolator()
AhArep = Show()

Contour1 = Contour
AhArep2 = Show()
AhArep2.EdgeColor = [0,0,0.5]
AhArep2.DiffuseColor = AhAdiffusecolor

a1_dimless_ricciScalar_AhA_dump_PVLookupTable = lookuptable1
a1_dimless_ricciScalar_AhA_dump_PiecewiseFunction = AhApiecewise
AhArep.ColorArrayName = ('POINT_DATA', 'dimless_ricciScalar_AhA.dump')
AhArep.LookupTable = a1_dimless_ricciScalar_AhA_dump_PVLookupTable

a1_dimless_ricciScalar_AhA_dump_PVLookupTable.ScalarOpacityFunction = a1_dimless_ricciScalar_AhA_dump_PiecewiseFunction

ScalarBarWidgetRepresentation1 = AhAscalarrep


#Reads in AhB
AhBread = OpenDataFile(AhB)
# applies filters to AhB
AhBExtractSurface = ExtractSurface()
AhBGenerateSurfaceNormals = GenerateSurfaceNormals()
AhBTemporalInter = TemporalInterpolator()
AhBrep = Show()

Contour2 = AhBcontour

AhBrep2 = Show()
AhBrep2.EdgeColor = AhBedgecolor
AhBrep2.DiffuseColor = AhBdiffusecolor
a1_dimless_ricciScalar_AhB_dump_PVLookupTable = lookuptable2
a1_dimless_ricciScalar_AhB_dump_PiecewiseFunction = AhBpiecwise

AhBrep.ColorArrayName = ('POINT_DATA', 'dimless_ricciScalar_AhB.dump')
AhBrep.LookupTable = a1_dimless_ricciScalar_AhB_dump_PVLookupTable

a1_dimless_ricciScalar_AhB_dump_PVLookupTable.ScalarOpacityFunction = a1_dimless_ricciScalar_AhB_dump_PiecewiseFunction

#Reads in AhC information
AhCread = OpenDataFile(AhC)
#apply filters to data
AhCExtractSurface = ExtractSurface()
AhCGenerateSurfaceNormals = GenerateSurfaceNormals()
AhCrep = Show()
AhCrep.Opacity = 0

Contour3 = AhCcontour

AhCrep2 = Show()
AhCrep2.EdgeColor = Ahcedgecolor
a1_dimless_ricciScalar_AhC_dump_PVLookupTable = lookuptable3
a1_dimless_ricciScalar_AhC_dump_PiecewiseFunction = AhCpiecewise

AhCrep.ColorArrayName = ('POINT_DATA', 'dimless_ricciScalar_AhC.dump')
AhCrep.LookupTable = a1_dimless_ricciScalar_AhC_dump_PVLookupTable

a1_dimless_ricciScalar_AhC_dump_PVLookupTable.ScalarOpacityFunction = a1_dimless_ricciScalar_AhC_dump_PiecewiseFunction
SetActiveSource(AhCread)

AhCrep3 = Show()
AhCrep3.Representation = 'Wireframe'
AhCrep3.Opacity = 0

AhCrep3.ColorArrayName = ('POINT_DATA', 'dimless_ricciScalar_AhC.dump')
AhCrep3.LookupTable = a1_dimless_ricciScalar_AhC_dump_PVLookupTable

# reads in plane data
planeread = OpenDataFile(plane)

#Apply filters on plane 

planeTemporalInter = TemporalInterpolator()
planeclip = Clip( ClipType = "Sphere")

planerep = Show()

planeclip.InsideOut = 1
planeclip.ClipType = "Sphere"
planeclip.ClipType.Center = planecenter
planeclip.ClipType.Radius = 8.8
a1_Lapse_PVLookupTable = lookuptable4
a1_Lapse_PiecewiseFunction = planepiecewise

planerep.ScalarOpacityFunction = a1_Lapse_PiecewiseFunction
planerep.ColorArrayName = ('POINT_DATA', 'Lapse')
planerep.LookupTable = a1_Lapse_PVLookupTable

a1_Lapse_PVLookupTable.ScalarOpacityFunction = a1_Lapse_PiecewiseFunction


ScalarBarWidgetRepresentation2 = planescalarrep
ScalarBarWidgetRepresentation1.Enabled = 0
ScalarBarWidgetRepresentation2.Enabled = 0

#Read Trajectory AhA data                                                                     
Trajectory_AhAread = OpenDataFile(Trajectory_AhA)
Trajectory_AhArep = Show()

#Read Trajectory AhB data                                                                   
Trajectory_AhBread = OpenDataFile(Trajectory_AhB)
Trajectory_AhBrep = Show()



# sets the tau values for each segment 
tau0 = 0.0
tau1 = 0.4
tau2 = 0.5
tau3 = 0.65
tau4 = 0.80
tau5 = 1.0

# sets the time values for each segment 
t0 = 0.0
t1 = 1610.
t2 = 1610.
t3 = 1619.5
t4 = 1619.5
t5 = 1650 

frame = 0

for tau in linspace(tau0, tau1,  tau1 * Nframes):
	# relation between tau and t ( time) 
    t = t0 + (t1-t0) * (tau - tau0)/(tau1 - tau0)
    print t
    imgfile = output + str(frame).zfill(4) + "image.png"
    RenderView.ViewTime = t
    RenderView.CameraPosition = InspiralCamPos
    Render(RenderView)
    WriteImage(imgfile)
    frame = frame + 1
  
# time remains constant and the fading of plane takes place    
for tau in linspace(tau1, (tau2)/2.0 , (Nframes * (tau2 - tau1))/2.0):
    t = t1
    print t
    f = (tau-tau1)/(tau2/2.0-tau1)  # goes from 0 to 1 during this interval
    planerep.Opacity = 1 - f
    Trajectory_AhArep.Opacity = 1 - f
    Trajectory_AhBrep.Opacity = 1 - f
    Trajectory_AhArep.LineWidth = 2 - 2*f 
    Trajectory_AhBrep.LineWidth = 2 - 2*f 
    imgfile = output + str(frame).zfill(4) + "image.png"
    RenderView.ViewTime = t
    Render(RenderView)
    WriteImage(imgfile)
    frame = frame + 1
    
    
# the camera now zooms in 
for tau in linspace(tau2/2.0, tau2, (Nframes * ( tau2 - tau1)/2.0)):
    t = t1
    f = (tau - tau2/2.0)/(tau2 - tau2/2.0)
    print t
    planerep.Opacity = 0
    Trajectory_AhArep.Opacity = 0
    Trajectory_AhBrep.Opacity = 0
    Trajectory_AhArep.LineWidth = 0
    Trajectory_AhBrep.LineWidth = 0
    curr_CamPos = InspiralCamPos*(1.-f) + MergerCamPos*f
    imgfile =  output + str(frame).zfill(4) + "image.png"
    RenderView.ViewTime = t
    RenderView.CameraPosition = curr_CamPos
    Render(RenderView)
    WriteImage(imgfile)
    frame = frame + 1

# the merger begins 
for tau in linspace(tau2,tau3, Nframes * (tau3 - tau2)/2.0):
    f = (tau - tau2)/(tau3 - tau2)
    t =t2 +  (t3-t2) * f
    print t
    planerep.Opacity = 0
    Trajectory_AhArep.Opacity = 0
    Trajectory_AhBrep.Opacity = 0
    AhCrep3.Opacity = 0
    imgfile = output + str(frame).zfill(4) + "image.png"
    RenderView.ViewTime = t
    RenderView.CameraPosition = MergerCamPos
    Render(RenderView)
    WriteImage(imgfile)
    frame = frame + 1

# the merger takes place 
for tau in linspace(tau3, tau4, Nframes * (tau4 - tau3)):
    change  = (tau - tau3)/(tau4 - tau3)
    t = t3 + (t4-t3) * change
    print t
    planerep.Opacity = 0
    Trajectory_AhArep.Opacity = 0
    Trajectory_AhBrep.Opacity = 0
    AhCrep2.Opacity = change
    AhBrep2.Opacity = 1.- change
    AhArep2.Opacity = 1. - change
    AhArep.Opacity = 1.- change
    AhBrep.Opacity = 1.- change
    AhCrep.Opacity = change
    AhCrep3.Opacity = 1. - change

    imgfile = output + str(frame).zfill(4) + "image.png"
    RenderView.ViewTime = t
    RenderView.ViewSize = [resx, resy]
    RenderView.CameraPosition = MergerCamPos
    Render(RenderView)
    WriteImage(imgfile)
    frame = frame + 1

# the merger has ended 
for tau in linspace(tau4,tau5, Nframes * (tau5 - tau4)):
    change = (tau - tau4)/(tau5 - tau4)
    t = t4 + (t5-t4) * change
    print t
    AhCrep2.Opacity = 1
    AhBrep2.Opacity = 0
    AhArep2.Opacity = 1
    AhArep.Opacity = 0
    AhBrep.Opacity = 0
    AhCrep3.Opacity = 0
    AhCrep.Opacity = 1
    planerep.Opacity = 0
    Trajectory_AhArep.Opacity = 0
    Trajectory_AhBrep.Opacity = 0
    Trajectory_AhArep.LineWidth = 2
    Trajectory_AhBrep.LineWidth = 2
    
    imgfile = output + str(frame).zfill(4) + "image.png"
    RenderView.ViewTime = t
    RenderView.ViewSize = [resx, resy]
    RenderView.CameraPosition = MergerCamPos
    Render(RenderView)
    WriteImage(imgfile)
    frame = frame + 1
