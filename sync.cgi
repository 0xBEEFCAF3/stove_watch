# -*- coding: utf-8 -*-
"""

@author: Armin
"""
from serial import Serial 
import time
import json




def main():
	TIME_BEFORE_CHECK = 15
	GAS_ERROR_VAL = -20
	TEMP_ERROR_VAL = -20

	device_port = '/dev/ttyACM1' 
	arm_port = '/dev/ttyUSB0' 

	arm_serial = Serial(arm_port, 9600)
	device_serial = Serial(device_port, 9600)
	
	response = []

	######## Synchronize #########
	while state = arm_serial.readline() != "-1":
		device_vals = device_serial.readline()
		response.append(json.loads(device_vals))
			
	device_serial.close()
	arm_serial.close()

if __name__ == '__main__':
	main()