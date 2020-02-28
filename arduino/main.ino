const int analogInPin = A0;

int sensorValue = 0;
float outputVoltage = 0;
float current = 0;

const int PWM1 = 3;
const int EN = 4;
const int PWM2 = 5;


void setup()
{
  Serial.begin(9600);
                        //set all pins as output
  pinMode(PWM1, OUTPUT);
  pinMode(PWM2, OUTPUT);
  pinMode(EN, OUTPUT);
}

void loop()
{
  sensorValue = analogRead(analogInPin);
  outputVoltage = (sensorValue / 1023.0) * 5.0;
  current = outputVoltage * 50; // 20mV/A

  Serial.println(current);
  
  delay(200);
                        //drive forward at full speed by pulling PWM1 High
                        //and PWM2 low, while writing a full 255 to EN to
                        //control speed
  digitalWrite(PWM1, HIGH);
  digitalWrite(PWM2, LOW);
  analogWrite(EN, 255);

                        //wait 1 second
  delay(1000);

                        //Brake the motor by pulling both direction pins to
                        //the same state (in this case LOW). PWMA doesn't matter
                        //in a brake situation, but set as 0.
  digitalWrite(PWM1, LOW);
  digitalWrite(PWM2, LOW);
  analogWrite(EN, 0);

                        //wait 1 second
  delay(1000);

                        //change direction to reverse by flipping the states
                        //of the direction pins from their forward state
  digitalWrite(PWM1, LOW);
  digitalWrite(PWM2, HIGH);
  analogWrite(EN, 150);

                        //wait 1 second
  delay(1000);

                        //Brake again
  digitalWrite(PWM1, LOW);
  digitalWrite(PWM2, LOW);
  analogWrite(EN, 0);

                        //wait 1 second
  delay(1000);
}
