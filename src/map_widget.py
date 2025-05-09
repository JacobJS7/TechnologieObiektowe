from PyQt5.QtWebEngineWidgets import QWebEngineView
import html


class MapWidget(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.load_map()

    def _get_base_html(self, center_lat=52.2298, center_lon=21.0122, zoom=12):
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
            </style>
        </head>
        <body>
            <div id="mapid"></div>
            <script>
                var map = L.map('mapid').setView([{center_lat}, {center_lon}], {zoom});
                L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                    attribution: '© OpenStreetMap contributors'
                }}).addTo(map);

                // PLACEHOLDER_FOR_MARKERS
                // PLACEHOLDER_FOR_POLYLINE
            </script>
        </body>
        </html>
        """

    def load_map(self):
        self.setHtml(self._get_base_html())

    def load_points(self, points):
        if not points:
            self.load_map()
            return

        # markery
        markers_js = ""
        path_coords = []  # tablica punktow

        for i, p in enumerate(points, 1):
            popup_content = (
                f"Punkt {i} <br> "
                f"Godzina: {p.time} <br>"
                f"Data: {p.date}<br>"
                f"Prędkość: {p.speed} km/h`"
            )

            # dodawanie markerow do punktow
            icon_js = ""
            if i == 1:
                icon_js = "icon: L.divIcon({className: 'marker-start', html: '<div style=\"background-color: blue; width: 10px; height: 10px; border-radius: 50%;\"></div>'})"
            elif i == len(points):
                icon_js = "icon: L.divIcon({className: 'marker-end', html: '<div style=\"background-color: red; width: 10px; height: 10px; border-radius: 50%;\"></div>'})"

            markers_js += f"L.marker([{p.latitude}, {p.longitude}], {{{icon_js}}}).addTo(map).bindPopup('{popup_content}');\n"
            path_coords.append(f"[{p.latitude}, {p.longitude}]")

        polyline_js = f"L.polyline([{', '.join(path_coords)}], {{color: 'lime', weight: 3}}).addTo(map);"

        html_content = self._get_base_html(
            center_lat=points[0].latitude,
            center_lon=points[0].longitude,
            zoom=13
        )

        html_content = html_content.replace("// PLACEHOLDER_FOR_MARKERS", markers_js)
        html_content = html_content.replace("// PLACEHOLDER_FOR_POLYLINE", polyline_js)

        self.setHtml(html_content)