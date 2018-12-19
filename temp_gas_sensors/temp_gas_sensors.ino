float temp;
int temp_sensor = 2; // analog input pin
int gas_sensor = 0; //GAS sensor output pin to Arduino analog A0 pin
int sample_time = 1000; // 1 second dafault 

void setup() 
{
 Serial.begin(9600);
}

void loop() {

  get_temp();
  get_gas(
  Serial.println(analogRead(gas_sensor));
  delay(sample_time);
}



double get_gas(){
  int i;
  float gas_value;
  for (i = 0 ; i < 50 ; i++) {
    gas_value = gas_value + analogRead(gas_sensor); //Add analog values of sensor 500 times
  }
  gas_value = gas_value/50;
  Serial.print("Gas Value: ");
  Serial.println(gas_value);
  
}


double get_temp(){
  temp = analogRead(temp_sensor);
  //Serial.print("RAW DATA: ");
  //Serial.print (temp);
  //Serial.println(" ");
  //converts raw data into degrees celsius and prints it out
  // 500mV/1024=.48828125
  temp = temp * 0.48828125;
  Serial.print("CELSIUS: ");
  Serial.print(temp);
  Serial.println("*C ");
  //converts celsius into fahrenheit 
  temp = temp *9 / 5;
  temp = temp + 32;
  Serial.print("FAHRENHEIT: ");
  Serial.print(temp);
  Serial.println("*F ");
  
  }
