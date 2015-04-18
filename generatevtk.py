# black_hole_visualization
creating data format from the simulation
import argparse
import os
import subprocess
import re
import numpy

#want user specified deltat and directory

p = argparse.ArgumentParser(description = "User specified delta t and directory for files")
p.add_argument('--DeltaT', action = 'store', type =float, required=True,
               help="Time-spacing for the output VTK files.")
p.add_argument("dirs", metavar='DIR', nargs='+')
p.add_argument("mpirun", action = 'store', type = str)
args = p.parse_args()
print args
deltat = args.DeltaT
subdirectory_list = args.dirs
mpirun = args.mpirun

#find the current directory
currentdirectory = os.getcwd()
print currentdirectory
## create a list of all the  sub directories
directories_use = []
for dir in subdirectory_list:
    dir = os.path.join(currentdirectory,dir)
    directories_use.append(dir)

print directories_use
# find the t times from spec.out

for directory in directories_use:
    print directory

# TODO:  Use the file TStepperDiag.out instead.
# 1) check that the file exists (if not terminate with error) (done)
# 2) use T_begin = first time in file (done)
# 3) use T_end = second to last time in file (done)

# TODO:  Massage UseTimes to be integer-multiples of DeltaT.
# Example:  DeltaT=50,   T_begin=4789.2, T_end=4969
    #           -> UseTimes=4800, 4850, 4900, 4950 
    filename = directory + "/" + "TStepperDiag.dat"
    if os.path.isfile(filename):
	f = numpy.loadtxt(filename, unpack = True, skiprows = 10)
       # f = open(filename, 'r')
       # lines = f.read()
        EvInfoTimeOutput=f[0]
	print EvInfoTimeOutput
	# re.findall('t=(.*?), step=', lines)
        if len(EvInfoTimeOutput) < 2:
            print "Warning, not enough values in TstepperDiag.out file found"
        T_begin = float(EvInfoTimeOutput[0])
        Test_begin = T_begin
        multiples_begin = T_begin % deltat
        if int(T_begin) <  T_begin:
                Test_begin = T_begin + 1
        i = 0
        while i  < 10:
            multiples_begin =int(Test_begin) % deltat
            if multiples_begin == 0:
                T_begin = Test_begin
            else:
                Test_begin = int(T_begin) + i 

            i  = i + 1

        T_end = float(EvInfoTimeOutput[-1])
	Test_end = T_end
	multiples_end = T_end % deltat
	if int(T_end) > T_end:
		Test_end = T_end - 1
	j = 0 		
        while j < 10:
            multiples_end = Test_end % deltat
            if multiples_end == 0:
                T_end = Test_end
            else:
            	Test_end = int(T_end) - j
            
            j = j + 1


        print "TimeInterval detected [{}, {}]".format(T_begin,
                                                  T_end)
        usetimes = numpy.arange(T_begin, T_end, deltat)

        args = ['-o','ConvertToVtk(Input=; Basename=VtkDomain; Coords=GridToInertial::MappedCoords; SdNumber=yes; SdSize=yes;)','SpatialCoordMap.input']

    # TODO:  add a command-line option to choose whether to add 
    # 'mpirun -np 1'.  Default this option to 'no mpirun'
        if mpirun == 'yes':
            mp = ['mpirun', '-np', '1']
            cmd = mp + ['ApplyObservers',
           '-UseTimes='+ ','.join([str(t) for t in usetimes])] + args
            os.chdir(directory)
            subprocess.call(cmd)
        if mpirun == 'no':
            cmd = ['ApplyObservers',
                   '-UseTimes='+ ','.join([str(t) for t in usetimes])] + args
            os.chdir(directory)
            subprocess.call(cmd)

    else:
        print "error file", filename, "does not exist"
