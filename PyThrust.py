import subprocess
import platform
import os
from DataImport import *

def thrust(t, data):
	'''
	INPUTS:
	- t:
	The point in time of the test flight (given in seconds)
	for which the thrust levels should be calculated.
	
	- data:
	An instance of the importData class from the ImportData
	module.
	
	OUTPUTS:
	- The thrust level of the left engine and the thrust level of
	the right engine. Both are given in Newtons.
	
	REQUIREMENTS:
	- Either windows or Linux. (I don't know how to do all this
	cross-platform stuff but I tried a very basic os check for Linux/
	Windows as that is what the people working on this project use.)
	- It requires the thrust.exe file as provided under the Flight Dynamics
	part of the Brightspace page of the AE3212-II course. The executable
	needs to be present in the the same directory as the PyThrust module.
	- If running on Linux (at least Ubuntu), wine is required to run the
	thrust.exe file.
	'''
	
	index = list(data.values[48]).index(t)
	
	file = open('matlab.dat', 'w')
	file.write(str(data.values[36][index]*0.3048))
	file.write(' ')
	file.write(str(data.values[39][index]))
	file.write(' ')
	file.write(str(data.values[35][index] - data.values[34][index]))
	file.write(' ')
	file.write(str(data.values[3][index]*0.45359237/3600.))
	file.write(' ')
	file.write(str(data.values[4][index]*0.45359237/3600.))
	file.close()
	
	if platform.platform()[0: 5] == 'Linux': subprocess.call(['wine', 'thrust.exe'], stdout=open(os.devnull, 'wb'))
	else: subprocess.call(['thrust.exe'], stdout=open(os.devnull, 'wb'))
	
	os.remove('matlab.dat')
	
	thrust_data_file = open('thrust.dat', 'r')
	thrust_data = thrust_data_file.readline()
	thrust_data_file.close()
	
	os.remove('thrust.dat')
	
	thrust_data = thrust_data.rstrip('\n').split('\t')
	
	return float(thrust_data[0]), float(thrust_data[1])

'''
### TEST BIT ###
datafile = 'RefData.mat'
data = importData(datafile)

thrust = thrust(680, data)
print('thrust:')
print(thrust)
'''