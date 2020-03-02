const int EN = 12;
const int PWM2 = 11;
const int PWM1 = 10;
const int OCC = 9;
const int analogInPin = A0;

int sensorValue = 0;
float outputVoltage = 0;
float current = 0;

void setup()
{
                        //set all pins as output
  Serial.begin(9600);
  pinMode(EN, OUTPUT);
  pinMode(PWM1, OUTPUT);
  pinMode(PWM2, OUTPUT);
  pinMode(OCC, OUTPUT);
}

void loop(mode)
{
  if (mode == 0) {
                        //Mode 0 means the arduino is awaiting instruction. It sets
                        //both PWM signals to low so the motor is not driven.
    digitalWrite(EN, LOW);
    digitalWrite(PWM1, LOW);
    digitalWrite(PWM2, LOW);
    digitalWrite(OCC, HIGH);
                        //wait 200ms
    delay(200);
  }
  
  if (mode == 1) {
                        //Mode 1 measures current through the motor. It reads the
                        //value of the sensor and calculates the output voltage to
                        //then calculate the current being drawn from the motor
    sensorValue = analogRead(analogInPin);
    outputVoltage = (sensorValue / 1023.0) * 5.0;
    current = outputVoltage * 50; // 20mV/A

    Serial.println(current);
                        //wait 200ms
    delay(200);
  }
  
  if (mode == 2) {
                        //Mode 2 closes the grippers. It drives the motor
                        //forward at full speed by pulling PWM1 High and
                        //PWM2 low, while setting EN to high.
    digitalWrite(EN, HIGH);
    digitalWrite(PWM1, HIGH);
    digitalWrite(PWM2, LOW);
    digitalWrite(OCC, LOW);

  
                        //wait 200ms
    delay(200);
    if (current < 75) {
                        //Stop motor if current gets too low
                        //since reduced current means more pressure
                        //is applied to the payload.
      mode = 0
      digitalWrite(EN, LOW);
      digitalWrite(PWM1, LOW);
      digitalWrite(PWM2, LOW);
      digitalWrite(OCC, HIGH);

    }
  }
  
  if (mode == 3) {
                        //Mode 3 opens the grippers. It pulls PWM2 high and PWM1
                        //low, so the states are reversed thus the direction
                        //of motor rotation reverses to open the grippers.
    digitalWrite(EN, HIGH);
    digitalWrite(PWM1, LOW);
    digitalWrite(PWM2, HIGH);
    digitalWrite(OCC, LOW);

  
                        //wait 200ms
    delay(200);
  }
}
