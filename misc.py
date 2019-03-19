def colorPrint(text):
	'''
	INPUTS:
	- text:
	A string that the user wants to print in the terminal.
	
	OUTPUTS:
	- text printed in the terminal as black text on a white background.
	'''
	
	# String to be used with the standard print() function to set the text color to
	# black and the background color to white.
	CRED = '\033[7m'
	
	# String to be used with the standard print() function to set the print output
	# to the standard white text on black background.
	CEND = '\033[0m'
	
	# Set the format of the print output to the black text on white background
	# one. Print the input text and set the print format back to the standard one.
	print(CRED + text + CEND)