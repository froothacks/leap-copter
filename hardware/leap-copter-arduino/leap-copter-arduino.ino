#include <string.h>
#include <Servo.h>
#include <SoftwareSerial.h>
// #include "RCArduinoFastLib.h"

// MultiChannels
//
// rcarduino.blogspot.com
//
// A simple approach for reading three RC Channels using pin change interrupts
//
// See related posts -
// http://rcarduino.blogspot.co.uk/2012/01/how-to-read-rc-receiver-with.html
// http://rcarduino.blogspot.co.uk/2012/03/need-more-interrupts-to-read-more.html
// http://rcarduino.blogspot.co.uk/2012/01/can-i-control-more-than-x-servos-with.html
//
// rcarduino.blogspot.com
// 

// #define SERVO_FRAME_SPACE 4

// #define PIN_A_IN 4
// #define PIN_E_IN 5
// #define PIN_T_IN 6
// #define PIN_R_IN 7

#define PIN_A_OUT 11
#define PIN_E_OUT 10
#define PIN_T_OUT 9

#define PIN_RC_OVERRIDE 8

Servo servoA, servoE, servoT;

SoftwareSerial btSerial(2, 3); // RX, TX

int messageType;
int valA, valE, valT, valR;

// volatile uint32_t ulCounter = 0;

void setup() {
  Serial.begin(115200);
  btSerial.begin(38400);

  // attach servo objects, these will generate the correct
  // pulses for driving Electronic speed controllers, servos or other devices
  // designed to interface directly with RC Receivers 

  // CRCArduinoFastServos::attach(PIN_A_IN,PIN_A_OUT);
  // CRCArduinoFastServos::attach(PIN_E_IN,PIN_E_OUT);
  // CRCArduinoFastServos::attach(PIN_T_IN,PIN_T_OUT);
  // CRCArduinoFastServos::attach(PIN_R_IN,PIN_R_OUT);
  
  // lets set a standard rate of 50 Hz by setting a frame space of 10 * 2000 = 3 Servos + 7 times 2000
  // CRCArduinoFastServos::setFrameSpaceA(SERVO_FRAME_SPACE,6*2000);

  // CRCArduinoFastServos::begin();
  // CRCArduinoPPMChannels::begin();

  servoA.attach(PIN_A_OUT);
  servoE.attach(PIN_E_OUT);
  servoT.attach(PIN_T_OUT);

  delay(1000);
}

void loop() {
  // Get Leap Motion data
  while (btSerial.available()) {
    int inByte = btSerial.read();

    if (messageType) {
      int val = inByte;

      if (messageType == 'p')
        valE = val;
      else if (messageType == 'r')
        valA = val;
      else if (messageType == 't')
        valT = val;

      messageType = 0;
    }
    else if (strchr("prt", inByte)) {
      messageType = inByte;
    }
  }

  // if (digitalRead(PIN_RC_OVERRIDE)) {
  //   // Repeat RC data
  //   valA = 0;
  //   valE = 0;
  //   valT = 0;
  // }

  servoA.write(map(valA, 1, 255, 0, 180));
  servoE.write(map(valE, 1, 255, 0, 180));
  servoT.write(map(valT, 1, 255, 0, 180));


  Serial.print(valA);
  Serial.print("\t");
  Serial.print(valE);
  Serial.print("\t");
  Serial.print(valT);
  Serial.print("\t");
  Serial.print(0);
  Serial.print("\t");
  Serial.print(255);
  Serial.println();

  // delay(0.01);

}
