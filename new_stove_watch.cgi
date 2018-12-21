#!/usr/bin/python


"""
@author: Armin
"""
from serial import Serial 
import time
import json

def formatHTML(isON, results):
	bg_color = "style=\"background-color: #dc3545 !important;color:white;\"" if isON else "style=\"background-color: #28a745 !important;\"";
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
	      <div class="jumbotron jumbotron-fluid"  """+ bg_color + """>
	      <div class="container">
	        <h1 class="display-4">Your stove is: """ + is_on_text +"""</h1>
	        <p class="lead">Sensor Readings</p>
					<table class="table">
					<thead></thead>
					<tbody>
						<tr> 
							<td> """ +str(results[0]) + """ Analog  </td><td>""" +str(results[1]) + """  Analog</td>
						</tr>
						<tr> 
							<td> """ + str(results[2]) +   """ Analog </td><td> """ + str(results[3]) + """ Analog </td>
						</tr>
					<tbody>
					<table
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
#<td> """ + str(results[0]["temp"]) + """F """ + str(results[0]["gas"]) + """ Analog  </td><td>""" + str(results[1]["temp"]) + """F """ + str(results[1]["gas"]) + """  Analog</td>

def isON(vals):
	for val in vals:
		try:
			if(val["temp"] > 85 or val["gas"]>200):
				return True
		except:
			continue
	return False

def main():
	TIME_BEFORE_CHECK = 15


	device_port = '/dev/ttyACM6' 
	arm_port = '/dev/ttyUSB1' 

	arm_serial = Serial(arm_port, 9600)
	device_serial = Serial(device_port, 9600)
	device_vals = "{}"
	response = []

	######## Synchronize #########
	state  = -1

  #arm_serial.write("1\r\n".encode())
	# device_serial.write("1\r\n".encode())
	# device_serial.readline()	

	# while  state != "4":
	# 	#print("running loop")
	# 	device_serial.write("1\r\n".encode())
	# 	device_vals = "{}"
	# 	try:
	# 		device_vals = device_serial.readline().split("::")[1].split("\r")[0].replace("'","\"") #
	# 		#print("Just read: ", device_vals)
	# 	except :
	# 		#print("Malformaties detected	")
	# 		continue

	# 	#print("device vals" , device_vals)
	# 	response.append(json.loads(device_vals))

	# 	arm_serial.write("1\r\n".encode())
	# 	#print("JUST WROTE TO ARM")
	# 	state = arm_serial.readline().split("\r")[0]

	# 	#print("arm state: ", state)
	# 	#time.sleep(5)

  ####STATE 1
	arm_serial.write("1\n".encode())
	device_serial.write("1\r\n".encode())
	try:
			device_vals = device_serial.readline().split("::")[1].split("\r")[0].replace("'","\"") #
			#print("Just read: state 1", device_vals)
	except :
            pass
			#print("Malformaties detected	")
	response.append(json.loads(device_vals))	
	####STATE 2
	state = arm_serial.readline().split("\r")[0]
	arm_serial.write("1\n".encode())
	state = arm_serial.readline().split("\r")[0]
	#print("THE CURRENT STATE:::: ", state)
	device_serial.write("1\r\n".encode())
	try:
			device_vals = device_serial.readline().split("::")[1].split("\r")[0].replace("'","\"") #
			#print("Just read:  state2", device_vals)
	except :
            pass
	#print("Malformaties detected	")
	response.append(json.loads(device_vals))	

	####STATE 3
	arm_serial.write("1\n".encode())
	state = arm_serial.readline().split("\r")[0]
	#print("THE CURRENT STATE:::: ", state)
	device_serial.write("1\r\n".encode())
	try:
			device_vals = device_serial.readline().split("::")[1].split("\r")[0].replace("'","\"") #
			#print("Just read: state3", device_vals)
	except :
            pass
		    #print("Malformaties detected	")
	response.append(json.loads(device_vals))	

	####STATE 4
	arm_serial.write("1\n".encode())
	try:
		state = arm_serial.readline().split("\r")[0]
	except:
		pass
	#print("THE CURRENT STATE:::: ", state)
	device_serial.write("1\r\n".encode())
	try:
			device_vals = device_serial.readline().split("::")[1].split("\r")[0].replace("'","\"") #
			#print("Just read: state4", device_vals)
	except :
            pass
		    #print("Malformaties detected	")
	response.append(json.loads(device_vals))	

    #close serial connection
	device_serial.close()
	arm_serial.close()

	#print("DONE", response)
	formatHTML(isON(response), response)
    
    

if __name__ == '__main__':
	main()
	#formatHTML(True, [1,2])
