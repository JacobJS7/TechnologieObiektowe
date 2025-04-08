#include <TinyGPS++.h>
#include <Wire.h>
#include <SoftwareSerial.h>
#include "U8g2lib.h"
#include "display_drawings.h"

#define Battery_Pin 4
#define GPS_TX 6
#define OpenLog_RX 7

TinyGPSPlus gps;
SoftwareSerial gpsSerial(GPS_TX, -1); //6 -> TX only
SoftwareSerial openLogSerial(-2, OpenLog_RX); //7 -> RX only
U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE, /* clock=*/ 9, /* data=*/ 8);

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
  uint16_t voltage;
};

SensorReadoutStructure SensorReadout;

void PrintData(struct SensorReadoutStructure SensorReadout){
  Serial.printf("%02d:%02d:%02d;", SensorReadout.hour, SensorReadout.minute, SensorReadout.second);
  Serial.printf("%02d/%02d/%04d;", SensorReadout.day, SensorReadout.month, SensorReadout.year);
  Serial.printf("%.6f;%.6f;%.2f;", SensorReadout.latitude, SensorReadout.longitude, SensorReadout.altitude);
  Serial.printf("%.2f;%.2f;", SensorReadout.course, SensorReadout.speed);
  Serial.printf("%d;%d;", SensorReadout.satellites, SensorReadout.hdop);
  Serial.printf("%d",SensorReadout.voltage);
  Serial.printf("\n");
}
void PrintDataToOpenLog(struct SensorReadoutStructure SensorReadout){
  openLogSerial.printf("%02d:%02d:%02d;", SensorReadout.hour, SensorReadout.minute, SensorReadout.second);
  openLogSerial.printf("%02d/%02d/%04d;", SensorReadout.day, SensorReadout.month, SensorReadout.year);
  openLogSerial.printf("%.6f;%.6f;%.2f;", SensorReadout.latitude, SensorReadout.longitude, SensorReadout.altitude);
  openLogSerial.printf("%.2f;%.2f;", SensorReadout.course, SensorReadout.speed);
  openLogSerial.printf("%d;%d;", SensorReadout.satellites, SensorReadout.hdop);
  openLogSerial.printf("%d",SensorReadout.voltage);
  openLogSerial.printf("\n");
}



void setup(){
  Serial.begin(115200);
  Serial.println("Startujemy...");
  gpsSerial.begin(9600);
  openLogSerial.begin(9600);
  u8g2.begin();
  pinMode(Battery_Pin, INPUT_PULLUP);

  if(!gpsSerial){
	  Serial.println("Blad inicjalizacji gps");
  }
  if(!openLogSerial){
	  Serial.println("Blad inicjalizacji openloga");
  }
}

void loop(){
  while (gpsSerial.available() > 0){
    if(gps.encode(gpsSerial.read())){
      if (gps.location.isUpdated()){
        Serial.println("Time | Date | Latitude | Longitude | Altitude | Course | Speed | Satelites | HDOP | Battery");
        
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

        SensorReadout.voltage = analogReadMilliVolts(Battery_Pin);
        
        PrintData(SensorReadout);
        PrintDataToOpenLog(SensorReadout);
        drawssd(u8g2);
        
        delay(2000);
      }
    }
  }

}