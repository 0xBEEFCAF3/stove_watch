#!/usr/bin/python



"""
@author: Armin
"""
from serial import Serial 
import time
import json

def formatHTML(isON, results):
	bg_color = "bg-danger" if isON else "bg-success";
	is_on_text = "ON" if isON  else  "OFF";

	html = "Content-type: text/html\n\n";

	html += """<!doctype html>
	<html lang="en">
	  <head>
	    <!-- Required meta tags -->
	    <meta charset="utf-8">
	    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

	    <!-- Bootstrap CSS -->
	    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">

	    <title>Stove Watch</title>
	  </head>
	  <body>
	    <div class="container">
	      <h1>Stove Watch</h1>
	            
	      <h3>Results:</h3>
	      <button type="button" class="btn btn-info">Run again!</button>
	      <hr>
	      <div class="jumbotron jumbotron-fluid """ + bg_color + """> <!-- bg-success  -->
	      <div class="container">
	        <h1 class="display-4">Your stove is: """ + is_on_text +"""</h1>
	        <p class="lead">Sensor Readings</p>
	        <p class="lead">""" + str(results) + """</p>
	      </div>
	    </div>
	    </div>

	    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
	    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
	    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
	    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
	  </body>
	  <script>
	    $(document).ready(function(){
	      $("button").click(function(){
	        location.reload();
	      });
	    });

	  </script>
	</html>"""
	print(html)

def isON(vals):
	for val in vals:
		if(val["temp"] > 80 or val["gas"]>200):
			return True
	return False

def main():
	TIME_BEFORE_CHECK = 15
	GAS_ERROR_VAL = -20
	TEMP_ERROR_VAL = -20

	device_port = '/dev/ttyACM4' 
	arm_port = '/dev/ttyUSB0' 

	arm_serial = Serial(arm_port, 9600)
	device_serial = Serial(device_port, 9600)
	
	response = []

	######## Synchronize #########
	state  = -1

  #arm_serial.write("1\r\n".encode())
	# device_serial.write("1\r\n".encode())
	# device_serial.readline()	

	# while  state != "4":
	# 	print("running loop")
	# 	device_serial.write("1\r\n".encode())
	# 	device_vals = "{}"
	# 	try:
	# 		device_vals = device_serial.readline().split("::")[1].split("\r")[0].replace("'","\"") #
	# 		print("Just read: ", device_vals)
	# 	except :
	# 		print("Malformaties detected	")
	# 		continue

	# 	print("device vals" , device_vals)
	# 	response.append(json.loads(device_vals))

	# 	arm_serial.write("1\r\n".encode())
	# 	print("JUST WROTE TO ARM")
	# 	state = arm_serial.readline().split("\r")[0]

	# 	print("arm state: ", state)
	# 	#time.sleep(5)

  ####STATE 1
	arm_serial.write("1\n".encode())
	device_serial.write("1\r\n".encode())
	try:
			device_vals = device_serial.readline().split("::")[1].split("\r")[0].replace("'","\"") #
			print("Just read: state 1", device_vals)
	except :
			print("Malformaties detected	")
	response.append(json.loads(device_vals))	
	####STATE 2
	state = arm_serial.readline().split("\r")[0]
	arm_serial.write("1\n".encode())
	state = arm_serial.readline().split("\r")[0]
	print("THE CURRENT STATE:::: ", state)
	device_serial.write("1\r\n".encode())
	try:
			device_vals = device_serial.readline().split("::")[1].split("\r")[0].replace("'","\"") #
			print("Just read:  state2", device_vals)
	except :
			print("Malformaties detected	")
	response.append(json.loads(device_vals))	

	####STATE 3
	arm_serial.write("1\n".encode())
	state = arm_serial.readline().split("\r")[0]
	print("THE CURRENT STATE:::: ", state)
	device_serial.write("1\r\n".encode())
	try:
			device_vals = device_serial.readline().split("::")[1].split("\r")[0].replace("'","\"") #
			print("Just read: state3", device_vals)
	except :
			print("Malformaties detected	")
	response.append(json.loads(device_vals))	

	####STATE 4
	arm_serial.write("1\n".encode())
	state = arm_serial.readline().split("\r")[0]
	print("THE CURRENT STATE:::: ", state)
	device_serial.write("1\r\n".encode())
	try:
			device_vals = device_serial.readline().split("::")[1].split("\r")[0].replace("'","\"") #
			print("Just read: state4", device_vals)
	except :
			print("Malformaties detected	")
	response.append(json.loads(device_vals))	

#close serial connection
	device_serial.close()
	arm_serial.close()

	print("DONE", response)
	print(isON(response))

if __name__ == '__main__':
	main()
	#formatHTML(True, [1,2])
