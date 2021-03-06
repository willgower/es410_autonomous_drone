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
const int EN = 11;
const int PWM2 = 10;
const int PWM1 = 9;
const int OCM = A1;

// Large Battery Current Sensing for energy logging
const int analogInPin = A0;
int sensorValue = 0;
float outputVoltage = 0;
float current = 0;
float grip_curr = 0; //initialise lower than threshold

/////////////////////////////////////////////
//                 Set Up                  //
/////////////////////////////////////////////

void setup() {
  pinMode(EN, OUTPUT);
  pinMode(PWM1, OUTPUT);
  pinMode(PWM2, OUTPUT);
  pinMode(analogInPin, INPUT);
  pinMode(OCM, INPUT);
  
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
  
    while (grip_curr < 0.15) { // Current threshold is 0.15mA
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
  
  while (grip_curr < 0.15) {
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
    int OCM_read = analogRead(OCM);
    float OCM_volt = (OCM_read / 1023.0) * 5.0;
    grip_curr = OCM_volt / 0.5; // 20mV/A
    Serial.println(grip_curr);
  delay(1000);
    
  // wait 2ms
  delay(2);
  }
  else if (mode == 2)
  {
    // Mode 2 closes the grippers
    
    // This function is blocking and will return when they are closed
    closeGrippers();
    float grip_curr = 0; //initialise lower than threshold
    int OCM_read = analogRead(OCM);
    float OCM_volt = (OCM_read / 1023.0) * 5.0;
    grip_curr = OCM_volt / 0.5; // 20mV/A
    Serial.println(grip_curr);
    while (grip_curr > 0.2) {
      stopGrippers();
    }

    Serial.println("grippers_closed");
    delay(1000);
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
