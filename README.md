# TransportTracker

## Overview
TransportTracker is an ESP32-C3 based GPS tracking system that records location data, speed, altitude, and other metrics. The project includes both firmware for the ESP32-C3 microcontroller and a companion desktop application for data visualization and analysis.

## Hardware Components
- ESP32-C3-DEVKITM-1 microcontroller
- NEO-6M GPS module (connected via SoftwareSerial)
- SSD1306 OLED display (using U8g2 library)

## Firmware Features
The ESP32 firmware (found in src/main.cpp) collects and logs:
- GPS coordinates (latitude/longitude)
- Speed
- Altitude
- Course/heading
- Time and date
- Number of satellites
- HDOP (Horizontal Dilution of Precision)
- Voltage level

### Libraries
The project uses the following libraries:
- [Adafruit AHTX0](https://github.com/adafruit/Adafruit_AHTX0) - For temperature and humidity sensing
- [Adafruit BMP280](https://github.com/adafruit/Adafruit_BMP280_Library) - For barometric pressure and altitude readings
- [TinyGPSPlus](https://github.com/mikalhart/TinyGPSPlus) - For parsing GPS NMEA data
- [EspSoftwareSerial](https://github.com/plerup/espsoftwareserial/) - For communication with the GPS module
- [U8g2](https://github.com/olikraus/u8g2) - For controlling the display

## Desktop Application
The companion desktop application provides tools for analyzing and visualizing the collected GPS data:

### Components
- **Main Application** (src/main.py) - Main GUI window with data import/export functionality
- **Map Widget** (src/map_widget.py) - Displays routes on interactive maps with markers
- **Plot Generator** (src/plot_generator.py) - Creates speed and altitude graphs
- **File Loader** (src/file_leader.py) - Parses GPS data from log files

### Features
- Import GPS data from log files
- Visualize routes on interactive maps
- Generate speed and altitude plots
- Export maps to HTML files
- View route segments with speed limit information

## File Format
The GPS data is stored in a semicolon-separated format with the following fields:
1. Time
2. Date
3. Latitude
4. Longitude
5. Altitude
6. Course
7. Speed
8. Satellites (count)
9. HDOP
10. Voltage

## Configuration
The ESP32 configuration is managed through `platformio.ini`:
- Serial monitor speed: 115200 baud
- Upload speed: 921600 baud
- USB mode is enabled for serial communication

## Building and Flashing

### Prerequisites
- [PlatformIO](https://platformio.org/install) installed (either as a VS Code extension or Core CLI)
- USB drivers for ESP32-C3 installed
- USB cable for connecting the device

### Building the Firmware
To build the firmware without uploading:
```
pio run
```

### Uploading the Firmware
To build and upload the firmware to the ESP32-C3:
```
pio run -t upload
```

If you need to specify a different port:
```
pio run -t upload --upload-port COM5
```

### Monitoring
To monitor the device's serial output:
```
pio device monitor
```

To build, upload, and start monitoring in one command:
```
pio run -t upload && pio device monitor
```

### Troubleshooting
- **Connection Issues**: If you encounter connection errors, try pressing the BOOT button on the ESP32-C3 while initiating the upload
- **Port Not Found**: Verify that the upload_port in platformio.ini matches your device's COM port
- **Driver Issues**: Make sure you have the correct USB-UART bridge drivers installed

### Clean Build
To clean the build files and start fresh:
```
pio run -t clean
```

## Development Setup
This project is developed using PlatformIO with Visual Studio Code. The required extensions and configurations are included in the `.vscode` directory.