#include <Servo.h> 
 
// create "servo objects"
Servo extend, updown, claw, clawturn, base; //extend is left, updown is right servo

int ct_p, extend_p, updown_p, claw_p, base_p;
int updown_flag = 0;
int extend_flag = 0;
int base_flag = 0;
int state_status;
void setup() 
{
  Serial.begin(9600); 
  //20 to 80 is our range for right_p AKA updown
  double vals[4];
  visitAllHotPlates(vals);
}

void visitAllHotPlates(double *vals){
    claw.attach(9);  // attaches the servo on pin 11 to the middle object
    clawturn.attach(10);  
    base.attach(11);
    extend.attach(13); 
    updown.attach(12);
    /*State 1 */
    ct_p = 50;
    claw_p = 50;
    updown_p = 80; //up down, 0 is up
    extend_p = 90; // 90 is retracted in, 10 is extended out
    base_p = 0;//initialization values
    claw.write(claw_p);
    clawturn.write(ct_p);
    updown.write(updown_p);
    extend.write(extend_p);
    base.write(base_p);
    Serial.println("1");
    
    while (Serial.available() < 0) {
        delay(800);
    }
    state_status = Serial.read();
    
    //delay(3000);
    /*State 2 */
    while(updown_p > 20){
      updown_p -= 2;
      updown.write(updown_p);
      delay(35);
    }
    while(extend_p > 40){
      extend_p -= 2;
      extend.write(extend_p);
      delay(35);
    }
    ct_p = 50;
    claw_p = 50;
    updown_p = 40; //up down, 0 is up
    extend_p = 20; // 90 is retracted in, 10 is extended out
    base_p = 0;//initialization values
    claw.write(claw_p);
    clawturn.write(ct_p);
    updown.write(updown_p);
    extend.write(extend_p);
    base.write(base_p);
    Serial.println("2");
    while (Serial.available() < 0) {
        delay(800);
    }
    state_status = Serial.read();
    //delay(3000);
    /*State 3 */
    while(base_p < 45){
      base_p += 2;
      base.write(base_p);
      delay(35);
    }
    ct_p = 50;
    claw_p = 50;
    updown_p = 40; //up down, 0 is up
    extend_p = 20; // 90 is retracted in, 10 is extended out
    base_p = 45;//initialization values
    claw.write(claw_p);
    clawturn.write(ct_p);
    updown.write(updown_p);
    extend.write(extend_p);
    base.write(base_p);
    Serial.println("3");
    while (Serial.available() < 0) {
        delay(800);
    }
    state_status = Serial.read();
    //delay(3000);

    /*State 4 */
    while(ct_p < 180){
      ct_p += 2;  
      clawturn.write(ct_p);
      delay(35);
    }

    while(extend_p > 10){
      extend_p -= 2;  
      extend.write(extend_p);
      delay(35);    
    }

    while(updown_p > 30){
      updown_p -= 2;  
      updown.write(updown_p);
      delay(35);
        
    }
      
    ct_p = 180;
    claw_p = 50;
    updown_p = 30; //up down, 0 is up
    extend_p = 10; // 90 is retracted in, 10 is extended out
    base_p = 30;//initialization values
    claw.write(claw_p);
    clawturn.write(ct_p);
    updown.write(updown_p);
    extend.write(extend_p);
    base.write(base_p);
    Serial.println("4");
    //delay(3000);
}
 
void loop() 
{ 
  
}
