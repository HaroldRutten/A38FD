import numpy as np
import scipy.io as sio
from misc import *

class importData:
	def __init__(self, datafile, print_info=False):
		if print_info: colorPrint('Start importing the data:')
		
		input = sio.loadmat(datafile)['flightdata'][0][0]
		
		self.variables = []
		self.values = []
		self.units = []
		self.n = 0
		
		for i in range(len(input)):
			# Extract the arrays that hold the information about the specific variable.
			variable_name = input[i][0][0][2]
			variable_unit = input[i][0][0][1]
			variable_values = input[i][0][0][0]
			
			# Format the variable name.
			if type(variable_name[0]) == np.str_: variable_name = variable_name[0]
			elif len(variable_name[0][0]) == 0: variable_name = ''
			else: variable_name = variable_name[0][0][0]
			
			# Format the variables unit.
			if type(variable_unit[0]) == np.str_: variable_unit = variable_unit[0]
			elif len(variable_unit[0][0]) == 0: variable_unit = '-'
			else: variable_unit = variable_unit[0][0][0]
			
			# Format the values.
			if len(variable_values) == 1: variable_values = variable_values[0]
			else: variable_values = variable_values[:, 0]
			
			if print_info:
				print(variable_name)
				print(variable_unit)
				print(variable_values)
				print('\n')
			
			self.variables.append(variable_name)
			self.values.append(variable_values)
			self.units.append(variable_unit)
			self.n += 1
	
	def printVariables(self):
		colorPrint('The variables for which flight data is available:')
		for i in range(self.n):
			print('%i. %s %s' % (i, self.variables[i], '[' + self.units[i] + ']'))
		print()

'''
### TEST BIT ###
datafile = 'RefData.mat'
data = importData(datafile)

colorPrint('The variables for which data is available:')
for variable_name in data.values: print(variable_name)
print(data.n)
'''