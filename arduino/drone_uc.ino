// ES410 Autonomous Drone
// Owner: Aaron Sodhi
// File: drone_uc.ino
// Description: Module to control gripper system and report battery current back to RPi


/////////////////////////////////////////////
//               Constants                 //
/////////////////////////////////////////////

// Generic
int mode = 0;

// Motor current sensing for force detection
const int EN = 12;
const int PWM2 = 11;
const int PWM1 = 10;
const int OCC = 9;
int torque;

// Large Battery Current Sensing for energy logging
const int analogInPin = A0;
int sensorValue = 0;
float outputVoltage = 0;
float current = 0;

/////////////////////////////////////////////
//                 Set Up                  //
/////////////////////////////////////////////

void setup() {
  pinMode(EN, OUTPUT);
  pinMode(PWM1, OUTPUT);
  pinMode(PWM2, OUTPUT);
  pinMode(OCC, OUTPUT);
  pinMode(analogInPin, INPUT);
  
  Serial.begin(9600);
  
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
}


/////////////////////////////////////////////
//          Function Definitions           //
/////////////////////////////////////////////

void openGrippers() {
  // Code here to open the grippers
  
  // It pulls PWM2 high and PWM1 low, this
  // reverses the motor direction to open the grippers
  
  digitalWrite(EN, HIGH);
  digitalWrite(PWM1, LOW);
  digitalWrite(PWM2, HIGH);
  digitalWrite(OCC, LOW);
  
    while (torque < 50) { // This is dependent on the torque constant being reduced as the motor begins to grip package
    // Stay in this loop while the grippers open up to the end stoppers
    continue;
  }
  
  // Now the torque has reached the threshold - stop closing
  stopGrippers();
}

void closeGrippers() {
  // Code here to close the grippers
  
  // It drives the motor forward at full speed by
  // pulling PWM1 High and PWM2 low, while setting EN to high.
  digitalWrite(EN, HIGH);
  digitalWrite(PWM1, HIGH);
  digitalWrite(PWM2, LOW);
  digitalWrite(OCC, LOW);
  
  while (torque < 50) {
    // Stay in this loop while the grippers close in around the box
    continue;
  }
  
  // Now the torque has reached the threshold - stop closing
  stopGrippers();
}

void stopGrippers() {
  // Code here to stop the grippers wherever they are
  
  // both PWM signals to low so the motor is not driven.
  digitalWrite(EN, LOW);
  digitalWrite(PWM1, LOW);
  digitalWrite(PWM2, LOW);
  digitalWrite(OCC, HIGH);
}

/////////////////////////////////////////////
//            Start Main Loop              //
/////////////////////////////////////////////

void loop() {
  if (Serial.available() > 0) {
    // read the incoming number
    mode = Serial.parseInt();
  }
  
  if (mode == 0) {
    // Mode 0 means the arduino is awaiting instruction
    
    // Make sure the grippers arent moving but do nothing else
    stopGrippers();
    
    delay(100);
  }
  else if (mode == 1)
  {
    // Mode 1 measures current through the motor. It reads the
    // value of the sensor and calculates the output voltage to
    // then calculate the current being drawn from the motor
    sensorValue = analogRead(analogInPin);
    outputVoltage = (sensorValue / 1023.0) * 5.0;
    current = outputVoltage * 50; // 20mV/A
    Serial.println(current);
    
    // wait 2ms
    delay(2);
  }
  else if (mode == 2)
  {
    // Mode 2 closes the grippers
    
    // This function is blocking and will return when they are closed
    closeGrippers();

    Serial.println("grippers_closed");
    // Return to IDLE state
    mode = 0;
  }
  else if (mode == 3)
  {
    // Mode 3 opens the grippers
    
    // This function is blocking and will return when they are opened
    openGrippers();

    Serial.println("grippers_opened");
    // Return to IDLE state
    mode = 0;
  }
}
