from PyQt5.QtWebEngineWidgets import QWebEngineView


class MapWidget(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.load_map()

    def load_map(self):
        map_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Mapa</title>
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
            <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
        </head>
        <body style="margin:0">
            <div id="mapid" style="width: 100%; height: 100vh;"></div>
            <script>
                var map = L.map('mapid').setView([52.2298, 21.0122], 12);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '© OpenStreetMap contributors'
                }).addTo(map);
            </script>
        </body>
        </html>
        """
        self.setHtml(map_html)

    def load_points(self, points):
        markers_js = ""
        path_coords = []  #wspolrzedne laczenia
        i = 1
        for p in points:
            popup = f"Punkt {i} <br>Godzina: {p.time}<br>Data: {p.date}<br>Prędkość: {p.speed} km/h"
            markers_js += f"L.marker([{p.latitude}, {p.longitude}]).addTo(map).bindPopup('{popup}');\n"
            path_coords.append(f"[{p.latitude}, {p.longitude}]")
            i += 1

        polyline_js = f"L.polyline([{', '.join(path_coords)}], {{color: 'orange'}}).addTo(map);"

        html = f"""
           <!DOCTYPE html>
           <html>
           <head>
               <meta charset="utf-8" />
               <meta name="viewport" content="width=device-width, initial-scale=1.0">
               <title>Mapa</title>
               <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
               <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
           </head>
           <body style="margin:0">
               <div id="mapid" style="width: 100%; height: 100vh;"></div>
               <script>
                   var map = L.map('mapid').setView([{points[0].latitude}, {points[0].longitude}], 13);
                   L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                       attribution: '© OpenStreetMap contributors'
                   }}).addTo(map);
                   {markers_js}
                   {polyline_js}
               </script>
           </body>
           </html>
           """
        self.setHtml(html)
