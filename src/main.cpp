/**
 * @file main.cpp
 * @brief Program główny dla urządzenia TransportTracker - rejestratora GPS
 * @author Jakub Szczur
 * @date 21.05.2025
 * 
 * TransportTracker to urządzenie zapisujące pozycję GPS w regularnych odstępach czasu,
 * wyposażone w wyświetlacz OLED pokazujący aktualne dane.
 */

#include <TinyGPS++.h>
#include <Wire.h>
#include <SoftwareSerial.h>
#include "U8g2lib.h"
#include "display_drawings.h"

/**
 * @defgroup Pin_Definitions Definicje pinów
 * @{
 */
#define Battery_Pin 4  ///< Pin do odczytu napięcia baterii
#define GPS_TX 6       ///< Pin odbierający dane z modułu GPS
#define OpenLog_RX 7   ///< Pin wysyłający dane do modułu OpenLog
#define Up_Button 3    ///< Pin przycisku w górę (zmiana interwału)
#define Down_Button 2  ///< Pin przycisku w dół (potwierdzenie wyboru)
//SDA 8              ///< Pin danych I2C dla wyświetlacza
//SCL 9              ///< Pin zegara I2C dla wyświetlacza
/** @} */

/**
 * @brief Obiekt do przetwarzania danych GPS
 */
TinyGPSPlus gps;

/**
 * @brief Port szeregowy do komunikacji z modułem GPS (tylko RX)
 */
SoftwareSerial gpsSerial(GPS_TX, -1); //6 -> TX only

/**
 * @brief Port szeregowy do komunikacji z modułem OpenLog (tylko TX)
 */
SoftwareSerial openLogSerial(-2, OpenLog_RX); //7 -> RX only

/**
 * @brief Obiekt do obsługi wyświetlacza OLED 128x64 na I2C
 */
U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE, /* clock=*/ 9, /* data=*/ 8);

/**
 * @brief Struktura przechowująca aktualne odczyty z sensorów
 */
SensorReadoutStructure SensorReadout;

/**
 * @brief Dostępne opcje interwału zapisu danych (w milisekundach)
 */
const uint32_t intervalOptions[4] = {5000, 15000, 30000, 60000};

/**
 * @brief Indeks aktualnie wybranego interwału zapisu
 */
uint8_t selectedInterval = 0;

/**
 * @brief Aktualnie wybrany interwał zapisu w milisekundach
 */
uint32_t loggingInterval = 5000; // Default 5s

/**
 * @brief Timestamp ostatniego zapisu danych
 */
uint32_t lastLogTime = 0;

/**
 * @brief Flaga wskazująca czy sygnał GPS został nawiązany
 */
bool gpsSignalAcquired = false;

/**
 * @brief Wypisuje dane z sensorów na port szeregowy
 * 
 * @param SensorReadout Struktura z aktualnymi odczytami sensorów
 */
void PrintData(struct SensorReadoutStructure SensorReadout){
  Serial.printf("%02d:%02d:%02d;", SensorReadout.hour, SensorReadout.minute, SensorReadout.second);
  Serial.printf("%02d/%02d/%04d;", SensorReadout.day, SensorReadout.month, SensorReadout.year);
  Serial.printf("%.6f;%.6f;%.2f;", SensorReadout.latitude, SensorReadout.longitude, SensorReadout.altitude);
  Serial.printf("%.2f;%.2f;", SensorReadout.course, SensorReadout.speed);
  Serial.printf("%d;%d;", SensorReadout.satellites, SensorReadout.hdop);
  Serial.printf("%d",SensorReadout.voltage);
  Serial.printf("\n");
}

/**
 * @brief Wypisuje dane z sensorów do modułu OpenLog
 * 
 * @param SensorReadout Struktura z aktualnymi odczytami sensorów
 */
void PrintDataToOpenLog(struct SensorReadoutStructure SensorReadout){
  openLogSerial.printf("%02d:%02d:%02d;", SensorReadout.hour, SensorReadout.minute, SensorReadout.second);
  openLogSerial.printf("%02d/%02d/%04d;", SensorReadout.day, SensorReadout.month, SensorReadout.year);
  openLogSerial.printf("%.6f;%.6f;%.2f;", SensorReadout.latitude, SensorReadout.longitude, SensorReadout.altitude);
  openLogSerial.printf("%.2f;%.2f;", SensorReadout.course, SensorReadout.speed);
  openLogSerial.printf("%d;%d;", SensorReadout.satellites, SensorReadout.hdop);
  openLogSerial.printf("%d",SensorReadout.voltage);
  openLogSerial.printf("\n");
}

/**
 * @brief Obsługuje wybór interwału zapisu danych przez użytkownika
 * 
 * Funkcja wyświetla menu wyboru interwału i obsługuje przyciski użytkownika
 * do zmiany i potwierdzenia wyboru. Zawiera debouncing dla przycisków.
 * 
 * @return true gdy interwał został wybrany
 */
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

/**
 * @brief Funkcja inicjalizacyjna wywoływana raz przy starcie urządzenia
 * 
 * Inicjalizuje porty szeregowe, wyświetlacz, piny, oraz przeprowadza
 * wybór interwału zapisu danych przez użytkownika.
 */
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

/**
 * @brief Główna pętla programu
 * 
 * Odbiera dane GPS, przetwarza je, oraz w ustawionych odstępach czasu
 * zapisuje odczyty do pamięci i wyświetla na ekranie.
 * Gdy sygnał GPS jest niedostępny, wyświetla alert.
 */
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