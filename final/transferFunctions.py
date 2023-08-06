'''
-----------------------------------------------------------------------
 File : transferFuntions.py

 Programmer: Jack McGowan

 Program #: Final Design Project

 Due Date: 5/3/22

 Course: EGRE 347, Spring 2022

 Pledge: I have neither given nor received unauthorized aid on this program.

 Description: This is the implementation file for all of the functions needed
			  to run the database of circuits.

-----------------------------------------------------------------------
'''

import math
import matplotlib
import numpy
import RPi.GPIO as GPIO

matplotlib.use('Agg') # Allowing matplotlib to be used without a screen to output to
from matplotlib import pyplot as plt

# For all GPIO control, the following link was used: https://roboticsbackend.com/raspberry-pi-control-led-python-3/
red = 24
yellow = 5
green = 16
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(yellow, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)

def addCircuit():
	"""
	Function that prompts the user for needed values to create a new circuit
	
	This function prompts the user for a filter type, resistacne, capacitance, and inductance.
	It stores all of these values and creates the numerator and denominator for the transfer function
	for the specified filter type. All of the data is stored in a dictionary which is then returned.
	
	Parameters:
	None
	
	Returns:
	circuit: Dictionary contatining type, resistance, capacitance, inductance, and trasnfer function
	"""
	filterType = ""
	#Read and make sure a proper type is entered
	while True:
		filterType = input("What type of filter would you like? (Lowpass, Highpass, Bandpass): ").lower()
		if filterType == "lowpass" or filterType == "highpass" or filterType == "bandpass":
			break
	lightLED(filterType)
	#Read an make sure a valid resistance is entered
	while True:
		resistance = input("What is the resistance value in ohms (Must be greater than 0)? ")
		resisHold = resistance.replace(".", "")
		if resisHold.isnumeric():
			resistance = float(resistance)
		else:
			continue
		if resistance > 0:
			break
	#Read and validate capacitance
	while True:
		capacitance = input("What is the capacitance value in microfarads (Must be greater than 0)? ")
		capHold = capacitance.replace(".", "")
		if capHold.isnumeric():
			capacitance = float(capacitance) * 10**(-6) #Converting from nanoF to F
		else:
			continue
		if capacitance > 0:
			break
	#Read and validate inductance
	while True:
		inductance = input("what is the inductance value in millihenries (Must be greater than 0)? ")
		inducHold = inductance.replace(".", "")
		if inducHold.isnumeric():
			inductance = float(inductance) * 10**(-3) #Converting from mH to H
		else:
			continue
		if inductance > 0:
			break
	numerator = ""
	denominator = ""
	#Create numerator and denominator based on filter type
	if filterType == "lowpass":
		hold = lowpassTF(resistance, inductance, capacitance)
	elif filterType == "highpass":
		hold = highpassTF(resistance, inductance, capacitance)
	elif filterType == "bandpass":
		hold = bandpassTF(resistance, inductance, capacitance)
	
	circuit = dict(type = filterType, R = resistance, L = inductance, C = capacitance, numerator=hold[0], denominator=hold[1])
	print("\n")
	return circuit #Return dictionary to be added to list

def printTF(c):
	"""
	Function that prints the transfer function of a circuit
	
	This function prints the transfer function of a circuit in the form of a fraction that is easy
	for a user to read
	
	Parameters:
	c (dictionary): Dictionary containing all of the data for a circuit
	
	Returns:
	None
	*Note that the transfer function will be printed to the terminal
	"""
	num = c.get("numerator")
	den = c.get("denominator")
	print(num.center(len(den)))
	for i in range(0, len(den)):
		print("-", end='')
	print("\n" + den)
	print("\n")
	
def lowpassTF(R, L, C):
	"""
	Function that creates the numerator and denominator for a low pass circuit
	
	This function takes in the resistance, inductance, and capacitance of a circuit
	and computes the numerator and denominator of a low pass circuit's transfer function
	
	Parameters:
	R (float): Resistance value ohms
	L (float): Inductance value in mH
	C (float): capacitance value in nanoFarads
	
	Returns:
	numerator: string containing the numerator of a low pass transfer function
	denominator: string containing the denominator of a low pass transfer function
	"""
	#The hold variables are for constants based on circuit components
	holdLC = str(round(1 /  (C * L), 4))
	holdRL = str(round(R / L, 4))
	numerator = str(holdLC)
	denominator = "-\u03C9^2 + j" + holdRL + "\u03C9 + " + holdLC
	return numerator, denominator
	
def highpassTF(R, L, C):
	"""
	Function that creates the numerator and denominator for a high pass circuit
	
	This function takes in the resistance, inductance, and capacitance of a circuit
	and computes the numerator and denominator of a high pass circuit's transfer function
	
	Parameters:
	R (float): Resistance value ohms
	L (float): Inductance value in mH
	C (float): capacitance value in nanoFarads
	
	Returns:
	numerator: string containing the numerator of a high pass transfer function
	denominator: string containing the denominator of a high pass transfer function
	"""
	#The hold variables are for constants based on circuit components
	holdLC = str(round(1 /  (C * L), 4))
	holdRL = str(round(R / L, 4))
	numerator = "-\u03C9^2"
	denominator = "-\u03C9^2 + j" + holdRL + "\u03C9 + " + holdLC
	return numerator, denominator	

def bandpassTF(R, L, C):
	"""
	Function that creates the numerator and denominator for a band pass circuit
	
	This function takes in the resistance, inductance, and capacitance of a circuit
	and computes the numerator and denominator of a band pass circuit's transfer function
	
	Parameters:
	R (float): Resistance value ohms
	L (float): Inductance value in mH
	C (float): capacitance value in nanoFarads
	
	Returns:
	numerator: string containing the numerator of a band pass transfer function
	denominator: string containing the denominator of a band pass transfer function
	"""
	#The hold variables are for constants based on circuit components
	holdLC = str(round(1 /  (C * L), 4))
	holdRL = str(round(R / L, 4))
	numerator = "j" + holdRL + "\u03C9"
	denominator = "-\u03C9^2 + j" + holdRL + "\u03C9 + " + holdLC
	return numerator, denominator
	
def calculateOutput(c, omega):
	"""
	Function that calcualtes the output in V/V of a circuit given a frequency
	
	This function takes a circuit and calculates the output of a given angular frequency in rad/sec.
	It takes the transfer function numerator and denominator and substitutes in omega and calculates
	from there.
	
	Parameters:
	c (dictionary): Dictionary containing the data for a circuit
	omega (float): frequency to be calculated with
	
	Returns:
	gain (float): Result of the numerator divided by the denominator rounded to 4 sig figs
	"""
	num = c.get("numerator")
	den = c.get("denominator")
	if "j" in num: #Replacing omega
		num = num.replace("\u03C9", "*" + str(omega))
	else:
		num = num.replace("\u03C9", str(omega))
	num = num.replace("j", "").replace("^", "**") #Removing "j" and changing exponents to form to evaluate
	numAnswer = round(eval(num),4) #Value from numerator
	numMag = calculateMagnitude(numAnswer, 0) #Magnitude from numerator... only ever all real or all imaginary, so use 0 as 2nd argument
	den = den.replace("^", "**")
	denSplit = den.split()
	imag = real = ""
	for element in denSplit:
		if "j" in element:
			imag += element.replace("j", "").replace("\u03C9", "*" + str(omega)) #Creating string containing all imaginary terms
		else:
			real += element.replace("\u03C9", str(omega)) #Creating string with all real terms
	real = real.replace("++" , "+")
	imagAns = eval(imag)
	realAns = eval(real)
	denMag = calculateMagnitude(realAns, imagAns)
	gain = round(numMag / denMag, 4) #Calculating final output
	if gain > 1: #All filters are passive so if rounding causes > 1, it must be rounded down as it is not possible to go over 1
		gain = 1.0
	elif gain <= 0: #Nothing ever goes to 0... also true 0 causes issues in other functions
		gain = 0.0001
	return gain
	
def calculateOutputdB(c, omega):
	"""
	Function that calcualtes the output in dB of a circuit given a frequency
	
	This function takes a circuit and calculates the output of a given angular frequency in rad/sec.
	It takes the transfer function numerator and denominator and substitutes in omega and calculates
	from there. Given this value, it converts it to decibals for a log scale
	
	Parameters:
	c (dictionary): Dictionary containing the data for a circuit
	omega (float): frequency to be calculated with
	
	Returns:
	output (float): Result of the gain converted to a log scale
	"""
	output = calculateOutput(c, omega) #Getting gain in V/V
	output = round(20 * math.log(output), 4) #Convert to dB log scale
	if  output > 0: #Passive filters so can't be above 0
		output = 0
	return output

def calculateMagnitude(real, imag):
	"""
	Function that calcualtes the magnitude of a complex number
	
	This function takes a real and imaginary part and performs the calcualtions
	needed to make it a magnitude
	
	Parameters:
	real (float): real component of a complex number
	imag (float): imaginary component of a complex number
	
	Returns:
	result of the square root of the real part squared plus the imag part squared, rounded
	to 4 sig figs
	"""
	realSq = real**2
	imagSq = imag**2
	return round(math.sqrt(realSq + imagSq), 4)
	
def plotMagnitude(c, lower, upper):
	"""
	Function that plots the magnitude response of a circuit
	
	This function takes a circuit and upper and lower boundaries and plots the magnuitude as the function
	circuit is given frequencies from the lower and upper boundaries. The plot is then output as a jpg to 
	the same folder the program is run from
	
	Parameters:
	c (dictionary): Dictionary containing the data for a circuit
	lower (int): Lowest frequency for the graph
	upper (int): Upper frequency for the graph
	
	Returns:
	None
	*Note that a file will be created/overwritten with the graph
	"""
	x = numpy.arange(lower, upper, 0.1) #https://numpy.org/doc/stable/reference/generated/numpy.arange.html#numpy.arange
	y = []
	print("Please wait while the function is calculated (this may take a few seconds depending on your domain of \u03C9)")
	for i in numpy.arange(lower, upper, 0.1):
		y.append(calculateOutputdB(c,i))
	#Used for all graphing: https://matplotlib.org/stable/plot_types/index
	plt.clf()
	plt.semilogx(x, y)
	plt.title("Magnitude Response")
	plt.xlabel("\u03C9 (rad/sec)")
	plt.ylabel("Magnitude (dB)")
	plt.grid(True, which="both") #https://stackoverflow.com/questions/3590905/how-do-i-show-logarithmically-spaced-grid-lines-at-all-ticks-on-a-log-log-plot-u
	plt.savefig("magnitudePlot.jpg")
	print("\n")
	
def displayMenu():
	"""
	Function that displays the main menu
	
	This function prints out the main menu with the options for the user
	to choose from
	
	Parameters:
	None
	
	Returns:
	None
	*Note that the options will be output to the terminal
	"""
	print("Options:\n")
	print("(0) Add a new circuit")
	print("(1) See current saved circuits")
	print("(2) Delete saved circit")
	print("(3) Output a transfer function")
	print("(4) Calculate gain for a circuit in V/V for specified \u03C9")
	print("(5) Calculate gain for a circuit in dB for specified \u03C9")
	print("(6) Graph magnitude plot of circuit")
	print("(7) Exit program")
	
def displayCircuits(circuits):
	"""
	Function that displays the saved circuits in a way for users to see them easily
	
	This function takes a list of circuits and outputs them all with the type and all their
	component values for the user to see and make selections off of
	
	Parameters:
	circuits (list): List containing dictionaries with the data for circuits
	
	Returns:
	None
	*Note that the circuits will all be output to the terminal
	"""
	print("Current saved circuits:\n")
	for i in range(len(circuits)):
		print("(" + str(i) + ") " + circuits[i].get("type").title() + " filter with R = " + str(round(circuits[i].get("R"), 4)) + " \u03A9, L = " + str(round(circuits[i].get("L") * 10**3, 4)) + " mH, and C = " + str(round(circuits[i].get("C") * 10**6, 4)) + " \u03BCF")
	print("\n")
	
def lightLED(type):
	"""
	Function that lights corresponding LEDs to the filter types
	
	This function takes a type of a circuit and lights the correct LED. Green means it is
	currently working with a lowpass circuit, yellow is bandpass, and red is highpass
	
	Parameters:
	type (string): String with filter type
	
	Returns:
	None
	*Note that the LED states will be changed
	"""
	if type == "lowpass":
		GPIO.output(green, GPIO.HIGH)
		GPIO.output(yellow, GPIO.LOW)
		GPIO.output(red, GPIO.LOW)
	elif type == "bandpass":
		GPIO.output(green, GPIO.LOW)
		GPIO.output(yellow, GPIO.HIGH)
		GPIO.output(red, GPIO.LOW)
	elif type == "highpass":
		GPIO.output(green, GPIO.LOW)
		GPIO.output(yellow, GPIO.LOW)
		GPIO.output(red, GPIO.HIGH)

def turnOffLEDS():
	"""
	Function that turns off all LEDs
	
	This function turns all of the LEDs off
	
	Parameters:
	None
	
	Returns:
	None
	*Note that all the LEDs will be turned off
	"""
	GPIO.output(green, GPIO.LOW)
	GPIO.output(yellow, GPIO.LOW)
	GPIO.output(red, GPIO.LOW)