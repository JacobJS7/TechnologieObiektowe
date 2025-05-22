/**
 * @file display_drawings.h
 * @brief Biblioteka do obsługi wyświetlacza urządzenia TransportTracker
 * @author Jakub Szczur
 * @date 21.05.2025
 * 
 * Plik zawiera funkcje i struktury do rysowania różnych interfejsów
 * użytkownika na wyświetlaczu OLED SSD1306 128x64.
 */

#include "U8g2lib.h"

/**
 * @brief Bitmapa ikony używanej w interfejsie
 * 
 * Reprezentuje ikonę używaną przy wyświetlaniu informacji o prędkości.
 */
static const unsigned char image_download_bits[] U8X8_PROGMEM = {0x01,0x00,0x03,0x00,0x07,0x00,0x0d,0x00,0x1d,0x00,0x39,0x00,0x79,0x00,0xf1,0x00,0xf1,0x01,0xe1,0x03,0xf1,0x07,0x09,0x00,0x05,0x00,0x03,0x00,0x01,0x00,0x00,0x00};

/**
 * @brief Bitmapa ikony używanej w interfejsie
 * 
 * Reprezentuje ikonę używaną przy wyświetlaniu informacji o satelitach.
 */
static const unsigned char image_download_1_bits[] U8X8_PROGMEM = {0x00,0x70,0x00,0x50,0x00,0x50,0x00,0x50,0x00,0x57,0x00,0x57,0x00,0x57,0x00,0x57,0x70,0x57,0x70,0x57,0x70,0x57,0x70,0x57,0x77,0x57,0x77,0x57,0x77,0x77,0x00,0x00};

/**
 * @brief Bitmapa ikony używanej w interfejsie
 * 
 * Reprezentuje ikonę używaną przy wyświetlaniu informacji o pozycji geograficznej.
 */
static const unsigned char image_download_2_bits[] U8X8_PROGMEM = {0xc0,0x01,0x20,0x02,0x90,0x04,0x48,0x09,0x48,0x09,0x88,0x08,0x10,0x04,0x20,0x02,0x20,0x02,0x58,0x0d,0x84,0x10,0x84,0x10,0x02,0x20,0x02,0x20,0x39,0x4e,0xc7,0x71};

/**
 * @brief Bitmapa ikony używanej w interfejsie
 * 
 * Reprezentuje ikonę używaną przy wyświetlaniu informacji o baterii.
 */
static const unsigned char image_download_3_bits[] U8X8_PROGMEM = {0x00,0x00,0x00,0xf0,0xff,0x7f,0x08,0x00,0x80,0x68,0xdb,0xb6,0x6e,0xdb,0xb6,0x61,0xdb,0xb6,0x61,0xdb,0xb6,0x61,0xdb,0xb6,0x61,0xdb,0xb6,0x61,0xdb,0xb6,0x6e,0xdb,0xb6,0x68,0xdb,0xb6,0x08,0x00,0x80,0xf0,0xff,0x7f,0x00,0x00,0x00,0x00,0x00,0x00};

/**
 * @struct SensorReadoutStructure
 * @brief Struktura przechowująca odczyty sensorów GPS i inne dane
 */
struct SensorReadoutStructure{
    uint8_t hour;      ///< Godzina z odczytu GPS
    uint8_t minute;    ///< Minuta z odczytu GPS
    uint8_t second;    ///< Sekunda z odczytu GPS
    uint8_t day;       ///< Dzień z odczytu GPS
    uint8_t month;     ///< Miesiąc z odczytu GPS
    uint16_t year;     ///< Rok z odczytu GPS
    float latitude;    ///< Szerokość geograficzna w stopniach
    float longitude;   ///< Długość geograficzna w stopniach
    float altitude;    ///< Wysokość nad poziomem morza w metrach
    float course;      ///< Kierunek ruchu w stopniach
    float speed;       ///< Prędkość w km/h
    uint32_t satellites; ///< Liczba widocznych satelitów GPS
    int32_t hdop;      ///< Horyzontalna dokładność pozycji (HDOP)
    uint16_t voltage;  ///< Napięcie baterii w mV
};

/**
 * @brief Wyświetla wszystkie informacje na ekranie OLED
 * 
 * Funkcja rysuje kompletny interfejs użytkownika z danymi GPS, czasem,
 * datą, prędkością, kursem, liczba satelitów i napięciem baterii.
 * Wykorzystuje ikony i segmentację ekranu liniami dla lepszej czytelności.
 * 
 * @param u8g2 Obiekt wyświetlacza OLED
 * @param SensorReadout Struktura zawierająca dane do wyświetlenia
 */
void displayAllInfo(U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2, SensorReadoutStructure SensorReadout);

/**
 * @brief Bitmapa obrazu satelity używana przy wyświetlaniu alertu o braku sygnału GPS
 */
static const unsigned char image_Layer_3_bits[];

/**
 * @brief Wyświetla komunikat o oczekiwaniu na sygnał GPS
 * 
 * Funkcja pokazuje ekran alertu z tekstem "Oczekuje GPS..." oraz
 * grafiką satelity. Wyświetla się gdy urządzenie nie ma jeszcze
 * ustalonej pozycji GPS.
 * 
 * @param u8g2 Obiekt wyświetlacza OLED
 */
void displayAlert(U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2);

/**
 * @brief Wyświetla menu wyboru interwału zapisu
 * 
 * Funkcja rysuje interfejs wyboru interwału logowania danych. 
 * Użytkownik może wybierać spośród czterech opcji: 5, 15, 30 lub 60 sekund.
 * Aktualnie wybrana opcja jest zaznaczona ramką.
 * 
 * @param u8g2 Obiekt wyświetlacza OLED
 * @param selectedOption Indeks aktualnie wybranej opcji (0-3)
 */
void displayIntervalSelection(U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2, uint8_t selectedOption);
