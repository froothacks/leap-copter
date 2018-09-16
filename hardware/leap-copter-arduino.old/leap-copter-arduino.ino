#include <string.h>
#include <Servo.h>
#include <SoftwareSerial.h>

#define PIN_A_OUT 6
#define PIN_E_OUT 9
#define PIN_T_OUT 10
#define PIN_R_OUT 11
#define PIN_RC_OVERRIDE 7

#define PIN_A_IN A0
#define PIN_E_IN A1
#define PIN_T_IN A2
#define PIN_R_IN A3

Servo servoA, servoE, servoT, servoR;

SoftwareSerial btSerial(2, 3); // RX, TX

char messageType;
int valA, valE, valT, valR;

void setup() {
  btSerial.begin(38400);
  Serial.begin(9600);

  servoA.attach(PIN_A_OUT);
  servoE.attach(PIN_E_OUT);
  servoT.attach(PIN_T_OUT);
  servoR.attach(PIN_R_OUT);

  delay(1000);
}

void loop() {
  // Get Leap Motion data
  while (btSerial.available()) {
    char inByte = btSerial.read();

    if (messageType) {
      int val = 0;
      if (inByte > 0) {
        val = map(inByte, 1, 255, 0, 180);
      }

      if (messageType == 'p') {
        valE = (val) ? val : getRC(PIN_E_IN);
      }
      else if (messageType == 'r') {
        valA = (val) ? val : getRC(PIN_A_IN);
      }
      else if (messageType == 't') {
        valT = (val) ? val : getRC(PIN_T_IN);
      }
      messageType = 0;
    }
    else if (strchr("prt", inByte)) {
      messageType = inByte;
    }
  }

  if (digitalRead(PIN_RC_OVERRIDE)) {
    // Repeat RC data
    valA = getRC(PIN_A_IN);
    valE = getRC(PIN_E_IN);
    valT = getRC(PIN_T_IN);
  }

  // Always use RC rudder channel
  valR = getRC(PIN_R_IN);

  servoA.write(valA);
  servoE.write(valE);
  servoT.write(valT);
  servoR.write(valR);

  Serial.print(valA);
  Serial.print("\t");
  Serial.print(valE);
  Serial.print("\t");
  Serial.print(valT);
  Serial.print("\t");
  Serial.print(valR);
  Serial.println();
}

int getRC(int pin) {
  return map(analogRead(pin), 0, 1023, 0, 180);
}
