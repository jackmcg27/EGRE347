'''
-----------------------------------------------------------------------
 File : main.py

 Programmer: Jack McGowan

 Program #: Final Design Project

 Due Date: 5/3/22

 Course: EGRE 347, Spring 2022

 Pledge: I have neither given nor received unauthorized aid on this program.

 Description: This is the main file for the program that can contain a database of
			  transferfunctions for circuits based on resistance, inductance, and 
			  capacitance. This file serves as the driver that determines what
			  functions need to be run based on user input.

-----------------------------------------------------------------------
'''

import transferFunctions

print("Program to evaluate passive RLC filters\n---------------------------------------\n")
savedCircuits = [] #List where all circuits will be added to

#The while loop executes until program is exited
while True:
	transferFunctions.turnOffLEDS()
	transferFunctions.displayMenu()
	selection = input("\nWhat would you like to do? ")
	if selection.isnumeric(): #Checking to make sure selection is valid
		if selection == "0": #Adding circuit to list
			savedCircuits.append(transferFunctions.addCircuit())
		elif selection == "1": #Display circuits
			if len(savedCircuits) == 0:
				print("There are currently no saved circuits!")
			else:
				transferFunctions.displayCircuits(savedCircuits)
		elif selection == "2": #Deleting circuit
			hold = ""
			transferFunctions.displayCircuits(savedCircuits)
			while not hold.isnumeric():
				hold = input("Which circuit would you like to delete? ")
			hold = int(hold) #index of circuit to delete
			if hold >= len(savedCircuits): #Make sure there is a circuit at the index
				print("There is currently not that many circuits!\n")
				continue
			del savedCircuits[hold]
			print("\n")
		elif selection == "3": #Display Transfer Function
			hold = ""
			transferFunctions.displayCircuits(savedCircuits)
			#Validating data before calling next function
			while not hold.isnumeric():
				hold = input("Which circuit would you like to see? ")
			hold = int(hold) #index of circuit to use
			if hold >= len(savedCircuits): #Make sure there is a circuit at the index
				print("There is currently not that many circuits!\n")
				continue
			transferFunctions.printTF(savedCircuits[hold])
		elif selection == "4": #Output gain in V/V
			transferFunctions.displayCircuits(savedCircuits)
			hold = ""
			temp = ""
			#Validating data before calling next function
			while not hold.isnumeric():
				hold = input("Which circuit would you like to work with? ")
			hold = int(hold) #index of circuit to use
			if hold >= len(savedCircuits): #Make sure there is a circuit at the index
				print("There is currently not that many circuits!\n")
				continue
			transferFunctions.lightLED(savedCircuits[hold].get("type"))
			while not temp.isnumeric():
				temp = input("What value would you like for \u03C9 (rad/sec)? ")
			temp = round(float(temp), 4) #Value of omega
			print("\nThe gain for " + str(temp) + " rad/sec is: " + str(transferFunctions.calculateOutput(savedCircuits[hold], temp)) + " V/V\n")
		elif selection == "5": #Output dain in dB
			transferFunctions.displayCircuits(savedCircuits)
			hold = ""
			temp = ""
			#Validating data before calling next function
			while not hold.isnumeric():
				hold = input("Which circuit would you like to work with? ")
			hold = int(hold) #index of circuit to use
			if hold >= len(savedCircuits): #Make sure there is a circuit at the index
				print("There is currently not that many circuits!\n")
				continue
			transferFunctions.lightLED(savedCircuits[hold].get("type"))
			while not temp.isnumeric():
				temp = input("What value would you like for \u03C9 (rad/sec)? ")
			temp = round(float(temp), 4) #Value of omega
			print("\nThe gain for " + str(temp) + " rad/sec is: " + str(transferFunctions.calculateOutputdB(savedCircuits[hold], temp)) + " dB\n")
		elif selection == "6":
			print("\n")
			transferFunctions.displayCircuits(savedCircuits)
			hold = bound1 = bound2 = ""
			#Validating data before calling next function
			while not hold.isnumeric():
				hold = input("Which circuit would you like to plot? ")
			hold = int(hold) #index of circuit to use
			if hold >= len(savedCircuits): #Make sure there is a circuit at the index
				print("There is currently not that many circuits!\n")
				continue
			transferFunctions.lightLED(savedCircuits[hold].get("type"))
			while True:
				while not bound1.isnumeric():
					bound1 = input("What is the lower boundary for \u03C9 (rad/sec)? (Must be 0 or greater) ")
				bound1 = int(bound1) #Lower boundary
				if bound1 >= 0:
					break
			while True:
				while not bound2.isnumeric():
					bound2 = input("What is the upper boundary for \u03C9 (rad/sec)? (Must be 0 or greater) ")
				bound2 = int(bound2) #Upper boundary
				if bound2 >= 0:
					break
			transferFunctions.plotMagnitude(savedCircuits[hold], bound1, bound2)
		elif selection == "7":
			break
	else:
		print("That is not an option!\n")
