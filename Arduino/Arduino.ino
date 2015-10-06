const int oneSecond = 1000;
const int numSecsBetweenReads = 60;
const int deltaSerialEvent = 100; // milliseconds
const int inputPin = 23; //A0
const int numValues = 120;
int tempValues[numValues] = {0};
String inputString = "";  //This is global in case serialEvent is called mid-transmission

void setup() {
  Serial.begin(9600);
}

void loop() {
  for(int i = 0; i < numSecsBetweenReads * oneSecond / deltaSerialEvent; i++) {
    delay(deltaSerialEvent);
    while(!serialEvent()); //Read a serialEvent every deltaSerialEvent.
  }
  incrementQueue();
  tempValues[0] = analogRead(inputPin);
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
      // This is where the command would be handled
      Serial.println(inputString);
      // End Command Handle
      inputString = "";
      return true;
    }
  }
  return false;
}
