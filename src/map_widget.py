from PyQt5.QtWebEngineWidgets import QWebEngineView
import requests
import time
from math import radians, sin, cos, sqrt, atan2


class MapWidget(QWebEngineView):
    """
    Widget do wyświetlania interaktywnych map z trasami GPS.
    
    Używa OpenStreetMap przez Leaflet do wizualizacji tras GPS z kolorowaniem
    na podstawie limitów prędkości pobranych z API OpenStreetMap.
    """
    
    def __init__(self):
        """Inicjalizuje widget mapy i ładuje mapę bazową."""
        super().__init__()
        self.load_map()
        self.speed_limits_cache = {}  # Cache na limity prędkości, aby ograniczyć liczbę zapytań do API

    def _get_base_html(self, center_lat=52.2298, center_lon=21.0122, zoom=12):
        """
        Generuje bazowy kod HTML dla mapy.
        
        :param center_lat: Początkowa szerokość geograficzna środka mapy
        :type center_lat: float
        :param center_lon: Początkowa długość geograficzna środka mapy
        :type center_lon: float
        :param zoom: Początkowy stopień powiększenia mapy
        :type zoom: int
        :return: Kod HTML z osadzoną mapą Leaflet
        :rtype: str
        """
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Mapa</title>
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
            <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
            <style>
                #mapid {{ width: 100%; height: 100vh; }}
                body {{ margin: 0; }}
                .speed-info {{ 
                    padding: 6px 8px; 
                    background: white; 
                    box-shadow: 0 0 15px rgba(0,0,0,0.2);
                    border-radius: 5px;
                }}
                .speed-info h4 {{ margin: 0 0 5px; }}
                .legend {{ line-height: 18px; color: #555; }}
                .legend i {{ width: 18px; height: 18px; float: left; margin-right: 8px; opacity: 0.7; }}
            </style>
        </head>
        <body>
            <div id="mapid"></div>
            <script>
                var map = L.map('mapid').setView([{center_lat}, {center_lon}], {zoom});
                L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                    attribution: '© OpenStreetMap contributors'
                }}).addTo(map);

                // Dodaj legendę
                var legend = L.control({{position: 'bottomright'}});
                legend.onAdd = function (map) {{
                    var div = L.DomUtil.create('div', 'speed-info legend');
                    div.innerHTML += '<h4>Prędkość</h4>';
                    div.innerHTML += '<i style="background:green"></i> W normie<br>';
                    div.innerHTML += '<i style="background:red"></i> Przekroczona<br>';
                    return div;
                }};
                legend.addTo(map);

                // PLACEHOLDER_FOR_MARKERS
                // PLACEHOLDER_FOR_POLYLINE
            </script>
        </body>
        </html>
        """

    def load_map(self):
        """Ładuje pustą mapę bazową."""
        self.setHtml(self._get_base_html())

    def get_route_speed_limits(self, points):
        """
        Pobiera limity prędkości dla całej trasy za jednym razem z Overpass API.

        :param points: Lista punktów GPS
        :type points: list
        :return: Słownik segmentów dróg i ich limitów prędkości oraz typy dróg
        :rtype: dict
        """
        if not points or len(points) < 2:
            return {}
            
        min_lat = min(p.latitude for p in points)
        max_lat = max(p.latitude for p in points)
        min_lon = min(p.longitude for p in points)
        max_lon = max(p.longitude for p in points)

        buffer = 0.00005  # ok 5m
        min_lat -= buffer
        max_lat += buffer
        min_lon -= buffer
        max_lon += buffer
        
        # Zapytanie Overpass API o wszystkie drogi z limitami prędkości w tym obszarze
        overpass_url = "https://overpass-api.de/api/interpreter"
        overpass_query = f"""
        [out:json];
        way["highway"]({min_lat},{min_lon},{max_lat},{max_lon});
        out geom;
        """
        
        road_segments = {}
        
        try:
            print("Pobieranie danych o drogach...")
            response = requests.get(overpass_url, params={"data": overpass_query}, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                print(f"Pobrano dane o {len(data.get('elements', []))} drogach")
                
                for road in data.get("elements", []):
                    tags = road.get("tags", {})
                    road_type = tags.get("highway", "unclassified")
                    
                    if "maxspeed" in tags:
                        try:
                            speed_limit = int(tags["maxspeed"].split()[0])
                        except (ValueError, IndexError):
                            # domyślny limit na podstawie typu drogi
                            speed_limit = self._get_default_speed_limit(road_type)
                    else:
                        speed_limit = self._get_default_speed_limit(road_type)
                            
                    # Wszystkie segmenty drogi
                    coords = road.get("geometry", [])
                    for i in range(len(coords) - 1):
                        start = (coords[i]["lat"], coords[i]["lon"])
                        end = (coords[i+1]["lat"], coords[i+1]["lon"])
                        segment = (start, end)
                        road_segments[segment] = (speed_limit, road_type)
                
                print(f"Znaleziono {len(road_segments)} segmentów dróg")
                road_types = {}
                for segment, (limit, road_type) in list(road_segments.items())[:10]:
                    if road_type not in road_types:
                        road_types[road_type] = limit
                print(f"Przykładowe typy dróg i limity: {road_types}")
            else:
                print(f"Błąd API: {response.status_code}")
                
        except Exception as e:
            print(f"Błąd podczas pobierania danych o drogach: {e}")
        
        return road_segments

    def _get_default_speed_limit(self, road_type):
        """
        Zwraca domyślny limit prędkości dla danego typu drogi w Polsce.
        
        :param road_type: Typ drogi z OSM
        :type road_type: str
        :return: Domyślny limit prędkości w km/h
        :rtype: int
        """
        limits = {
            'motorway': 140,
            'trunk': 120,
            'primary': 90,
            'secondary': 90,
            'tertiary': 90,
            'residential': 50,
            'service': 30,
            'living_street': 20,
            'motorway_link': 80,
            'trunk_link': 80,
            'primary_link': 70,
            'secondary_link': 70,
            'tertiary_link': 70,
        }
        return limits.get(road_type, 50)  # 50 km/h domyślny limit

    def find_nearest_road_segment(self, lat, lon, road_segments):
        """
        Znajduje najbliższy segment drogi dla danego punktu.

        :param lat: Szerokość geograficzna punktu
        :type lat: float
        :param lon: Długość geograficzna punktu
        :type lon: float
        :param road_segments: Słownik segmentów dróg i ich danych
        :type road_segments: dict
        :return: Najbliższy segment, jego limit prędkości i typ drogi
        :rtype: tuple
        """
        if not road_segments:
            return None, 50, "unknown"
            
        min_distance = float('inf')
        nearest_segment = None
        
        for segment, (speed_limit, road_type) in road_segments.items():
            # Oblicz odległość punktu od segmentu drogi
            distance = self.point_to_segment_distance_improved(lat, lon, *segment[0], *segment[1])
            
            if distance < min_distance:
                min_distance = distance
                nearest_segment = (segment, speed_limit, road_type)

        # Jeśli punkt jest dalej niż 10m od najbliższej drogi, użyj domyślnego limitu prędkości
        if min_distance > 0.01:  
            return None, 50, "unknown"
            
        return nearest_segment

    def point_to_segment_distance_improved(self, px, py, x1, y1, x2, y2):
        """
        Oblicza dokładną odległość punktu od odcinka drogi.

        :return: Odległość w kilometrach
        :rtype: float
        """
        # długość segmentu
        segment_length = self.haversine_distance(x1, y1, x2, y2)
        
        # Jeśli segment jest praktycznie punktem, zwróć odległość do tego punktu
        if segment_length < 0.00001:
            return self.haversine_distance(px, py, x1, y1)
        
        
        # minimum odległości do punktów początkowego i końcowego
        return min(
            self.haversine_distance(px, py, x1, y1),
            self.haversine_distance(px, py, x2, y2)
        )
        
    def haversine_distance(self, lat1, lon1, lat2, lon2):
        """
        Oblicza odległość między dwoma punktami geograficznymi w kilometrach.

        :param lat1: Szerokość geograficzna pierwszego punktu
        :type lat1: float
        :param lon1: Długość geograficzna pierwszego punktu
        :type lon1: float
        :param lat2: Szerokość geograficzna drugiego punktu
        :type lat2: float
        :param lon2: Długość geograficzna drugiego punktu
        :type lon2: float
        :return: Odległość w kilometrach
        :rtype: float
        """
        # Promień Ziemi w km
        R = 6371.0
        
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        return R * c

    def load_points(self, points):
        """
        Ładuje punkty GPS na mapę oraz koloruje trasę w zależności od przekroczenia limitu prędkości.

        :param points: Lista punktów GPS
        :type points: list
        """
        if not points:
            self.load_map()
            return

        # Pobieranie limity prędkości dla całej trasy za jednym razem
        road_segments = self.get_route_speed_limits(points)
        
        markers_js = ""
        segments_js = ""
        
        for i, p in enumerate(points, 1):
            popup_content = (
                f"Punkt {i} <br> "
                f"Godzina: {p.time} <br>"
                f"Data: {p.date}<br>"
                f"Prędkość: {p.speed} km/h"
            )

            # dodawanie markerow
            icon_js = ""
            if i == 1:
                icon_js = "icon: L.divIcon({className: 'marker-start', html: '<div style=\"background-color: blue; width: 10px; height: 10px; border-radius: 50%;\"></div>'})"
            elif i == len(points):
                icon_js = "icon: L.divIcon({className: 'marker-end', html: '<div style=\"background-color: red; width: 10px; height: 10px; border-radius: 50%;\"></div>'})"

            markers_js += f"L.marker([{p.latitude}, {p.longitude}], {{{icon_js}}}).addTo(map).bindPopup(`{popup_content}`);\n"


            if i > 1:
                prev_point = points[i-2]  
                
                try:
                    _, speed_limit, road_type = self.find_nearest_road_segment(
                        (prev_point.latitude + p.latitude)/2,  # środek segmentu
                        (prev_point.longitude + p.longitude)/2,
                        road_segments
                    )
                    
                    # porównanie prędkości z limitem
                    actual_speed = float(p.speed)
                    speed_exceeded = actual_speed > speed_limit
                    
                    color = 'red' if speed_exceeded else 'green'
                    
                    segments_js += f"""
                    L.polyline([[{prev_point.latitude}, {prev_point.longitude}], [{p.latitude}, {p.longitude}]], 
                        {{color: '{color}', weight: 4}}).addTo(map)
                        .bindTooltip('Typ drogi: {road_type}<br>Limit: {speed_limit} km/h<br>Prędkość: {p.speed} km/h');
                    """
                    print(f"Segment: droga typu {road_type}, limit {speed_limit} km/h, prędkość {p.speed} km/h")
                except (ValueError, TypeError) as e:
                    print(f"Błąd przetwarzania segmentu: {e}")
                    segments_js += f"""
                    L.polyline([[{prev_point.latitude}, {prev_point.longitude}], [{p.latitude}, {p.longitude}]], 
                        {{color: 'blue', weight: 4}}).addTo(map);
                    """

        html_content = self._get_base_html(
            center_lat=points[0].latitude,
            center_lon=points[0].longitude,
            zoom=13
        )

        html_content = html_content.replace("// PLACEHOLDER_FOR_MARKERS", markers_js)
        html_content = html_content.replace("// PLACEHOLDER_FOR_POLYLINE", segments_js)

        self.setHtml(html_content)