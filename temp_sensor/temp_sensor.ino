
float temp;
int tempPin = 2; // analog input pin
int sampleTime = 1000; // 1 second dafault 
double rsum = 0.0;
int NUM_SAMPLES = 5;
int loopIdx=0;
void setup() 
{
 Serial.begin(9600);
}

void loop() {
  if(loopIdx >= NUM_SAMPLES){
    Serial.println(rsum);
    Serial.println(rsum/(float)NUM_SAMPLES);
    exit(1);
  }
  rsum += getFahrenheit();
  delay(sampleTime);
  loopIdx++;
}


float getFahrenheit(){
  temp = analogRead(tempPin);
//  Serial.print("RAW DATA: ");
//  Serial.print (temp);
//  Serial.println(" ");
  //converts raw data into degrees celsius and prints it out
  // 500mV/1024=.48828125
  temp = temp * 0.48828125;
//  Serial.print("CELSIUS: ");
//  Serial.print(temp);
//  Serial.println("*C ");
  //converts celsius into fahrenheit 
  temp = temp *9 / 5;
  temp = temp + 32;
  //Serial.print("FAHRENHEIT: ");
  //Serial.print(temp);
  //Serial.println("*F");
  return temp;
  }
