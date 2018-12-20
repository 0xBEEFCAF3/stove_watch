float temp;
int temp_sensor = 2; // analog input pin
int gas_sensor = 0; //GAS sensor output pin to Arduino analog A0 pin
int sample_time = 1000; // 1 second dafault 

void setup() 
{
 Serial.begin(9600);
}

void loop() {
  float cur_temp;
  float cur_gas;
  String JSON_object;

  if (Serial.available() > 0) {
    // read the incoming byte:
    //incomingByte = Serial.read();
    cur_temp = get_temp();
    cur_gas = get_gas();
    JSON_object = "{'temp':"+(String)cur_temp+",'gas':"+(String)cur_gas+"}";
    Serial.println(JSON_object);
  }
    delay(sample_time);    
}

float get_gas(){
  int i;
  float gas_value;
  for (i = 0 ; i < 50 ; i++) {
    gas_value = gas_value + analogRead(gas_sensor); //Add analog values of sensor 500 times
  }
  gas_value = gas_value/50;
  // Serial.print("Gas Value: ");
  // Serial.println(gas_value);
  return gas_value;
}


float get_temp(){
  temp = analogRead(temp_sensor);
  //Serial.print("RAW DATA: ");
  //Serial.print (temp);
  //Serial.println(" ");
  //converts raw data into degrees celsius and prints it out
  // 500mV/1024=.48828125
  temp = temp * 0.48828125;
  // Serial.print("CELSIUS: ");
  // Serial.print(temp);
  // Serial.println("*C ");
  //converts celsius into fahrenheit 
  temp = temp *9 / 5;
  temp = temp + 32;
  // Serial.print("FAHRENHEIT: ");
  // Serial.print(temp);
  // Serial.println("*F ");

  return temp;
  
  }
