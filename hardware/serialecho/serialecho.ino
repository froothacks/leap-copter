char inByte;

void setup() {
  pinMode(13, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    inByte = Serial.read();

    digitalWrite(13, HIGH);
    delay(80);
    digitalWrite(13, LOW);
    delay(80);

    Serial.print(inByte);
  }
}
