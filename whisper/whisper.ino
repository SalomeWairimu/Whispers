#include <NewPing.h>
#include <ESP8266WiFi.h>

// Network Credentials
const char* ssid = "Device-Northwestern";


int status = WL_IDLE_STATUS;
IPAddress server(129,105,209,248); 

// Define the Pin Numbers
#define TRIGGER_PIN 2
#define ECHO_PIN 0
#define MAX_DISTANCE 200
WiFiClient client;
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);
void setup() {
 Serial.begin(115200); Serial.print("beginning");
// pinMode(TRIGGER_PIN, OUTPUT); // Set trigger pin as output
// pinMode(ECHO_PIN, INPUT); // Set echo pin as input
 // pinMode(BUILTIN_LED, OUTPUT);

wifiConnect();
}

//void loop() {
//  long duration, distance;
//
//  // Clear the trigger pin
//  digitalWrite(TRIGGER_PIN, LOW);
//  delayMicroseconds(2);
//
//  // Sets the trigger pin on high for 10 microseconds
//  digitalWrite(TRIGGER_PIN, HIGH);
//  delayMicroseconds(10);
//  digitalWrite(TRIGGER_PIN, LOW);
//
//  // Reads the trigger pin and returns the sound wave travel time in microseconds
//  duration = pulseIn(ECHO_PIN, HIGH);
//  distance = (duration/2) / 29.1; // Speed of sound in air is 29.1 microseconds per centimeter
//  String payload = "{ \"d\" : {\"distance\":";
//  payload += distance;
//  payload += "}}";
//  Serial.println(payload);
//    // if you get a connection, report back via serial:
//  if (client.connect(server, 65432)) {
//    Serial.println("connected");
//    // Make a HTTP request:
//    client.println(payload);
//  }
//}

void loop() {

delayMicroseconds(2);

unsigned int uS = sonar.ping();

pinMode(ECHO_PIN,OUTPUT);

digitalWrite(ECHO_PIN,LOW);

pinMode(ECHO_PIN,INPUT);

//Serial.print("Ping: ");
//
//Serial.print(uS / US_ROUNDTRIP_CM);
//
//Serial.println("cm");

String payload = "{ \"d\" : {\"distance\":";
payload += uS / US_ROUNDTRIP_CM;
payload += "}}";
Serial.print(payload);

if (client.connect(server, 65432)) {
  Serial.println("connected");
  // Make a HTTP request:
  client.println(payload);
}
delay(10000);
}

void wifiConnect() {
 Serial.print("Connecting to "); Serial.print(ssid);
 WiFi.begin(ssid);
 while (WiFi.status() != WL_CONNECTED) {
   delay(500);
   Serial.println(".");
 }
 Serial.print("WiFi connected, IP address: "); Serial.println(WiFi.localIP());
}
