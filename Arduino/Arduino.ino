const unsigned long oneSecond = 1000;
const unsigned long numSecsBetweenReads = 60;
const unsigned long deltaSerialEvent = 100; // milliseconds
const int tempPin = A0;
const int tempSetPin = A2;
const int humPin = A1;
const int numValues = 120;
float tempValues[numValues] = {
  0};
float humValues[numValues] = {
  0};
String inputString = "";  //This is global in case serialEvent is called mid-transmission
boolean getTemp;

void setup() {
  Serial.begin(9600);
  tempValues[0] = analogRead(tempPin) / 204.6;
  humValues[0] = analogRead(humPin) / 204.6;
}

void loop() {
  for(int i = 0; i < numSecsBetweenReads * oneSecond / deltaSerialEvent; i++) {
    delay(deltaSerialEvent);
    serialEvent(); //Read a serialEvent every deltaSerialEvent.
  }
  incrementQueue();
  tempValues[0] = analogRead(tempPin) / 204.6;
  humValues[0] = analogRead(humPin) / 204.6;
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

// t = 1/(0.001284 + 2.364e-4 * log(V/I) + 9.304e-8 * log(V/I)^3)
// I = 10mA?

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

void setTemp(float num){
  analogWrite(tempSetPin, num * 51);
}

