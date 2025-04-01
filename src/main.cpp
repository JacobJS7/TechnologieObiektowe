#include <TinyGPS++.h>
#include <Wire.h>
#include <SoftwareSerial.h>

TinyGPSPlus gps;
SoftwareSerial gpsSerial(6, -1); //6 -> TX only
SoftwareSerial openLogSerial(-2, 7); //7 -> RX only

struct SensorReadoutStructure{
  uint8_t hour;
  uint8_t minute;
  uint8_t second; 
  uint8_t day;
  uint8_t month;
  uint16_t year;
  float latitude;
  float longitude;
  float altitude;
  float course;
  float speed;
  uint32_t satellites;
  int32_t hdop;
};

SensorReadoutStructure SensorReadout;

void PrintData(struct SensorReadoutStructure SensorReadout){
  Serial.printf("%02d:%02d:%02d;", SensorReadout.hour, SensorReadout.minute, SensorReadout.second);
  Serial.printf("%02d/%02d/%04d;", SensorReadout.day, SensorReadout.month, SensorReadout.year);
  Serial.printf("%.6f;%.6f;%.2f;", SensorReadout.latitude, SensorReadout.longitude, SensorReadout.altitude);
  Serial.printf("%.2f;%.2f;", SensorReadout.course, SensorReadout.speed);
  Serial.printf("%d;%d", SensorReadout.satellites, SensorReadout.hdop);
  Serial.printf("\n");
}
void PrintDataToOpenLog(struct SensorReadoutStructure SensorReadout){
  openLogSerial.printf("%02d:%02d:%02d;", SensorReadout.hour, SensorReadout.minute, SensorReadout.second);
  openLogSerial.printf("%02d/%02d/%04d;", SensorReadout.day, SensorReadout.month, SensorReadout.year);
  openLogSerial.printf("%.6f;%.6f;%.2f;", SensorReadout.latitude, SensorReadout.longitude, SensorReadout.altitude);
  openLogSerial.printf("%.2f;%.2f;", SensorReadout.course, SensorReadout.speed);
  openLogSerial.printf("%d;%d", SensorReadout.satellites, SensorReadout.hdop);
  openLogSerial.printf("\n");
}

void setup(){
  Serial.begin(115200);
  Serial.println("Startujemy...");
  gpsSerial.begin(9600);
  openLogSerial.begin(9600);
  if(!gpsSerial){
	  Serial.println("Blad inicjalizacji gps");
  }
}

void loop(){
  while (gpsSerial.available() > 0){
    if(gps.encode(gpsSerial.read())){
      if (gps.location.isUpdated()){
        Serial.println("Time | Date | Latitude | Longitude | Altitude | Course | Speed | Satelites | HDOP");
        
        SensorReadout.hour = gps.time.hour()+2;
        SensorReadout.minute = gps.time.minute();
        SensorReadout.second = gps.time.second();

        SensorReadout.day = gps.date.day();
        SensorReadout.month = gps.date.month();
        SensorReadout.year = gps.date.year();

        SensorReadout.latitude = gps.location.lat();
        SensorReadout.longitude = gps.location.lng();
        SensorReadout.altitude = gps.altitude.meters();

        SensorReadout.course = gps.course.deg();
        SensorReadout.speed = gps.speed.kmph();
        
        SensorReadout.satellites = gps.satellites.value();
        SensorReadout.hdop = gps.hdop.value();
        
        PrintData(SensorReadout);
        PrintDataToOpenLog(SensorReadout);
        
        delay(2000);
      }
    }
  }

}