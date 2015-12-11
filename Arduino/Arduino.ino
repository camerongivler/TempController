#include <Wire.h>
#include <math.h>

#define MCP4725_ADDR 0x60

const unsigned long oneSecond = 1000;
const unsigned long numSecsBetweenReads = 60;
const unsigned long deltaSerialEvent = 100; // milliseconds
const int tempPin = A1;
const int humPin = A0;
const int numValues = 120;
float tempValues[numValues] = {
  0};
float humValues[numValues] = {
  0};
String inputString = "";  //This is global in case serialEvent is called mid-transmission
boolean getTemp;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  
  pinMode(tempPin, INPUT); 
  pinMode(humPin, INPUT); 
  pinMode(A2, OUTPUT);
  pinMode(A3, OUTPUT);
  pinMode(10, OUTPUT);
  digitalWrite(10, HIGH);
  digitalWrite(A2, LOW);//Set A2 as GND
  digitalWrite(A3, HIGH);//Set A3 as Vcc
}

void loop() {
  tempValues[0] = getTemperature(analogRead(tempPin) / 204.6);
  humValues[0] = getHumidity(analogRead(humPin) / 204.6);
  for(int i = 0; i < numSecsBetweenReads * oneSecond / deltaSerialEvent; i++) {
    delay(deltaSerialEvent);
    serialEvent(); //Read a serialEvent every deltaSerialEvent.
  }
  incrementQueue();
}

void incrementQueue() {
  for(int i = numValues - 1; i > 0; i--) {
    tempValues[i] = tempValues[i - 1];
  }
  for(int i = numValues - 1; i > 0; i--) {
    humValues[i] = humValues[i - 1];
  }
}

boolean serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n') {
      // This is where the command is handled
      if(inputString == "get data\r\n") {
        sendTemperatures();
        sendHumidities();
      } else if (inputString == "setTemp\r\n") {
        setTemp(Serial.parseFloat());
      }      // End Command Handle
      inputString = "";
      return true;
    }
  }
  return false;
}

void sendTemperatures(){
  sendData("temperatures", tempValues);
}

void sendHumidities() {
  sendData("humidities", humValues);
}

void sendData(String str, float values[]) {
  Serial.println("\n" + str);
  Serial.print(values[0]);
  for(int i = 1; i < numValues; i++) {
    Serial.print(",");
    Serial.print(values[i]);
  }
  Serial.println();
}

void setTemp(float temp){
  int voltage = getVoltage(temp) * 819; // 12-bit integer
  Serial.print("setting voltage temp: ");
  Serial.print(voltage);
  Serial.print(" temperature: ");
  Serial.println(temp);
  Wire.beginTransmission(MCP4725_ADDR);
  Wire.write(64);                     // cmd to update the DAC
  Wire.write(voltage >> 4);        // the 8 most significant bits
  Wire.write((voltage & 15) << 4); // the 4 least significant bits
  //Wire.write(voltage);
  Wire.endTransmission();
}

float getVoltage(float temp) {
  return 3.286*exp(-0.04819*temp);
}

float getTemperature(float voltage) {
  return log(voltage / 3.286) / -0.04819;
}

float getHumidity(float voltage) {
  return 50.19*voltage - 29.69;
}


