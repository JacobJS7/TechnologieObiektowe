#include <TinyGPS++.h>
#include <HardwareSerial.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

static const int RXPin = 4, TXPin = 5;
static const uint32_t GPSBaud = 9600;
TinyGPSPlus gps;
//SoftwareSerial gpsSerial(RXPin, TXPin);
HardwareSerial gpsSerial(1);

void setup(){
  Serial.begin(115200);
  Serial.println("Startujemy...");
  //gpsSerial.begin(GPSBaud);
  gpsSerial.begin(GPSBaud, SERIAL_8N1, 20, 21);
  if(!gpsSerial){
	  Serial.println("Blad inicjalizacji gps");
  }
}


void loop(){
  
  while (gpsSerial.available() > 0){
    if(gps.encode(gpsSerial.read())){
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