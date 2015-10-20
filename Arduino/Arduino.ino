const unsigned long oneSecond = 1000;
const unsigned long numSecsBetweenReads = 60;
const unsigned long deltaSerialEvent = 100; // milliseconds
const int inputPin = 23; //A0
const int numValues = 120;
float tempValues[numValues] = {0};
String inputString = "";  //This is global in case serialEvent is called mid-transmission

void setup() {
  Serial.begin(9600);
  tempValues[0] = analogRead(inputPin) / 204.6;
}

void loop() {
  for(int i = 0; i < numSecsBetweenReads * oneSecond / deltaSerialEvent; i++) {
    delay(deltaSerialEvent);
    serialEvent(); //Read a serialEvent every deltaSerialEvent.
  }
  incrementQueue();
  tempValues[0] = analogRead(inputPin) / 204.6;
}

void incrementQueue() {
  for(int i = numValues - 1; i > 0; i--) {
    tempValues[i] = tempValues[i - 1];
  }
}

boolean serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n') {
      // This is where the command is handled
      if(inputString == "get data\r\n") {
        sendData();
      }
      // End Command Handle
      inputString = "";
      return true;
    }
  }
  return false;
}

void sendData() {
  Serial.println("data");
  Serial.print(tempValues[0]);
  for(int i = 1; i < numValues; i++) {
    Serial.print(",");
    Serial.print(tempValues[i]);
  }
  Serial.println();
}
