# Py Road - GPS Route Visualizer

## Introduction

Py Road is a Python-based GPS route visualization tool that allows users to import GPS data, display routes on interactive maps, analyze route statistics, and generate various data plots.

## Features

- **GPS Data Import**: Load GPS data from text files
- **Interactive Map Visualization**: Display routes on an OpenStreetMap with:
  - Color-coded route segments based on speed limits
  - Start and end point markers
  - Point-by-point information
- **Data Analysis**:
  - Speed analysis with comparison to road speed limits
  - Altitude tracking
  - Satellite connection information
  - Battery voltage monitoring
- **Charts and Graphs**:
  - Speed over time
  - Altitude profile
  - HDOP (Horizontal Dilution of Precision) accuracy
  - Satellite count
  - Battery voltage
- **Export Functionality**:
  - Export the visualized map as HTML

## Installation

### Prerequisites

- Python 3.12
- PyQt5
- PyQtWebEngine
- Matplotlib
- Requests

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/TechnologieObiektowe.git
   cd TechnologieObiektowe
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install PyQt5 PyQtWebEngine matplotlib requests
   ```

## Usage

1. Run the application:
   ```bash
   python src/main.py
   ```

2. **Importing GPS data**:
   - Click on "Plik" → "Importuj"
   - Select a GPS data file recorded by dedicated device (format: [time;date;latitude;longitude;altitude;course;speed;satellites;hdop;voltage])

3. **Viewing data**:
   - The map will display your route with color-coding:
     - Green segments: Speed within limits
     - Red segments: Speed exceeding limits
   - Click on points in the left panel to view detailed information
   - The bottom panel shows details for the selected point

4. **Generating plots**:
   - Click on "Wykresy" menu and select one of the available charts:
     - "Wykres prędkości" - Speed chart
     - "Wykres wysokości npm" - Altitude chart
     - "Wykres dokładności HDOP" - HDOP accuracy chart
     - "Wykres ilości satelit" - Satellite count chart
     - "Wykres napięcia baterii" - Battery voltage chart

5. **Exporting maps**:
   - Click on "Plik" → "Eksportuj"
   - Choose a location to save the HTML file

## Architecture

### Components

1. **MainWindow** - Main application window
   - Handles UI setup, menu creation, and overall application logic

2. **MapWidget** - Map visualization component
   - Renders routes on OpenStreetMap using Leaflet
   - Fetches speed limits from OpenStreetMap
   - Calculates and visualizes speed limit violations

3. **GPSLoader** - Data loading component
   - Parses GPS data from text files
   - Converts raw data into `GPSPoint` objects

4. **Plotter** - Data visualization component
   - Generates various matplotlib-based charts from GPS data

### Data Format

The application expects GPS data in text files with the following semicolon-separated format:

```
time;date;latitude;longitude;altitude;course;speed;satellites;hdop;voltage
```

Where:
- `time`: Time of the GPS recording
- `date`: Date of the GPS recording
- `latitude`, `longitude`: Geographic coordinates
- `altitude`: Height above sea level in meters
- `course`: Direction in degrees
- `speed`: Speed in km/h
- `satellites`: Number of satellites connected
- `hdop`: Horizontal Dilution of Precision (accuracy indicator)
- `voltage`: Battery voltage in mV
