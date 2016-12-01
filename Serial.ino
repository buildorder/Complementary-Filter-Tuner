#include <Wire.h>

#define MPU9250 0x68

int dataBuffer[5];
int i = 0;

void GetData()
{
  Wire.beginTransmission(MPU9250);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU9250, 6, true);

  dataBuffer[0] = Wire.read() << 8 | Wire.read();
  dataBuffer[1] = Wire.read() << 8 | Wire.read();
  dataBuffer[2] = Wire.read() << 8 | Wire.read();

  Wire.beginTransmission(MPU9250);
  Wire.write(0x43);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU9250, 4, true);

  dataBuffer[3] = Wire.read() << 8 | Wire.read();
  dataBuffer[4] = Wire.read() << 8 | Wire.read();
}

void setup() {

  Wire.begin();
  Serial.begin(57600);

  Wire.beginTransmission(MPU9250);
  Wire.write(0x6B); 
  Wire.write(0);
  Wire.endTransmission(true);

  delay(1000);
}

void loop() {

  GetData();

  for(i = 0; i < 4; i++) 
  {
    Serial.print(dataBuffer[i]);
    Serial.print("|");
  }
  Serial.println(dataBuffer[4]);
}
