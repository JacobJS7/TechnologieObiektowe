#include <TinyGPS++.h>
#include <SoftwareSerial.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

static const int RXPin = 12, TXPin = 14;
static const uint32_t GPSBaud = 9600;
TinyGPSPlus gps;
SoftwareSerial ss(RXPin, TXPin);

void setup(){
  Serial.begin(9600);
  Serial.println("Start...");
  //ss.begin(GPSBaud);
  if(!ss.begin(GPSBaud)){
	Serial.println("Blad inicjalizacji gps");
  }

}


void loop(){
  
  while (ss.available() > 0){
    if(gps.encode(ss.read())){
      if (gps.location.isUpdated()){
        Serial.println("Time | Date | Latitude | Longitude | Altitude | Course | Speed | Satelites | HDOP");
        
        String Time = String(gps.time.hour()+2) + ":" + String(gps.time.minute()) + ":" + String(gps.time.second());
        
        Serial.print(Time); 
        Serial.print(";"); 

        String Date = String(gps.date.day()) + "/" + String(gps.date.month()) + "/" + String(gps.date.year());

        Serial.print(Date);
        Serial.print(";"); 

        String LocationData = String(gps.location.lat(), 6) + ";" + String(gps.location.lng(), 6) + ";" + String(gps.altitude.meters());

        Serial.print(LocationData);
        Serial.print(";"); 

        String CourseData = String(gps.course.deg()) + ";" + String(gps.speed.kmph());

        Serial.print(CourseData); 
        Serial.print(";"); 
       
        String GPSControlData = String(gps.satellites.value()) + ";" + String(gps.hdop.value());
        Serial.print(GPSControlData); 
        Serial.println(" ");
        
        delay(2000);
      }
    }
  }
  

}
