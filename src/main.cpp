#include <TinyGPS++.h>
#include <Wire.h>
#include <SoftwareSerial.h>
#include "U8g2lib.h"
#include "display_drawings.h"

#define Battery_Pin 4
#define GPS_TX 6
#define OpenLog_RX 7
#define Up_Button 3
#define Down_Button 2
//SDA 8
//SCL 9

TinyGPSPlus gps;
SoftwareSerial gpsSerial(GPS_TX, -1); //6 -> TX only
SoftwareSerial openLogSerial(-2, OpenLog_RX); //7 -> RX only
U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE, /* clock=*/ 9, /* data=*/ 8);
SensorReadoutStructure SensorReadout;

const uint32_t intervalOptions[4] = {5000, 15000, 30000, 60000};
uint8_t selectedInterval = 0;
uint32_t loggingInterval = 5000; // Default 5s
uint32_t lastLogTime = 0;
bool gpsSignalAcquired = false;

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

bool selectInterval() {
  bool intervalSelected = false;
  
  pinMode(Up_Button, INPUT_PULLUP);//GND
  pinMode(Down_Button, INPUT_PULLUP);//GND
  
  displayIntervalSelection(u8g2, selectedInterval);
  
  bool upButtonState = HIGH;
  bool downButtonState = HIGH;
  bool lastUpButtonState = HIGH;
  bool lastDownButtonState = HIGH;
  uint32_t lastUpDebounceTime = 0;
  uint32_t lastDownDebounceTime = 0;
  const uint32_t debounceDelay = 50; // 50ms debounce
  
  while (!intervalSelected) {
    bool currentUpState = digitalRead(Up_Button);
    bool currentDownState = digitalRead(Down_Button);
    
    if (currentUpState != lastUpButtonState) {
      lastUpDebounceTime = millis();
    }
    
    if ((millis() - lastUpDebounceTime) > debounceDelay) {
      if (currentUpState != upButtonState) {
        upButtonState = currentUpState;
        
        if (upButtonState == LOW) {
          selectedInterval = (selectedInterval + 1) % 4;
          displayIntervalSelection(u8g2, selectedInterval);
        }
      }
    }
    
    if (currentDownState != lastDownButtonState) {
      lastDownDebounceTime = millis();
    }
    
    if ((millis() - lastDownDebounceTime) > debounceDelay) {
      if (currentDownState != downButtonState) {
        downButtonState = currentDownState;
        
        if (downButtonState == LOW) {
          loggingInterval = intervalOptions[selectedInterval];
          intervalSelected = true;
        }
      }
    }
    
    lastUpButtonState = currentUpState;
    lastDownButtonState = currentDownState;
    
    delay(10); 
  }
  
  return true;
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
  
  selectInterval();
  
  u8g2.clearBuffer();
  u8g2.setFont(u8g2_font_6x12_tr);
  u8g2.drawStr(15, 25, "Interwal wybrany:");
  char intervalStr[20];
  snprintf(intervalStr, sizeof(intervalStr), "%d sekund", loggingInterval / 1000);
  u8g2.drawStr(30, 40, intervalStr);
  u8g2.sendBuffer();
  
  delay(2000); 
  
  Serial.print("Wybrano interwal: ");
  Serial.print(loggingInterval / 1000);
  Serial.println(" sekund");
  
  lastLogTime = millis(); 
}

void loop(){
  if(gpsSerial.available() <= 0 && !gpsSignalAcquired){
    displayAlert(u8g2);
  }
  
  while (gpsSerial.available() > 0){
    if(gps.encode(gpsSerial.read())){
      if (gps.location.isUpdated()){
        uint32_t currentTime = millis();
        gpsSignalAcquired = true;
        
        if (currentTime - lastLogTime >= loggingInterval) {
          lastLogTime = currentTime; // Reset timera
          
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
          displayAllInfo(u8g2, SensorReadout);
        }
      }
    }
  }
}