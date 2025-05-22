from PyQt5.QtWebEngineWidgets import QWebEngineView
from road_info_service import RoadInfoService

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
        self.road_service = RoadInfoService()  # Używamy zewnętrznego serwisu

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

    def load_points(self, points):
        """
        Ładuje punkty GPS na mapę oraz koloruje trasę w zależności od przekroczenia limitu prędkości.

        :param points: Lista punktów GPS
        :type points: list
        """
        if not points:
            self.load_map()
            return

        road_segments = self.road_service.get_route_speed_limits(points)
        
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
                    _, speed_limit, road_type = self.road_service.find_nearest_road_segment(
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