using namespace std;

#include <iostream>
#include <wiringPi.h>
#include <csignal>
 
const int red = 24;
const int yellow = 5;
const int green = 16;

const string password = "testing";

int main () {
	
	string input;
	
	wiringPiSetupGpio();
	
	pinMode(red, OUTPUT);
	pinMode(yellow, OUTPUT);
	pinMode(green, OUTPUT);
	
	while (true) {
		cout << "Enter the password: ";
		cin >> input;
		
		if (input == "quit") {
			digitalWrite(green, LOW);
			digitalWrite(yellow, LOW);
			digitalWrite(red, LOW);
			return 0;
		}
		
		if (input == password) {
			digitalWrite(green, HIGH);
			digitalWrite(yellow, LOW);
			digitalWrite(red, LOW);
		} else if (input.length() == password.length()) {
			digitalWrite(yellow, HIGH);
			digitalWrite(red, LOW);
			digitalWrite(green, LOW);
		} else {
			digitalWrite(red, HIGH);
			digitalWrite(green, LOW);
			digitalWrite(yellow, LOW);
		}	
	}
}